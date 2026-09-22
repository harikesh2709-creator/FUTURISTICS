/**
 * SPECTRA — RF Phase-Space 3D Orbital Visualizer
 * Mathematically projects (I(t), Q(t), dφ/dt) into a 3D phase-space manifold.
 * Rendered with warm gold/silver particle trails matching the premium dark aesthetic.
 */

class RFOrbitalVisualizer {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        if (!canvasId || !this.canvas) return;
        this.ctx = this.canvas.getContext('2d');
        
        this.rotX = 0.4;
        this.rotY = 0.6;
        this.autoRotSpeed = 0.006;
        this.zoom = 1.0;
        this.isDragging = false;
        this.lastMouseX = 0;
        this.lastMouseY = 0;

        // Particle cloud
        this.numParticles = 500;
        this.particles = [];
        this.iqPoints = [];
        this.animId = null;

        this.initParticles();
        this.setupEvents();
        this.resize();
        this.start();
    }

    initParticles() {
        this.particles = [];
        for (let i = 0; i < this.numParticles; i++) {
            const u = (i / this.numParticles) * Math.PI * 2 * 6;
            const v = (i / this.numParticles) * Math.PI * 2;
            const rMajor = 70;
            const rMinor = 28 + Math.sin(u * 2) * 8;
            
            // Toroidal phase-space coordinates
            const x = (rMajor + rMinor * Math.cos(v)) * Math.cos(u * 0.4);
            const y = (rMajor + rMinor * Math.cos(v)) * Math.sin(u * 0.4);
            const z = rMinor * Math.sin(v) * 1.5;

            // Warm gold to silver to soft violet gradient
            const t = i / this.numParticles;
            let hue, sat, light;
            if (t < 0.4) {
                hue = 38 + t * 20; // Gold range
                sat = 60 + t * 20;
                light = 55 + t * 15;
            } else if (t < 0.7) {
                hue = 220 + (t - 0.4) * 30; // Silver-blue range
                sat = 20 + (t - 0.4) * 15;
                light = 65 + (t - 0.4) * 10;
            } else {
                hue = 260 + (t - 0.7) * 40; // Soft violet
                sat = 50 + (t - 0.7) * 30;
                light = 60 + (t - 0.7) * 10;
            }

            this.particles.push({
                baseX: x, baseY: y, baseZ: z,
                x, y, z,
                u, v,
                speed: 0.012 + (i % 5) * 0.003,
                size: 1.2 + (i % 3) * 0.7,
                hue,
                sat,
                light,
                alpha: 0.3 + (i % 4) * 0.12
            });
        }
    }

    setIQData(iData, qData) {
        if (!iData || !qData || iData.length === 0) return;
        this.iqPoints = [];
        const step = Math.max(1, Math.floor(iData.length / 300));
        let prevPhase = 0;
        
        for (let idx = 0; idx < iData.length; idx += step) {
            const I = iData[idx];
            const Q = qData[idx];
            const phase = Math.atan2(Q, I);
            const dPhase = phase - prevPhase;
            prevPhase = phase;

            this.iqPoints.push({
                x: I * 65,
                y: Q * 65,
                z: dPhase * 35,
                mag: Math.hypot(I, Q)
            });
        }
    }

    setupEvents() {
        this.canvas.addEventListener('mousedown', (e) => {
            this.isDragging = true;
            this.lastMouseX = e.clientX;
            this.lastMouseY = e.clientY;
        });

        window.addEventListener('mousemove', (e) => {
            if (!this.isDragging) return;
            const dx = e.clientX - this.lastMouseX;
            const dy = e.clientY - this.lastMouseY;
            this.rotY += dx * 0.01;
            this.rotX += dy * 0.01;
            this.lastMouseX = e.clientX;
            this.lastMouseY = e.clientY;
        });

        window.addEventListener('mouseup', () => {
            this.isDragging = false;
        });

        this.canvas.addEventListener('wheel', (e) => {
            e.preventDefault();
            this.zoom *= e.deltaY > 0 ? 0.95 : 1.05;
            this.zoom = Math.max(0.5, Math.min(2.0, this.zoom));
        }, { passive: false });
    }

    resize() {
        const rect = this.canvas.parentElement.getBoundingClientRect();
        const dpr = window.devicePixelRatio || 1;
        this.width = rect.width || 300;
        this.height = rect.height || 180;
        this.canvas.width = this.width * dpr;
        this.canvas.height = this.height * dpr;
        this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }

    start() {
        const renderLoop = () => {
            this.render();
            this.animId = requestAnimationFrame(renderLoop);
        };
        this.animId = requestAnimationFrame(renderLoop);
    }

    render() {
        const ctx = this.ctx;
        const W = this.width;
        const H = this.height;
        if (!W || !H) return;

        ctx.clearRect(0, 0, W, H);

        if (!this.isDragging) {
            this.rotY += this.autoRotSpeed;
        }

        const cx = W / 2;
        const cy = H / 2;
        const cosX = Math.cos(this.rotX);
        const sinX = Math.sin(this.rotX);
        const cosY = Math.cos(this.rotY);
        const sinY = Math.sin(this.rotY);
        const fov = 350 * this.zoom;

        // Warm atmospheric glow
        const grad = ctx.createRadialGradient(cx, cy, 10, cx, cy, Math.min(W, H) * 0.7);
        grad.addColorStop(0, 'rgba(200, 169, 110, 0.08)');
        grad.addColorStop(0.4, 'rgba(124, 106, 239, 0.03)');
        grad.addColorStop(1, 'rgba(0, 0, 0, 0)');
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, W, H);

        // Update particle positions
        const projected = [];

        // 1. Torus particle cloud
        for (let i = 0; i < this.particles.length; i++) {
            const p = this.particles[i];
            p.u += p.speed;
            p.v += p.speed * 0.7;

            const rMajor = 72;
            const rMinor = 24 + Math.sin(p.u * 3) * 6;
            const bx = (rMajor + rMinor * Math.cos(p.v)) * Math.cos(p.u * 0.5);
            const by = (rMajor + rMinor * Math.cos(p.v)) * Math.sin(p.u * 0.5);
            const bz = rMinor * Math.sin(p.v) * 1.4;

            // 3D Rotation
            const x1 = bx * cosY - bz * sinY;
            const z1 = bx * sinY + bz * cosY;
            const y2 = by * cosX - z1 * sinX;
            const z2 = by * sinX + z1 * cosX;

            const scale = fov / (fov + z2 + 250);
            const projX = cx + x1 * scale;
            const projY = cy + y2 * scale;

            projected.push({
                x: projX,
                y: projY,
                z: z2,
                size: Math.max(0.4, p.size * scale),
                color: `hsla(${p.hue}, ${p.sat}%, ${p.light}%, ${p.alpha * scale})`,
                glow: `hsla(${p.hue}, ${p.sat}%, ${p.light}%, ${p.alpha * 0.3})`
            });
        }

        // 2. Projected live I/Q orbit trail (if available)
        if (this.iqPoints.length > 0) {
            ctx.beginPath();
            let started = false;
            for (let i = 0; i < this.iqPoints.length; i++) {
                const pt = this.iqPoints[i];
                const x1 = pt.x * cosY - pt.z * sinY;
                const z1 = pt.x * sinY + pt.z * cosY;
                const y2 = pt.y * cosX - z1 * sinX;
                const z2 = pt.y * sinX + z1 * cosX;

                const scale = fov / (fov + z2 + 250);
                const px = cx + x1 * scale;
                const py = cy + y2 * scale;

                if (!started) {
                    ctx.moveTo(px, py);
                    started = true;
                } else {
                    ctx.lineTo(px, py);
                }
            }
            ctx.strokeStyle = 'rgba(200, 169, 110, 0.35)';
            ctx.lineWidth = 1.2;
            ctx.stroke();
        }

        // Sort particles by depth Z (back to front)
        projected.sort((a, b) => b.z - a.z);

        // Render particles with soft halo
        for (let i = 0; i < projected.length; i++) {
            const p = projected[i];
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fillStyle = p.color;
            ctx.shadowColor = p.glow;
            ctx.shadowBlur = 5;
            ctx.fill();
        }
        ctx.shadowBlur = 0; // reset
    }
}

window.RFOrbitalVisualizer = RFOrbitalVisualizer;
