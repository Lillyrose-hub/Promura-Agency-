// Ultra-Compact Caption Library JavaScript
let allCaptions = [];
let activeFilter = 'All';

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadCaptions();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    // Excel upload
    const uploadInput = document.getElementById('excelUpload');
    if (uploadInput) {
        uploadInput.addEventListener('change', handleExcelUpload);
    }

    // Add caption button
    const addBtn = document.getElementById('addCaptionBtn');
    if (addBtn) {
        addBtn.addEventListener('click', handleAddCaption);
    }

    // Enter key on caption input
    const captionInput = document.getElementById('newCaptionInput');
    if (captionInput) {
        captionInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                handleAddCaption();
            }
        });
    }

    // Search input
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                filterCaptions(searchInput.value);
            }, 300);
        });
    }

    // Category filters
    document.querySelectorAll('.pill-mini').forEach(pill => {
        pill.addEventListener('click', function() {
            document.querySelectorAll('.pill-mini').forEach(p => p.classList.remove('active'));
            this.classList.add('active');
            activeFilter = this.dataset.category;
            filterByCategory(activeFilter);
        });
    });
}

// Load captions from API
async function loadCaptions() {
    try {
        const response = await fetch('/api/captions');
        if (response.ok) {
            allCaptions = await response.json();
            renderCaptions(allCaptions);
            updateCount(allCaptions.length);
        }
    } catch (error) {
        console.error('Error loading captions:', error);
    }
}

// Render captions in grid
function renderCaptions(captions) {
    const grid = document.getElementById('captionGrid');

    if (captions.length === 0) {
        grid.innerHTML = '';
        return;
    }

    grid.innerHTML = captions.map(caption => `
        <div class="caption-card-compact" data-id="${caption.id}">
            <div class="caption-text">${escapeHtml(caption.text)}</div>
            <div class="caption-meta">
                <span class="caption-category">${caption.category}</span>
                <span class="caption-usage">${caption.usage_count || 0} uses</span>
            </div>
        </div>
    `).join('');

    // Add click handlers
    grid.querySelectorAll('.caption-card-compact').forEach(card => {
        card.addEventListener('click', () => copyCaption(card.dataset.id));
    });
}

// Copy caption to clipboard
async function copyCaption(captionId) {
    const caption = allCaptions.find(c => c.id === captionId);
    if (caption) {
        try {
            await navigator.clipboard.writeText(caption.text);

            // Track usage
            fetch(`/api/captions/${captionId}/use`, { method: 'POST' });

            // Show toast
            showToast('Caption copied!', 'success');

            // Update usage count locally
            caption.usage_count = (caption.usage_count || 0) + 1;
            renderCaptions(getFilteredCaptions());
        } catch (error) {
            console.error('Error copying caption:', error);
        }
    }
}

// Handle Excel upload
async function handleExcelUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    // Ask for confirmation before replacing
    if (!confirm("⚠️ This will DELETE all existing captions and replace with new ones. Continue?")) {
        event.target.value = ''; // Clear the file input
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/api/captions/replace-all', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.success) {
            showToast(`Replaced all captions. Added ${result.captions.length} captions`, 'success');
            await loadCaptions();
        } else {
            showToast(result.message || 'Upload failed', 'error');
        }
    } catch (error) {
        showToast('Upload error', 'error');
        console.error('Upload error:', error);
    }

    // Reset input
    event.target.value = '';
}

// Handle adding single caption
async function handleAddCaption() {
    const input = document.getElementById('newCaptionInput');
    const categorySelect = document.getElementById('categorySelect');

    const text = input.value.trim();
    if (!text) return;

    const formData = new FormData();
    formData.append('text', text);
    formData.append('category', categorySelect.value);

    try {
        const response = await fetch('/api/captions/add-single', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.success) {
            showToast('Caption added', 'success');
            input.value = '';
            await loadCaptions();
        } else {
            showToast('Failed to add caption', 'error');
        }
    } catch (error) {
        showToast('Error adding caption', 'error');
        console.error('Error:', error);
    }
}

// Filter captions by search text
function filterCaptions(searchText) {
    const filtered = searchText
        ? allCaptions.filter(c =>
            c.text.toLowerCase().includes(searchText.toLowerCase()))
        : getFilteredCaptions();

    renderCaptions(filtered);
}

// Filter by category
function filterByCategory(category) {
    renderCaptions(getFilteredCaptions());
}

// Get filtered captions based on active filter
function getFilteredCaptions() {
    if (activeFilter === 'All') {
        return allCaptions;
    }
    return allCaptions.filter(c => c.category === activeFilter);
}

// Update caption count
function updateCount(count) {
    const badge = document.getElementById('captionCount');
    if (badge) {
        badge.textContent = count.toString();
    }
}

// Show toast notification
function showToast(message, type = 'info') {
    const toast = document.getElementById('notificationToast');
    if (!toast) {
        // Use copy toast as fallback
        const copyToast = document.getElementById('copyToast');
        if (copyToast) {
            copyToast.querySelector('.toast-text').textContent = message;
            copyToast.classList.add('show');
            setTimeout(() => copyToast.classList.remove('show'), 2000);
        }
        return;
    }

    toast.querySelector('.toast-message').textContent = message;
    toast.className = `notification-toast show ${type}`;

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Escape HTML for safe display
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K for search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        document.getElementById('searchInput')?.focus();
    }

    // Ctrl/Cmd + N for new caption
    if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
        e.preventDefault();
        document.getElementById('newCaptionInput')?.focus();
    }
});