// Main JavaScript for Student Management System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeTableFilters();
    initializeFormValidation();
    initializeDeleteConfirmation();
    initializeProgressTracking();
});

/**
 * Initialize table filtering functionality
 */
function initializeTableFilters() {
    const filterBtn = document.getElementById('filter-btn');
    if (filterBtn) {
        filterBtn.addEventListener('click', function() {
            const form = this.closest('form');
            form.submit();
        });
    }
}

/**
 * Initialize form validation
 */
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Check required fields
            const requiredFields = this.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.classList.add('border-red-500');
                    isValid = false;
                } else {
                    field.classList.remove('border-red-500');
                }
            });

            // Email validation
            const emailFields = this.querySelectorAll('input[type="email"]');
            emailFields.forEach(field => {
                const isValidEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(field.value);
                if (!isValidEmail && field.value) {
                    field.classList.add('border-red-500');
                    isValid = false;
                } else {
                    field.classList.remove('border-red-500');
                }
            });

            // Number validation for GPA and scores
            const numberFields = this.querySelectorAll('input[type="number"]');
            numberFields.forEach(field => {
                const value = parseFloat(field.value);
                const min = field.getAttribute('min');
                const max = field.getAttribute('max');
                
                if (min && value < min) {
                    field.classList.add('border-red-500');
                    isValid = false;
                } else if (max && value > max) {
                    field.classList.add('border-red-500');
                    isValid = false;
                } else {
                    field.classList.remove('border-red-500');
                }
            });

            if (!isValid) {
                e.preventDefault();
                showAlert('Please fill all required fields correctly', 'error');
            }
        });
    });
}

/**
 * Initialize delete confirmation dialogs
 */
function initializeDeleteConfirmation() {
    const deleteLinks = document.querySelectorAll('a[href*="delete"]');
    deleteLinks.forEach(link => {
        if (!link.href.includes('/delete/')) return;
        
        link.addEventListener('click', function(e) {
            // Allow the form submission in the confirmation page
            if (this.closest('form')) return;
            
            e.preventDefault();
            const confirmed = confirm('Are you sure you want to delete this item?');
            if (confirmed) {
                window.location.href = this.href;
            }
        });
    });
}

/**
 * Show alert messages
 */
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    let classes = 'p-4 mb-4 rounded-lg text-sm ';
    
    if (type === 'success') {
        classes += 'bg-green-100 text-green-800';
    } else if (type === 'error') {
        classes += 'bg-red-100 text-red-800';
    } else {
        classes += 'bg-blue-100 text-blue-800';
    }
    
    alertDiv.className = classes;
    alertDiv.textContent = message;
    
    const container = document.querySelector('.max-w-7xl');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
}

/**
 * Initialize progress tracking
 */
function initializeProgressTracking() {
    const studentLinks = document.querySelectorAll('a[data-student-id]');
    studentLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const studentId = this.getAttribute('data-student-id');
            loadStudentProgress(studentId);
        });
    });
}

/**
 * Load student progress via AJAX
 */
function loadStudentProgress(studentId) {
    fetch(`/api/student/${studentId}/progress/`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayProgress(data.progress_records);
            }
        })
        .catch(error => console.error('Error loading progress:', error));
}

/**
 * Display student progress information
 */
function displayProgress(progressRecords) {
    const container = document.getElementById('progress-container');
    if (!container) return;
    
    let html = '<h3 class="font-bold mb-4">Progress History</h3>';
    html += '<table class="w-full text-sm"><thead><tr><th class="text-left">Semester</th><th class="text-center">GPA</th><th class="text-center">Cumulative</th></tr></thead><tbody>';
    
    progressRecords.forEach(record => {
        html += `<tr><td>${record.semester} ${record.year}</td><td class="text-center">${record.semester_gpa}</td><td class="text-center">${record.cumulative_gpa}</td></tr>`;
    });
    
    html += '</tbody></table>';
    container.innerHTML = html;
}

/**
 * Calculate grade from score
 */
function calculateGrade(score) {
    if (score >= 90) return 'A';
    if (score >= 80) return 'B';
    if (score >= 70) return 'C';
    if (score >= 60) return 'D';
    return 'F';
}

/**
 * Export table to CSV
 */
function exportTableToCSV(filename) {
    const table = document.querySelector('table');
    if (!table) return;
    
    let csv = [];
    const rows = table.querySelectorAll('tr');
    
    rows.forEach(row => {
        const cols = row.querySelectorAll('td, th');
        let csvRow = [];
        cols.forEach(col => {
            csvRow.push('"' + col.innerText + '"');
        });
        csv.push(csvRow.join(','));
    });
    
    downloadCSV(csv.join('\n'), filename);
}

/**
 * Download CSV file
 */
function downloadCSV(csv, filename) {
    const csvFile = new Blob([csv], { type: 'text/csv' });
    const downloadLink = document.createElement('a');
    downloadLink.href = URL.createObjectURL(csvFile);
    downloadLink.download = filename;
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

/**
 * Search in table
 */
function searchTable(tableId, searchTerm) {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    const rows = table.querySelectorAll('tbody tr');
    rows.forEach(row => {
        const text = row.innerText.toLowerCase();
        if (text.includes(searchTerm.toLowerCase())) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

/**
 * Initialize real-time search
 */
document.addEventListener('DOMContentLoaded', function() {
    const searchInputs = document.querySelectorAll('[data-search-table]');
    searchInputs.forEach(input => {
        input.addEventListener('keyup', function() {
            const tableId = this.getAttribute('data-search-table');
            searchTable(tableId, this.value);
        });
    });
});
