document.addEventListener("DOMContentLoaded", () => {
    const categoriesGrid = document.querySelector(".categories-grid");
    if (!categoriesGrid) {
        console.error("categories-grid element not found!");
        return;
    }

    categoriesGrid.addEventListener("click", (event) => {
        console.log("Click detected on:", event.target);

        // Download Palette
        if (event.target.closest(".download-icon")) {
            const paletteId = event.target.closest("button").dataset.paletteId;
            console.log("Download clicked for paletteId:", paletteId);

            fetch(`/palette/${paletteId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.image_path) {
                        const link = document.createElement('a');
                        link.href = data.image_path;
                        link.download = data.image_path.split('/').pop();
                        link.click();
                    } else {
                        console.error("No image path found for palette.");
                    }
                })
                .catch(err => {
                    console.error("Error fetching palette details:", err);
                });
        }

        // Delete Palette
        if (event.target.closest(".delete-icon")) {
            const paletteId = event.target.closest("button").dataset.paletteId;
            console.log("Delete clicked for paletteId:", paletteId);

            if (confirm("Are you sure you want to delete this palette?")) {
                fetch(`/delete_palette/${paletteId}`, { method: "DELETE" })
                    .then((response) => {
                        if (response.ok) {
                            event.target.closest(".category-item").remove();
                        } else {
                            alert("Failed to delete palette.");
                        }
                    })
                    .catch((err) => {
                        console.error("Error deleting palette:", err);
                    });
            }
        }
    });
    
});
