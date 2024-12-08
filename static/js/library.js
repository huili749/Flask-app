document.addEventListener("DOMContentLoaded", () => {
    const addCategoryButton = document.getElementById("add-category");
    const saveModal = document.getElementById("save-modal");
    const closeModalButton = document.getElementById("close-modal");
    const saveCategoryButton = document.getElementById("save-category");
    const categorySelect = document.getElementById("category-select");
    const newCategoryInput = document.getElementById("new-category");

    // Open the modal when "Add Category" is clicked
    addCategoryButton.addEventListener("click", () => {
        saveModal.style.display = "flex";
        newCategoryInput.value = ""; // Clear any previous input
    });

    // Close the modal when "Cancel" is clicked
    closeModalButton.addEventListener("click", () => {
        saveModal.style.display = "none";
    });

    // Save category logic
    saveCategoryButton.addEventListener("click", () => {
        const newCategory = newCategoryInput.value.trim();

        if (!newCategory) {
            alert("Please enter a category name.");
            return;
        }

        // Send the data to the server
        fetch("/save_category", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                new_category: newCategory, // Pass the new category name
            }),
        })
            .then((response) => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error("Failed to save category.");
                }
            })
            .then((data) => {
                alert(data.message || "Category saved successfully!");
                saveModal.style.display = "none";

                // Optionally reload the page to show the new category
                window.location.reload();
            })
            .catch((error) => {
                console.error("Error:", error);
            });
    });

    const editModal = document.getElementById("edit-modal");
    const editCategoryNameInput = document.getElementById("edit-category-name");
    const saveEditButton = document.getElementById("save-edit");
    const closeEditModalButton = document.getElementById("close-edit-modal");

    let currentCategoryId = null;

    // Open the edit modal
    document.querySelectorAll(".edit-category-button").forEach((button) => {
        button.addEventListener("click", (event) => {
            const categoryItem = event.target.closest(".library-item");
            currentCategoryId = categoryItem.dataset.categoryId;
            const currentCategoryName = categoryItem.querySelector(".category-name").textContent;
            editCategoryNameInput.value = currentCategoryName;
            editModal.style.display = "flex";
        });
    });

    // Close the modal
    closeEditModalButton.addEventListener("click", () => {
        editModal.style.display = "none";
    });

    // Save the updated category name
    saveEditButton.addEventListener("click", () => {
        const newCategoryName = editCategoryNameInput.value.trim();
        if (newCategoryName === "") {
            alert("Category name cannot be empty!");
            return;
        }

        fetch(`/update_category/${currentCategoryId}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ name: newCategoryName }),
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    // Update the category name in the UI
                    document.querySelector(
                        `.library-item[data-category-id="${currentCategoryId}"] .category-name`
                    ).textContent = newCategoryName;
                    editModal.style.display = "none";
                } else {
                    alert("Failed to update category name.");
                }
            })
            .catch((err) => {
                console.error("Error updating category name:", err);
            });
    });
});
