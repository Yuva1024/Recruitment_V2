// Main JavaScript file

document.addEventListener('DOMContentLoaded', function() {
    // Enable Bootstrap tooltips everywhere
    try {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        if (tooltipTriggerList.length > 0 && typeof bootstrap !== 'undefined') {
            tooltipTriggerList.map(function (tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl);
            });
        }
    } catch (error) {
        console.log('Tooltip initialization skipped:', error);
    }

    // Enable Bootstrap popovers
    try {
        const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
        if (popoverTriggerList.length > 0 && typeof bootstrap !== 'undefined') {
            popoverTriggerList.map(function (popoverTriggerEl) {
                return new bootstrap.Popover(popoverTriggerEl);
            });
        }
    } catch (error) {
        console.log('Popover initialization skipped:', error);
    }

    // Handle file input customization
    try {
        const fileInputs = document.querySelectorAll('.custom-file-input');
        if (fileInputs.length > 0) {
            fileInputs.forEach(input => {
                input.addEventListener('change', function(e) {
                    if (this.files && this.files.length > 0) {
                        const fileName = this.files[0].name;
                        const label = this.nextElementSibling;
                        if (label) {
                            label.textContent = fileName;
                        }
                    }
                });
            });
        }
    } catch (error) {
        console.log('File input handling skipped:', error);
    }

    // Password strength meter
    const passwordInput = document.getElementById('password');
    const meterBar = document.getElementById('password-strength-meter');
    const strengthText = document.getElementById('password-strength-text');

    if (passwordInput && meterBar && strengthText) {
        passwordInput.addEventListener('input', function() {
            const val = passwordInput.value;
            const result = calculatePasswordStrength(val);
            
            // Update the meter
            meterBar.value = result.score;
            
            // Update the text indicator
            if (val !== "") {
                strengthText.textContent = "Password strength: " + result.message;
            } else {
                strengthText.textContent = "";
            }
        });
    }

    // Filter form handling for job listings
    const jobFilterForm = document.getElementById('job-filter-form');
    if (jobFilterForm) {
        // Handle form submission
        jobFilterForm.addEventListener('submit', function(e) {
            // Remove empty fields to keep the URL clean
            const formElements = jobFilterForm.elements;
            for (let i = 0; i < formElements.length; i++) {
                if (formElements[i].value === "" && formElements[i].name !== "" && formElements[i].type !== "submit") {
                    formElements[i].disabled = true;
                }
            }
        });
    }

    // Character counter for textareas
    try {
        const textareas = document.querySelectorAll('textarea[maxlength]');
        if (textareas.length > 0) {
            textareas.forEach(textarea => {
                if (textarea && textarea.parentNode) {
                    const counter = document.createElement('small');
                    counter.className = 'form-text text-muted character-counter';
                    counter.innerHTML = `0/${textarea.maxLength || 0} characters`;
                    textarea.parentNode.appendChild(counter);

                    textarea.addEventListener('input', function() {
                        counter.innerHTML = `${this.value.length}/${this.maxLength || 0} characters`;
                    });
                }
            });
        }
    } catch (error) {
        console.log('Textarea character counter skipped:', error);
    }

    // Handle job application status updates
    try {
        const statusForm = document.getElementById('application-status-form');
        if (statusForm) {
            const statusSelect = document.getElementById('status-select');
            if (statusSelect) {
                statusSelect.addEventListener('change', function() {
                    statusForm.submit();
                });
            }
        }
    } catch (error) {
        console.log('Status form handling skipped:', error);
    }

    // Date picker enhancement
    try {
        const datePickers = document.querySelectorAll('input[type="date"]');
        if (datePickers.length > 0) {
            datePickers.forEach(picker => {
                // Add min attribute to prevent selecting dates in the past for closing dates
                if (picker && picker.id === 'closing_date') {
                    picker.min = new Date().toISOString().split('T')[0];
                }
            });
        }
    } catch (error) {
        console.log('Date picker handling skipped:', error);
    }
});

// Function to calculate password strength
function calculatePasswordStrength(password) {
    // Implement a simple password strength calculation
    let score = 0;
    let message = '';

    if (password.length > 7) score++;
    if (password.length > 10) score++;
    if (/[A-Z]/.test(password)) score++;
    if (/[0-9]/.test(password)) score++;
    if (/[^A-Za-z0-9]/.test(password)) score++;

    switch (score) {
        case 0:
        case 1:
            message = 'Very Weak';
            break;
        case 2:
            message = 'Weak';
            break;
        case 3:
            message = 'Medium';
            break;
        case 4:
            message = 'Strong';
            break;
        case 5:
            message = 'Very Strong';
            break;
    }

    return {
        score: score,
        message: message
    };
}

// Confirm deletion
function confirmDelete(event, itemName) {
    if (!confirm(`Are you sure you want to delete this ${itemName}? This action cannot be undone.`)) {
        event.preventDefault();
        return false;
    }
    return true;
}
