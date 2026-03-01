// ============================================
// QURAN ONLINE — Main JavaScript
// ============================================

document.addEventListener('DOMContentLoaded', function() {

    // --- Mobile Navigation Toggle ---
    const navToggle = document.getElementById('navToggle');
    const navLinks = document.getElementById('navLinks');

    if (navToggle && navLinks) {
        navToggle.addEventListener('click', function() {
            navLinks.classList.toggle('show');
            const icon = this.querySelector('i');
            if (navLinks.classList.contains('show')) {
                icon.className = 'fas fa-times';
            } else {
                icon.className = 'fas fa-bars';
            }
        });

        // Close menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!navToggle.contains(e.target) && !navLinks.contains(e.target)) {
                navLinks.classList.remove('show');
                const icon = navToggle.querySelector('i');
                icon.className = 'fas fa-bars';
            }
        });
    }

    // --- Smooth scroll to top on page load ---
    window.scrollTo(0, 0);
});
