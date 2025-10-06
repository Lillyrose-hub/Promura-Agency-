// Sidebar Toggle Functionality
document.addEventListener('DOMContentLoaded', function() {
    // Get or create toggle button
    const sidebar = document.querySelector('.sidebar-nav');
    const container = document.querySelector('.container.with-sidebar');

    // Create toggle button if it doesn't exist
    let toggleBtn = document.getElementById('sidebarToggle');
    if (!toggleBtn && sidebar) {
        toggleBtn = createToggleButton();
    }

    // Load saved sidebar state from localStorage
    const savedState = localStorage.getItem('sidebarState');
    if (savedState === 'collapsed') {
        collapseSidebar();
    }

    // Create the toggle button
    function createToggleButton() {
        const button = document.createElement('button');
        button.id = 'sidebarToggle';
        button.className = 'sidebar-toggle-btn';
        button.innerHTML = `
            <svg class="toggle-icon close" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="15 18 9 12 15 6"></polyline>
            </svg>
            <svg class="toggle-icon open" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
        `;

        // Insert button in body (not inside sidebar)
        document.body.appendChild(button);

        // Add click event
        button.addEventListener('click', toggleSidebar);

        return button;
    }

    // Toggle sidebar function
    function toggleSidebar() {
        if (sidebar.classList.contains('collapsed')) {
            expandSidebar();
        } else {
            collapseSidebar();
        }
    }

    // Collapse sidebar
    function collapseSidebar() {
        if (!sidebar) return;

        sidebar.classList.add('collapsed');
        if (container) {
            container.classList.add('sidebar-collapsed');
        }

        // Save state
        localStorage.setItem('sidebarState', 'collapsed');

        // Update toggle button
        if (toggleBtn) {
            toggleBtn.classList.add('collapsed');
        }
    }

    // Expand sidebar
    function expandSidebar() {
        if (!sidebar) return;

        sidebar.classList.remove('collapsed');
        if (container) {
            container.classList.remove('sidebar-collapsed');
        }

        // Save state
        localStorage.setItem('sidebarState', 'expanded');

        // Update toggle button
        if (toggleBtn) {
            toggleBtn.classList.remove('collapsed');
        }
    }

    // Mobile menu toggle
    let mobileToggle = document.getElementById('mobileMenuToggle');
    if (!mobileToggle && window.innerWidth <= 768) {
        mobileToggle = createMobileToggle();
    }

    function createMobileToggle() {
        const button = document.createElement('button');
        button.id = 'mobileMenuToggle';
        button.className = 'mobile-menu-toggle';
        button.innerHTML = `
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="3" y1="12" x2="21" y2="12"></line>
                <line x1="3" y1="6" x2="21" y2="6"></line>
                <line x1="3" y1="18" x2="21" y2="18"></line>
            </svg>
        `;

        document.body.appendChild(button);

        button.addEventListener('click', function() {
            sidebar.classList.toggle('mobile-open');
            button.classList.toggle('active');
        });

        return button;
    }

    // Close mobile menu when clicking outside
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 768 && sidebar) {
            if (!sidebar.contains(e.target) && !mobileToggle?.contains(e.target)) {
                sidebar.classList.remove('mobile-open');
                if (mobileToggle) {
                    mobileToggle.classList.remove('active');
                }
            }
        }
    });

    // Handle window resize
    let resizeTimeout;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(function() {
            if (window.innerWidth > 768) {
                // Remove mobile classes on desktop
                sidebar?.classList.remove('mobile-open');
                mobileToggle?.classList.remove('active');
            }
        }, 250);
    });
});