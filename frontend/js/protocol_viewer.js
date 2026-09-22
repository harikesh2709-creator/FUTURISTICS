/**
 * Protocol Viewer — Bitstream correlation chart and hex dump renderer.
 * Premium dark aesthetic with gold/cyan traces.
 */

class ProtocolViewer {
    constructor(corrCanvasId) {
        this.corrCanvas = document.getElementById(corrCanvasId);
        this.corrCtx = this.corrCanvas.getContext('2d');
    }

    resizeCorr() {
        const rect = this.corrCanvas.parentElement.getBoundingClientRect();
        this.corrCanvas.width = rect.width;
        this.corrCanvas.height = Math.max(100, rect.height - 30);
    }

    renderCorrelation(correlation, positions, threshold) {
        if (!correlation || correlation.length === 0) return;
        this.resizeCorr();

        const ctx = this.corrCtx;
        const W = this.corrCanvas.width;
        const H = this.corrCanvas.height;

        // Background
        ctx.fillStyle = '#030306';
        ctx.fillRect(0, 0, W, H);

        const N = correlation.length;
        const maxCorr = Math.max(...correlation, 0.1);

        // Grid
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.03)';
        ctx.lineWidth = 0.5;
        for (let v = 0; v <= 1; v += 0.25) {
            const y = H - v / maxCorr * (H - 20) - 10;
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(W, y);
            ctx.stroke();
        }

        // Correlation trace — cyan
        ctx.strokeStyle = 'rgba(78, 205, 196, 0.8)';
        ctx.lineWidth = 1.2;
        ctx.shadowColor = 'rgba(78, 205, 196, 0.3)';
        ctx.shadowBlur = 4;
        ctx.beginPath();
        for (let i = 0; i < N; i++) {
            const x = (i / N) * W;
            const y = H - (correlation[i] / maxCorr) * (H - 20) - 10;
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        }
        ctx.stroke();
        ctx.shadowBlur = 0;

        // Detection markers — gold
        if (positions && positions.length > 0) {
            ctx.fillStyle = 'rgba(200, 169, 110, 0.9)';
            ctx.shadowColor = 'rgba(200, 169, 110, 0.4)';
            ctx.shadowBlur = 6;
            for (const pos of positions) {
                const x = (pos / (N * (correlation.length > 1 ? 1 : 1))) * W;
                if (x >= 0 && x <= W) {
                    ctx.beginPath();
                    ctx.arc(x, 10, 4, 0, 2 * Math.PI);
                    ctx.fill();
                }
            }
            ctx.shadowBlur = 0;
        }

        // Threshold line
        if (threshold !== undefined) {
            const threshVal = 1 - threshold / 32;
            const ty = H - (threshVal / maxCorr) * (H - 20) - 10;
            ctx.strokeStyle = 'rgba(239, 68, 68, 0.35)';
            ctx.setLineDash([4, 4]);
            ctx.beginPath();
            ctx.moveTo(0, ty);
            ctx.lineTo(W, ty);
            ctx.stroke();
            ctx.setLineDash([]);
        }

        // Labels
        ctx.fillStyle = 'rgba(142, 149, 169, 0.5)';
        ctx.font = '9px "JetBrains Mono"';
        ctx.fillText('CORRELATION', 4, 12);
        ctx.fillText(`${N} samples`, W - 80, 12);
    }

    renderFrameTable(frames, tbodyId) {
        const tbody = document.getElementById(tbodyId);
        tbody.innerHTML = '';

        if (!frames || frames.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;color:var(--text-muted)">No frames detected</td></tr>';
            return;
        }

        for (const frame of frames) {
            const tr = document.createElement('tr');
            const payloadPreview = frame.payload_hex ? frame.payload_hex.substring(0, 40) + (frame.payload_hex.length > 40 ? '…' : '') : '—';
            let crcCell = '—';
            if (frame.crc_valid === true) crcCell = '<span class="crc-pass">✓ PASS</span>';
            else if (frame.crc_valid === false) crcCell = '<span class="crc-fail">✗ FAIL</span>';

            tr.innerHTML = `
                <td>${frame.frame_num}</td>
                <td>${frame.bit_position}</td>
                <td style="color:var(--accent-gold)">${frame.sync_hex}</td>
                <td>${payloadPreview}</td>
                <td>${crcCell}</td>
                <td>${frame.entropy}</td>
            `;
            tbody.appendChild(tr);
        }
    }

    renderDepthSearchChart(depthScores, bestDepth, canvasId = 'depth-search-canvas') {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        const rect = canvas.parentElement.getBoundingClientRect();
        canvas.width = rect.width;
        canvas.height = Math.max(120, rect.height - 20);

        const W = canvas.width;
        const H = canvas.height;

        ctx.fillStyle = '#030306';
        ctx.fillRect(0, 0, W, H);

        if (!depthScores || depthScores.length === 0) {
            ctx.fillStyle = 'rgba(142, 149, 169, 0.3)';
            ctx.font = '11px "Outfit"';
            ctx.textAlign = 'center';
            ctx.fillText('No depth search telemetry available. Run blind de-interleaver search.', W / 2, H / 2);
            ctx.textAlign = 'start';
            return;
        }

        const pad = { left: 45, right: 20, top: 25, bottom: 25 };
        const plotW = W - pad.left - pad.right;
        const plotH = H - pad.top - pad.bottom;

        // Axes & Grid
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.03)';
        ctx.lineWidth = 0.5;
        ctx.fillStyle = 'rgba(142, 149, 169, 0.5)';
        ctx.font = '9px "JetBrains Mono"';

        for (let v = 0; v <= 0.5; v += 0.1) {
            const y = pad.top + plotH * (1 - v / 0.5);
            ctx.beginPath();
            ctx.moveTo(pad.left, y);
            ctx.lineTo(W - pad.right, y);
            ctx.stroke();
            ctx.fillText(v.toFixed(2), 6, y + 3);
        }

        // Title & Legend
        ctx.fillStyle = 'rgba(200, 169, 110, 0.8)';
        ctx.font = '9px "JetBrains Mono"';
        ctx.fillText(`HYPOTHESIS DEPTH SEARCH · BEST DEPTH = ${bestDepth}`, pad.left, 14);

        const nBars = depthScores.length;
        const barW = Math.max(8, (plotW / nBars) * 0.65);
        const barGap = plotW / nBars;

        depthScores.forEach((item, idx) => {
            const x = pad.left + idx * barGap + (barGap - barW) / 2;
            const score = Math.min(0.5, Math.max(0, item.score));
            const barH = (score / 0.5) * plotH;
            const y = pad.top + plotH - barH;

            const isBest = item.depth === bestDepth;

            // Bar fill
            if (isBest) {
                ctx.fillStyle = 'rgba(16, 185, 129, 0.8)';
                ctx.shadowColor = 'rgba(16, 185, 129, 0.4)';
                ctx.shadowBlur = 8;
            } else {
                ctx.fillStyle = item.score > 0.2 ? 'rgba(239, 68, 68, 0.4)' : 'rgba(200, 169, 110, 0.3)';
                ctx.shadowBlur = 0;
            }

            // Rounded top bars
            const radius = 3;
            ctx.beginPath();
            ctx.moveTo(x + radius, y);
            ctx.lineTo(x + barW - radius, y);
            ctx.quadraticCurveTo(x + barW, y, x + barW, y + radius);
            ctx.lineTo(x + barW, y + Math.max(3, barH));
            ctx.lineTo(x, y + Math.max(3, barH));
            ctx.lineTo(x, y + radius);
            ctx.quadraticCurveTo(x, y, x + radius, y);
            ctx.closePath();
            ctx.fill();
            ctx.shadowBlur = 0;

            // X-axis label
            ctx.fillStyle = isBest ? 'rgba(16, 185, 129, 0.9)' : 'rgba(142, 149, 169, 0.6)';
            ctx.font = isBest ? 'bold 9px "JetBrains Mono"' : '8px "JetBrains Mono"';
            ctx.textAlign = 'center';
            ctx.fillText(`d=${item.depth}`, x + barW / 2, H - 8);

            // Value label
            if (isBest || item.score < 0.05) {
                ctx.fillText(item.score.toFixed(3), x + barW / 2, y - 5);
            }
            ctx.textAlign = 'start';
        });
    }

    renderHexDump(hexData, containerId) {
        const container = document.getElementById(containerId);
        if (!hexData || !hexData.lines || hexData.lines.length === 0) {
            container.textContent = 'No bitstream data available.';
            return;
        }
        container.textContent = hexData.lines.join('\n');
    }
}

window.ProtocolViewer = ProtocolViewer;
