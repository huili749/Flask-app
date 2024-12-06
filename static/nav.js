// static/scripts.js

document.addEventListener("DOMContentLoaded", function () {
    // Get the current page's pathname
    const currentPath = window.location.pathname;

    // Map paths to data-page values
    const pageMap = {
        "{{ url_for('home') }}": "generate",
        "{{ url_for('library') }}": "library",
        "{{ url_for('create') }}": "history",
    };

    // Get the corresponding page identifier
    const activePage = pageMap[currentPath];

    // Set the nav's data-active-page attribute
    if (activePage) {
        document.querySelector("nav").setAttribute("data-active-page", activePage);
    }
});
