document.addEventListener("DOMContentLoaded", () => {
    // Upload Button
    const uploadButton = document.getElementById("upload-button");
    const fileInput = document.getElementById("file-input");

    uploadButton.addEventListener("click", () => {
        fileInput.click();
    });

    fileInput.addEventListener("change", (event) => {
        if (event.target.files.length > 0) {
            uploadButton.innerText = `File: ${event.target.files[0].name}`;
        }
    });

    // Dropdown Menu
    const numberButton = document.getElementById("number-button");
    const dropdownMenu = document.getElementById("dropdown-menu");
    const colorCountInput = document.getElementById("color-count");

    numberButton.addEventListener("click", () => {
        dropdownMenu.parentElement.classList.toggle("active");
    });

    dropdownMenu.addEventListener("click", (event) => {
        if (event.target.dataset.value) {
            const selectedValue = event.target.dataset.value;
            colorCountInput.value = selectedValue;
            numberButton.innerText = `Number: ${selectedValue}`;
            dropdownMenu.parentElement.classList.remove("active");
        }
    });

    // Event Delegation for Color Adjustments
    const colorRow = document.querySelector('.color-row');
    if (colorRow) {
        colorRow.addEventListener("click", (event) => {
            const colorItem = event.target.closest('.color-item');

            // Adjust Color
            if (event.target.closest('.adjust-btn')) {
                const picker = colorItem.querySelector('.color-picker');

                // Dynamically position the picker
                const iconRect = event.target.getBoundingClientRect();
                picker.style.position = "absolute";
                picker.style.left = `${iconRect.left}px`;
                picker.style.top = `${iconRect.bottom + window.scrollY}px`;
                picker.style.display = "block";

                // Focus and open the color picker
                picker.focus();

                // Hide picker on outside click
                const hidePicker = (e) => {
                    if (!colorItem.contains(e.target)) {
                        picker.style.display = "none";
                        document.removeEventListener("click", hidePicker);
                    }
                };
                document.addEventListener("click", hidePicker);
            }

            // 📋 Copy Color Code
            if (event.target.closest('.copy-btn')) {
                const colorCode = colorItem.querySelector('.color-code').textContent;
                if (colorCode) {
                    navigator.clipboard.writeText(colorCode).then(() => {
                        // Optionally show feedback
                        const icon = event.target.closest('.copy-btn').querySelector('i'); 
                        if (icon) {
                            icon.className = "fa-solid fa-check"; 
                            setTimeout(() => {
                                icon.className = "fa-regular fa-copy"; 
                            }, 1500);
                        }
                    }).catch(err => {
                        console.error("Failed to copy color code:", err);
                    });
                }
            }

            // Move Left
            if (event.target.classList.contains('left-arrow') && colorItem) {
                const previousSibling = colorItem.previousElementSibling;
                if (previousSibling) {
                    colorRow.insertBefore(colorItem, previousSibling);
                }
            }

            // Move Right
            if (event.target.classList.contains('right-arrow') && colorItem) {
                const nextSibling = colorItem.nextElementSibling;
                if (nextSibling) {
                    colorRow.insertBefore(nextSibling, colorItem);
                }
            }
        });
    }

    // Update Color from Color Picker
    document.querySelectorAll('.color-picker').forEach(picker => {
        picker.addEventListener('input', (event) => {
            const colorItem = event.target.closest('.color-item');
            if (colorItem) {
                const colorBlock = colorItem.querySelector('.color-block');
                const colorCode = colorItem.querySelector('.color-code');
                if (colorBlock && colorCode) {
                    const newColor = event.target.value;
                    colorBlock.style.backgroundColor = newColor;
                    colorCode.textContent = newColor;
                }
            }
        });
    });

    // Download Color Palette as Image
    const downloadButton = document.getElementById("download-button");
    downloadButton.addEventListener("click", () => {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');

        // Get all color codes
        const colors = Array.from(document.querySelectorAll('.color-code')).map(code => code.textContent);

        // Define canvas dimensions
        const blockWidth = 1000; // Width of each color block
        const blockHeight = 500; // Height of the color blocks
        canvas.width = colors.length * blockWidth;
        canvas.height = blockHeight;

        // Draw each color block
        colors.forEach((color, index) => {
            ctx.fillStyle = color;
            ctx.fillRect(index * blockWidth, 0, blockWidth, blockHeight);
        });

        // Convert canvas to an image and trigger download
        const link = document.createElement('a');
        link.download = 'color-palette.png';
        link.href = canvas.toDataURL('image/png');
        link.click();
    });

    // Save Palette to Library
    const saveLibraryButton = document.getElementById("save-library-button");
    const saveModal = document.getElementById("save-modal");
    const closeModal = document.getElementById("close-modal");
    const saveCategoryButton = document.getElementById("save-category");
    const saveLibraryForm = document.getElementById("save-library-form");

    saveLibraryButton.addEventListener("click", () => {
        // Show the modal for selecting/creating a category
        saveModal.style.display = "flex";
    });

    closeModal.addEventListener("click", () => {
        // Close the modal
        saveModal.style.display = "none";
    });

    saveCategoryButton.addEventListener("click", () => {
        const categorySelect = document.getElementById("category-select");
        const newCategoryInput = document.getElementById("new-category");

        // Get the selected or newly created category
        const selectedCategory = categorySelect.value.trim();
        const newCategory = newCategoryInput.value.trim();

        if (!selectedCategory && !newCategory) {
            alert("Please select or create a category.");
            return;
        }

        // Get all color codes
        const colorElements = document.querySelectorAll('.color-code');
        const colors = Array.from(colorElements).map(el => el.textContent.trim());

        if (colors.length === 0) {
            alert("No colors found to save.");
            return;
        }

        // Remove any previously appended hidden inputs
        saveLibraryForm.querySelectorAll('input[type="hidden"]').forEach(input => input.remove());

        // Add the category and colors to the form
        const categoryInput = document.createElement("input");
        categoryInput.type = "hidden";
        categoryInput.name = "new_category";
        categoryInput.value = newCategory || "";

        const selectedCategoryInput = document.createElement("input");
        selectedCategoryInput.type = "hidden";
        selectedCategoryInput.name = "category";
        selectedCategoryInput.value = selectedCategory || "";

        const colorsInput = document.createElement("input");
        colorsInput.type = "hidden";
        colorsInput.name = "colors";
        colorsInput.value = JSON.stringify(colors);

        saveLibraryForm.appendChild(categoryInput);
        saveLibraryForm.appendChild(selectedCategoryInput);
        saveLibraryForm.appendChild(colorsInput);

        console.log("Submitting form with data:", {
            newCategory: newCategory,
            selectedCategory: selectedCategory,
            colors: colors
        });

        // Submit the form
        saveLibraryForm.submit();
    });
    
});
