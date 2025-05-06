// Main JavaScript file

document.addEventListener('DOMContentLoaded', function() {
    // Enable Bootstrap tooltips everywhere
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Enable Bootstrap popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Handle file input customization
    const fileInputs = document.querySelectorAll('.custom-file-input');
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const fileName = this.files[0].name;
            const label = this.nextElementSibling;
            label.textContent = fileName;
        });
    });

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
    const textareas = document.querySelectorAll('textarea[maxlength]');
    textareas.forEach(textarea => {
        const counter = document.createElement('small');
        counter.className = 'form-text text-muted character-counter';
        counter.innerHTML = `0/${textarea.maxLength} characters`;
        textarea.parentNode.appendChild(counter);

        textarea.addEventListener('input', function() {
            counter.innerHTML = `${this.value.length}/${this.maxLength} characters`;
        });
    });

    // Handle job application status updates
    const statusForm = document.getElementById('application-status-form');
    if (statusForm) {
        const statusSelect = document.getElementById('status-select');
        statusSelect.addEventListener('change', function() {
            statusForm.submit();
        });
    }

    // Date picker enhancement
    const datePickers = document.querySelectorAll('input[type="date"]');
    datePickers.forEach(picker => {
        // Add min attribute to prevent selecting dates in the past for closing dates
        if (picker.id === 'closing_date') {
            picker.min = new Date().toISOString().split('T')[0];
        }
    });
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
