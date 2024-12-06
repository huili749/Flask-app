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

            // 🎨 Adjust Color
            if (event.target.classList.contains('adjust-btn') && colorItem) {
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
});
