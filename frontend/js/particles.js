/**
 * SPECTRA — Premium Particle Background System
 * Inspired by USTA 3D particle cloud aesthetic
 * Creates a starfield/particle constellation that subtly moves
 * with interconnected lines between nearby particles.
 */

(function () {
    'use strict';

    const canvas = document.getElementById('particle-bg');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    let W, H;
    let particles = [];
    let animId = null;
    let mouseX = -1000, mouseY = -1000;

    // Configuration
    const CONFIG = {
        particleCount: 120,
        maxSpeed: 0.15,
        connectionDistance: 140,
        mouseInfluenceRadius: 200,
        particleSizeMin: 0.5,
        particleSizeMax: 2.0,
        baseOpacity: 0.25,
        connectionOpacity: 0.06,
        colors: [
            { r: 200, g: 169, b: 110 },  // Gold
            { r: 168, g: 180, b: 200 },  // Silver
            { r: 124, g: 106, b: 239 },  // Violet
            { r: 78,  g: 205, b: 196 },  // Cyan
        ],
        // Orbiting cluster — a denser knot in the upper-right
        clusterCenter: { x: 0.75, y: 0.25 },
        clusterRadius: 200,
        clusterCount: 40,
    };

    function resize() {
        const dpr = window.devicePixelRatio || 1;
        W = window.innerWidth;
        H = window.innerHeight;
        canvas.width = W * dpr;
        canvas.height = H * dpr;
        canvas.style.width = W + 'px';
        canvas.style.height = H + 'px';
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }

    function createParticle(clustered = false) {
        const color = CONFIG.colors[Math.floor(Math.random() * CONFIG.colors.length)];
        let x, y;

        if (clustered) {
            // Gaussian distribution around the cluster center
            const angle = Math.random() * Math.PI * 2;
            const dist = Math.random() * CONFIG.clusterRadius * (0.3 + Math.random() * 0.7);
            x = CONFIG.clusterCenter.x * W + Math.cos(angle) * dist;
            y = CONFIG.clusterCenter.y * H + Math.sin(angle) * dist;
        } else {
            x = Math.random() * W;
            y = Math.random() * H;
        }

        return {
            x,
            y,
            vx: (Math.random() - 0.5) * CONFIG.maxSpeed * 2,
            vy: (Math.random() - 0.5) * CONFIG.maxSpeed * 2,
            size: CONFIG.particleSizeMin + Math.random() * (CONFIG.particleSizeMax - CONFIG.particleSizeMin),
            color,
            alpha: CONFIG.baseOpacity * (0.4 + Math.random() * 0.6),
            pulse: Math.random() * Math.PI * 2,
            pulseSpeed: 0.005 + Math.random() * 0.01,
            clustered,
        };
    }

    function init() {
        resize();
        particles = [];

        // Background scattered particles
        for (let i = 0; i < CONFIG.particleCount; i++) {
            particles.push(createParticle(false));
        }

        // Clustered particle knot (like the USTA signal burst)
        for (let i = 0; i < CONFIG.clusterCount; i++) {
            particles.push(createParticle(true));
        }

        // Mouse tracking
        document.addEventListener('mousemove', (e) => {
            mouseX = e.clientX;
            mouseY = e.clientY;
        });

        document.addEventListener('mouseleave', () => {
            mouseX = -1000;
            mouseY = -1000;
        });

        window.addEventListener('resize', () => {
            resize();
        });
    }

    function update() {
        for (let i = 0; i < particles.length; i++) {
            const p = particles[i];

            // Gentle drift
            p.x += p.vx;
            p.y += p.vy;

            // Pulse alpha
            p.pulse += p.pulseSpeed;
            const pulseFactor = 0.7 + 0.3 * Math.sin(p.pulse);

            // Mouse repulsion — very subtle
            const dx = p.x - mouseX;
            const dy = p.y - mouseY;
            const dist = Math.sqrt(dx * dx + dy * dy);
            if (dist < CONFIG.mouseInfluenceRadius && dist > 0) {
                const force = (1 - dist / CONFIG.mouseInfluenceRadius) * 0.3;
                p.vx += (dx / dist) * force;
                p.vy += (dy / dist) * force;
            }

            // Dampen velocity
            p.vx *= 0.998;
            p.vy *= 0.998;

            // Wrap around edges
            if (p.x < -20) p.x = W + 20;
            if (p.x > W + 20) p.x = -20;
            if (p.y < -20) p.y = H + 20;
            if (p.y > H + 20) p.y = -20;

            p._renderAlpha = p.alpha * pulseFactor;
        }
    }

    function draw() {
        ctx.clearRect(0, 0, W, H);

        // Draw connections
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const a = particles[i];
                const b = particles[j];
                const dx = a.x - b.x;
                const dy = a.y - b.y;
                const dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < CONFIG.connectionDistance) {
                    const opacity = CONFIG.connectionOpacity * (1 - dist / CONFIG.connectionDistance);
                    const avgColor = {
                        r: (a.color.r + b.color.r) / 2,
                        g: (a.color.g + b.color.g) / 2,
                        b: (a.color.b + b.color.b) / 2,
                    };
                    ctx.strokeStyle = `rgba(${avgColor.r}, ${avgColor.g}, ${avgColor.b}, ${opacity})`;
                    ctx.lineWidth = 0.5;
                    ctx.beginPath();
                    ctx.moveTo(a.x, a.y);
                    ctx.lineTo(b.x, b.y);
                    ctx.stroke();
                }
            }
        }

        // Draw particles
        for (let i = 0; i < particles.length; i++) {
            const p = particles[i];
            const { r, g, b } = p.color;

            // Soft glow halo
            if (p.size > 1.2) {
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.size * 3, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(${r}, ${g}, ${b}, ${p._renderAlpha * 0.15})`;
                ctx.fill();
            }

            // Core particle
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(${r}, ${g}, ${b}, ${p._renderAlpha})`;
            ctx.fill();
        }

        // Subtle vignette edges
        const vignetteGrad = ctx.createRadialGradient(
            W / 2, H / 2, Math.min(W, H) * 0.25,
            W / 2, H / 2, Math.max(W, H) * 0.8
        );
        vignetteGrad.addColorStop(0, 'rgba(0, 0, 0, 0)');
        vignetteGrad.addColorStop(1, 'rgba(0, 0, 0, 0.3)');
        ctx.fillStyle = vignetteGrad;
        ctx.fillRect(0, 0, W, H);
    }

    function loop() {
        update();
        draw();
        animId = requestAnimationFrame(loop);
    }

    init();
    loop();
})();
