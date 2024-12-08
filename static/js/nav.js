document.addEventListener("DOMContentLoaded", () => {
    // Highlight the active page
    const navLinks = document.querySelectorAll("nav ul li a");
    navLinks.forEach(link => {
        if (link.getAttribute("href") === window.location.pathname) {
            link.classList.add("active");
        }
    });

    // Show username dropdown (optional)
    const userInfo = document.querySelector(".user-info");
    if (userInfo) {
        userInfo.addEventListener("click", () => {
            alert("User menu can be implemented here (optional).");
        });
    }; 
});