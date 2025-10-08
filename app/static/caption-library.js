// Caption Library JavaScript Functionality
document.addEventListener('DOMContentLoaded', function() {
    // Global variables
    let allCaptions = [];
    let filteredCaptions = [];
    let activeCategory = 'All Categories';
    let captionStats = {};

    // Elements
    const uploadZone = document.getElementById('uploadZone');
    const excelUpload = document.getElementById('excelUpload');
    const uploadStatus = document.getElementById('uploadStatus');
    const categoryFilters = document.getElementById('categoryFilters');
    const captionSearch = document.getElementById('captionSearch');
    const messagesGrid = document.getElementById('messagesGrid');
    const captionCount = document.getElementById('captionCount');
    const copyToast = document.getElementById('copyToast');

    // Initialize
    loadCaptions();
    loadStats();
    setupEventListeners();

    // Load captions from API
    async function loadCaptions() {
        try {
            const response = await fetch('/api/captions');
            const captions = await response.json();
            allCaptions = captions;
            filteredCaptions = captions;

            // Update category filters with actual categories
            updateCategoryFilters();
            renderCaptions();
        } catch (error) {
            console.error('Error loading captions:', error);
        }
    }

    // Load statistics
    async function loadStats() {
        try {
            const response = await fetch('/api/captions/stats');
            captionStats = await response.json();
        } catch (error) {
            console.error('Error loading stats:', error);
        }
    }

    // Setup all event listeners
    function setupEventListeners() {
        // Upload zone click
        uploadZone.addEventListener('click', () => {
            excelUpload.click();
        });

        // File upload
        excelUpload.addEventListener('change', handleFileUpload);

        // Drag and drop
        uploadZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadZone.classList.add('dragging');
        });

        uploadZone.addEventListener('dragleave', () => {
            uploadZone.classList.remove('dragging');
        });

        uploadZone.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadZone.classList.remove('dragging');

            const files = e.dataTransfer.files;
            if (files.length > 0 && isExcelFile(files[0])) {
                handleFileUpload({ target: { files: files } });
            } else {
                showStatus('error', 'Please upload an Excel file (.xlsx or .xls)');
            }
        });

        // Category filters
        categoryFilters.addEventListener('click', (e) => {
            if (e.target.classList.contains('filter-btn')) {
                // Remove active class from all buttons
                categoryFilters.querySelectorAll('.filter-btn').forEach(btn => {
                    btn.classList.remove('active');
                });

                // Add active class to clicked button
                e.target.classList.add('active');

                // Filter captions
                activeCategory = e.target.dataset.category;
                filterCaptions();
            }
        });

        // Search functionality
        let searchTimeout;
        captionSearch.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                filterCaptions();
            }, 300);
        });
    }

    // Handle file upload
    async function handleFileUpload(event) {
        const file = event.target.files[0];

        if (!file) return;

        if (!isExcelFile(file)) {
            showStatus('error', 'Please upload an Excel file (.xlsx or .xls)');
            return;
        }

        // Ask for confirmation before replacing
        if (!confirm("⚠️ This will DELETE all existing captions and replace with new ones. Continue?")) {
            // Clear the file input if user cancels
            excelUpload.value = '';
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            showStatus('loading', 'Replacing all captions...');

            const response = await fetch('/api/captions/replace-all', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                showStatus('success', result.message);

                // Show summary if available
                if (result.summary) {
                    const summaryText = `Replaced with ${result.summary.total} captions across ${Object.keys(result.summary.by_category).length} categories`;
                    console.log('Upload Summary:', result.summary);
                }

                // Reload captions to show new ones
                await loadCaptions();
                await loadStats();

                // Clear the file input
                excelUpload.value = '';
            } else {
                showStatus('error', result.message);
            }
        } catch (error) {
            showStatus('error', 'Error uploading file. Please try again.');
            console.error('Upload error:', error);
        }
    }

    // Check if file is Excel
    function isExcelFile(file) {
        const validTypes = [
            'application/vnd.ms-excel',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        ];
        const validExtensions = ['.xls', '.xlsx'];

        const hasValidType = validTypes.includes(file.type);
        const hasValidExtension = validExtensions.some(ext => file.name.toLowerCase().endsWith(ext));

        return hasValidType || hasValidExtension;
    }

    // Show upload status
    function showStatus(type, message) {
        uploadStatus.style.display = 'block';
        uploadStatus.className = 'upload-status ' + type;

        const statusContent = uploadStatus.querySelector('.status-content');
        const statusIcon = statusContent.querySelector('.status-icon');
        const statusMessage = statusContent.querySelector('.status-message');

        if (type === 'loading') {
            statusIcon.innerHTML = '⏳';
        } else if (type === 'success') {
            statusIcon.innerHTML = '✓';
        } else if (type === 'error') {
            statusIcon.innerHTML = '✕';
        }

        statusMessage.textContent = message;

        if (type !== 'loading') {
            setTimeout(() => {
                uploadStatus.style.display = 'none';
            }, 5000);
        }
    }

    // Filter captions based on category and search
    function filterCaptions() {
        const searchTerm = captionSearch.value.toLowerCase();

        filteredCaptions = allCaptions.filter(caption => {
            const matchesCategory = activeCategory === 'All Categories' || caption.category === activeCategory;
            const matchesSearch = !searchTerm || caption.text.toLowerCase().includes(searchTerm);
            return matchesCategory && matchesSearch;
        });

        renderCaptions();
    }

    // Update category filters based on loaded captions
    function updateCategoryFilters() {
        const categories = new Set(['All Categories']);
        allCaptions.forEach(caption => {
            if (caption.category) {
                categories.add(caption.category);
            }
        });

        // Get unique categories and sort them
        const sortedCategories = Array.from(categories).sort((a, b) => {
            if (a === 'All Categories') return -1;
            if (b === 'All Categories') return 1;
            return a.localeCompare(b);
        });

        // Keep existing filter buttons if they match, otherwise rebuild
        const existingButtons = categoryFilters.querySelectorAll('.filter-btn');
        const existingCategories = Array.from(existingButtons).map(btn => btn.dataset.category);

        if (JSON.stringify(sortedCategories) !== JSON.stringify(existingCategories)) {
            categoryFilters.innerHTML = '';
            sortedCategories.forEach(category => {
                const btn = document.createElement('button');
                btn.className = 'filter-btn';
                if (category === activeCategory) {
                    btn.classList.add('active');
                }
                btn.dataset.category = category;
                btn.textContent = category;
                categoryFilters.appendChild(btn);
            });
        }
    }

    // Render captions to the grid
    function renderCaptions() {
        // Update count
        captionCount.textContent = `${filteredCaptions.length} caption${filteredCaptions.length !== 1 ? 's' : ''}`;

        // Clear grid
        messagesGrid.innerHTML = '';

        if (filteredCaptions.length === 0) {
            // Show empty state
            messagesGrid.innerHTML = `
                <div class="empty-state">
                    <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
                        <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"></path>
                        <polyline points="14 2 14 8 20 8"></polyline>
                        <line x1="16" y1="13" x2="8" y2="13"></line>
                        <line x1="16" y1="17" x2="8" y2="17"></line>
                        <polyline points="10 9 9 9 8 9"></polyline>
                    </svg>
                    <p>No captions found</p>
                    <p class="empty-subtext">Try adjusting your filters or search term</p>
                </div>
            `;
            return;
        }

        // Render caption cards
        filteredCaptions.forEach(caption => {
            const card = createMessageCard(caption);
            messagesGrid.appendChild(card);
        });
    }

    // Create a message card element
    function createMessageCard(caption) {
        const card = document.createElement('div');
        card.className = 'message-card';
        card.dataset.captionId = caption.id;

        // Format date if available
        const createdDate = caption.created_at ?
            new Date(caption.created_at).toLocaleDateString() : '';

        // Usage badge
        const usageBadge = caption.usage_count > 0 ?
            `<span class="usage-badge" title="Used ${caption.usage_count} time(s)">
                ${caption.usage_count}x
            </span>` : '';

        card.innerHTML = `
            <div class="card-header">
                <div class="message-category">${caption.category || 'General'}</div>
                ${usageBadge}
            </div>
            <p class="message-text">${escapeHtml(caption.text)}</p>
            <div class="card-footer">
                <button class="copy-btn" data-id="${caption.id}">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                    </svg>
                    Copy
                </button>
                ${caption.source ? `<span class="source-label" title="Source: ${caption.source}">📄</span>` : ''}
                ${createdDate ? `<span class="date-label">${createdDate}</span>` : ''}
            </div>
        `;

        // Add event listeners
        const copyBtn = card.querySelector('.copy-btn');
        copyBtn.addEventListener('click', async () => {
            await copyToClipboard(caption.text);

            // Track usage
            try {
                await fetch(`/api/captions/${caption.id}/use`, { method: 'POST' });
                caption.usage_count = (caption.usage_count || 0) + 1;

                // Update the badge
                const badge = card.querySelector('.usage-badge');
                if (badge) {
                    badge.textContent = `${caption.usage_count}x`;
                } else {
                    const header = card.querySelector('.card-header');
                    header.insertAdjacentHTML('beforeend',
                        `<span class="usage-badge" title="Used ${caption.usage_count} time(s)">
                            ${caption.usage_count}x
                        </span>`
                    );
                }
            } catch (error) {
                console.error('Error tracking usage:', error);
            }
        });

        return card;
    }

    // Escape HTML to prevent XSS
    function escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, m => map[m]);
    }

    // Copy text to clipboard
    async function copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text);
            showCopyToast();
        } catch (err) {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            textArea.style.position = 'fixed';
            textArea.style.opacity = '0';
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            showCopyToast();
        }
    }

    // Show copy toast notification
    function showCopyToast() {
        copyToast.classList.add('show');
        setTimeout(() => {
            copyToast.classList.remove('show');
        }, 2000);
    }

    // Check system status
    async function checkSystemStatus() {
        try {
            const response = await fetch('/api/status');
            const status = await response.json();

            const statusElement = document.getElementById('systemStatus');
            const statusDot = statusElement.querySelector('.status-dot');
            const statusText = statusElement.querySelector('.status-text');

            if (status.online) {
                statusDot.className = 'status-dot online';
                statusText.textContent = 'System Online';
            } else {
                statusDot.className = 'status-dot offline';
                statusText.textContent = 'System Offline';
            }
        } catch (error) {
            console.error('Error checking status:', error);
        }
    }

    // Check status periodically
    checkSystemStatus();
    setInterval(checkSystemStatus, 30000); // Check every 30 seconds
});