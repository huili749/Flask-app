const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

// Set canvas dimensions
canvas.width = canvas.offsetWidth;
canvas.height = canvas.offsetHeight;

const dots = [];
const numDots = 60; // Increase density by increasing the grid size
const dotRadius = 2; // Make dots larger
const mouse = { x: null, y: null };

// Create a grid of dots
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

// Draw dots on the canvas
const drawDots = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    dots.forEach((dot) => {
        ctx.beginPath();
        ctx.arc(dot.x, dot.y, dotRadius, 0, Math.PI * 2);
        ctx.fillStyle = dot.color;
        ctx.fill();
    });
};

// Animate dots toward the cursor
const animateDots = () => {
    dots.forEach((dot) => {
        const dx = dot.x - mouse.x;
        const dy = dot.y - mouse.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        const buffer = 150; // Area of influence

        if (distance < buffer) {
            const factor = (buffer - distance) / buffer; // Closer dots move more
            dot.x -= dx * 0.02 * factor; // Smooth movement
            dot.y -= dy * 0.02 * factor;
            dot.color = `hsl(${Math.random() * 360}, 80%, 60%)`; // Brighter on hover
        } else {
            // Smoothly return to original position
            dot.x += (dot.originalX - dot.x) * 0.02;
            dot.y += (dot.originalY - dot.y) * 0.02;
        }
    });
};

// Update the animation frame
const update = () => {
    drawDots();
    animateDots();
    requestAnimationFrame(update);
};

// Track mouse movement
canvas.addEventListener('mousemove', (e) => {
    const rect = canvas.getBoundingClientRect();
    mouse.x = e.clientX - rect.left;
    mouse.y = e.clientY - rect.top;
});

// Handle window resize
window.addEventListener('resize', () => {
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
    dots.length = 0; // Clear and recreate dots
    createDots();
});

// Initialize
createDots();
update();
