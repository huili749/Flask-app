const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

// Set canvas dimensions
canvas.width = canvas.offsetWidth;
canvas.height = canvas.offsetHeight;

// Variables
const dots = [];
const numDots = 60;
let buffer = canvas.width * 0.15; // Dynamic influence area based on canvas size
const mouse = { x: null, y: null, active: false };

// Create grid of dots
const createDots = () => {
    const spacingX = canvas.width / numDots;
    const spacingY = canvas.height / numDots;

    for (let y = 0; y < numDots; y++) {
        for (let x = 0; x < numDots; x++) {
            dots.push({
                x: x * spacingX,
                y: y * spacingY,
                originalX: x * spacingX,
                originalY: y * spacingY,
                color: `hsl(${Math.random() * 360}, 80%, 50%)`,
            });
        }
    }
};

// Draw dots
const drawDots = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    dots.forEach((dot) => {
        ctx.beginPath();
        ctx.arc(dot.x, dot.y, 2, 0, Math.PI * 2);
        ctx.fillStyle = dot.color;
        ctx.fill();
    });
};

// Animate dots
const animateDots = () => {
    dots.forEach((dot) => {
        const dx = dot.x - mouse.x;
        const dy = dot.y - mouse.y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (mouse.active && distance < buffer) {
            const factor = (buffer - distance) / buffer;
            dot.x -= dx * 0.02 * factor;
            dot.y -= dy * 0.02 * factor;
            dot.color = `hsl(${Math.random() * 360}, 80%, 60%)`;
        } else {
            dot.x += (dot.originalX - dot.x) * 0.02;
            dot.y += (dot.originalY - dot.y) * 0.02;
        }
    });
};

// Update animation frame
const update = () => {
    drawDots();
    animateDots();
    requestAnimationFrame(update);
};

// Track mouse movement inside canvas
const canvasWrapper = document.querySelector('.canvas-wrapper');
canvasWrapper.addEventListener('mousemove', (e) => {
    const rect = canvas.getBoundingClientRect();
    mouse.x = e.clientX - rect.left;
    mouse.y = e.clientY - rect.top;
    mouse.active = true;
});

canvasWrapper.addEventListener('mouseleave', () => {
    mouse.active = false;
});

// Adjust buffer on resize
window.addEventListener('resize', () => {
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
    buffer = canvas.width * 0.15; 
    dots.length = 0; 
    createDots();
});

// Initialize
createDots();
update();
