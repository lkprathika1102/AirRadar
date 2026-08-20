const canvas = document.getElementById('radar-canvas');
const ctx = canvas.getContext('2d');
let width, height, centerX, centerY;

const RING_COUNT = 4;
const RING_COLOR = '#222';
const ACCENT_COLOR = '#00ff41';

function resize() {
    width = window.innerWidth > 800 ? 600 : window.innerWidth * 0.8;
    height = width;
    canvas.width = width;
    canvas.height = height;
    centerX = width / 2;
    centerY = height / 2;
    drawGrid();
}

function drawGrid() {
    ctx.clearRect(0, 0, width, height);
    
    const maxRadius = width * 0.45;
    const step = maxRadius / RING_COUNT;

    ctx.strokeStyle = RING_COLOR;
    ctx.lineWidth = 1;

    for (let i = 1; i <= RING_COUNT; i++) {
        ctx.beginPath();
        ctx.arc(centerX, centerY, step * i, 0, Math.PI * 2);
        ctx.stroke();
    }

    ctx.strokeStyle = RING_COLOR;
    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.lineTo(centerX, centerY - maxRadius);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.lineTo(centerX + maxRadius, centerY);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.lineTo(centerX, centerY + maxRadius);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.lineTo(centerX - maxRadius, centerY);
    ctx.stroke();

    ctx.fillStyle = ACCENT_COLOR;
    ctx.beginPath();
    ctx.arc(centerX, centerY, 4, 0, Math.PI * 2);
    ctx.fill();
}

window.addEventListener('resize', resize);
resize();