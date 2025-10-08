// Dashboard JavaScript - Main functionality

// Global variables
let selectedModels = [];

// Handle different submit actions
function submitPost(event, action) {
    event.preventDefault();

    const form = document.getElementById('postForm');
    const scheduleTimeInput = document.getElementById('schedule_time');

    if (action === 'now') {
        // Clear schedule time for immediate posting
        scheduleTimeInput.value = '';
    } else if (action === 'schedule') {
        // Check if schedule time is set
        if (!scheduleTimeInput.value) {
            showNotification('Please select a schedule time', 'error');
            scheduleTimeInput.focus();
            return false;
        }
    }

    // Submit the form
    form.dispatchEvent(new Event('submit'));
}

// Debounce utility function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeModelSelector();
    initializeFormHandlers();
    initializeMediaPreview();
    updateDashboardStats();
    loadCaptionSuggestions(); // Load caption suggestions

    // Start periodic updates
    setInterval(updateDashboardStats, 30000); // Every 30 seconds
});

// Model Selector Functions
function initializeModelSelector() {
    const modelSearch = document.getElementById('modelSearch');
    const modelDropdown = document.getElementById('modelDropdown');
    const modelList = document.getElementById('modelList');

    if (!modelSearch || !modelDropdown) return;

    // Toggle dropdown on click
    modelSearch.addEventListener('click', (e) => {
        e.stopPropagation();
        modelDropdown.style.display = modelDropdown.style.display === 'block' ? 'none' : 'block';
    });

    // Search functionality
    modelSearch.addEventListener('input', (e) => {
        const searchTerm = e.target.value.toLowerCase();
        const modelItems = modelList.querySelectorAll('.model-item');

        modelItems.forEach(item => {
            const modelName = item.dataset.modelName.toLowerCase();
            item.style.display = modelName.includes(searchTerm) ? 'flex' : 'none';
        });
    });

    // Handle model selection
    document.querySelectorAll('.model-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', (e) => {
            const modelName = e.target.value;

            if (e.target.checked) {
                if (!selectedModels.includes(modelName)) {
                    selectedModels.push(modelName);
                }
            } else {
                selectedModels = selectedModels.filter(m => m !== modelName);
            }

            updateSelectedModelsDisplay();
        });
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.model-selector')) {
            modelDropdown.style.display = 'none';
        }
    });
}

// Update selected models display
function updateSelectedModelsDisplay() {
    const selectedModelsDiv = document.getElementById('selectedModels');
    if (!selectedModelsDiv) return;

    selectedModelsDiv.innerHTML = selectedModels.map(model => `
        <span class="model-pill">
            ${model}
            <span class="remove-model" onclick="removeModel('${model}')">×</span>
        </span>
    `).join('');
}

// Remove model from selection
function removeModel(modelName) {
    selectedModels = selectedModels.filter(m => m !== modelName);
    document.querySelectorAll('.model-checkbox').forEach(checkbox => {
        if (checkbox.value === modelName) {
            checkbox.checked = false;
        }
    });
    updateSelectedModelsDisplay();
}

// Select all models
function selectAllModels() {
    selectedModels = [];
    document.querySelectorAll('.model-checkbox').forEach(checkbox => {
        checkbox.checked = true;
        selectedModels.push(checkbox.value);
    });
    updateSelectedModelsDisplay();
}

// Deselect all models
function deselectAllModels() {
    selectedModels = [];
    document.querySelectorAll('.model-checkbox').forEach(checkbox => {
        checkbox.checked = false;
    });
    updateSelectedModelsDisplay();
}

// Form Handlers
function initializeFormHandlers() {
    const postForm = document.getElementById('postForm');
    if (!postForm) return;

    postForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        await submitPost();
    });
}

// Submit post
async function submitPost() {
    const formData = new FormData();
    formData.append('content', document.getElementById('content').value);
    formData.append('models', JSON.stringify(selectedModels));
    formData.append('schedule_time', document.getElementById('schedule_time').value);

    // Add library media IDs
    if (selectedLibraryMedia.length > 0) {
        formData.append('library_media_ids', JSON.stringify(selectedLibraryMedia.map(m => m.id)));
    }

    // Add new uploaded files
    uploadedFiles.forEach(file => {
        formData.append('media_files', file);
    });

    try {
        const response = await fetch('/schedule-post', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        showNotification(result.message, result.success ? 'success' : 'error');

        if (result.success) {
            // Reset form
            document.getElementById('postForm').reset();
            selectedModels = [];
            selectedLibraryMedia = [];
            uploadedFiles = [];
            updateSelectedModelsDisplay();
            updateMediaPreview();

            // Update stats
            updateDashboardStats();
        }
    } catch (error) {
        showNotification('Error: ' + error.message, 'error');
    }
}

// Media Preview
let selectedLibraryMedia = [];
let uploadedFiles = [];

function initializeMediaPreview() {
    const mediaInput = document.getElementById('media_files');
    if (!mediaInput) return;

    mediaInput.addEventListener('change', (e) => {
        uploadedFiles = Array.from(e.target.files);
        updateMediaPreview();
    });
}

// Update combined media preview
function updateMediaPreview() {
    const previewGrid = document.getElementById('mediaPreviewGrid');
    const previewHeader = document.querySelector('.media-preview-header');
    const mediaCount = document.getElementById('mediaCount');

    if (!previewGrid) return;

    previewGrid.innerHTML = '';
    const totalCount = selectedLibraryMedia.length + uploadedFiles.length;

    if (totalCount === 0) {
        previewHeader.style.display = 'none';
        return;
    }

    previewHeader.style.display = 'block';
    mediaCount.textContent = `${totalCount} file${totalCount !== 1 ? 's' : ''}`;

    // Add library items first (with indicator)
    selectedLibraryMedia.forEach(media => {
        const div = document.createElement('div');
        div.className = 'preview-item library-item';
        div.innerHTML = `
            <div class="preview-badge">Library</div>
            ${media.type === 'image' ?
                `<img src="${media.url}" alt="${media.filename}">` :
                `<video src="${media.url}"></video>`}
            <button class="remove-preview" onclick="removeLibraryMedia('${media.id}')">×</button>
        `;
        previewGrid.appendChild(div);
    });

    // Add new uploads (with indicator)
    uploadedFiles.forEach((file, index) => {
        const reader = new FileReader();
        reader.onload = (e) => {
            const div = document.createElement('div');
            div.className = 'preview-item upload-item';
            div.innerHTML = `
                <div class="preview-badge new">New Upload</div>
                ${file.type.startsWith('image/') ?
                    `<img src="${e.target.result}" alt="${file.name}">` :
                    `<video src="${e.target.result}"></video>`}
                <button class="remove-preview" onclick="removeUploadedFile(${index})">×</button>
            `;
            previewGrid.appendChild(div);
        };
        reader.readAsDataURL(file);
    });
}

// Open file upload dialog
function openFileUpload() {
    document.getElementById('media_files').click();
}

// Open library modal for post selection
function openLibraryForPost() {
    const modal = document.getElementById('librarySelectionModal');
    if (modal) {
        modal.style.display = 'block';
        loadLibraryForSelection();
    }
}

// Close library modal
function closeLibraryModal() {
    const modal = document.getElementById('librarySelectionModal');
    if (modal) {
        modal.style.display = 'none';
    }
}

// Load library content for selection
async function loadLibraryForSelection() {
    try {
        const response = await fetch('/api/library');
        const media = await response.json();
        renderLibraryModal(media);
    } catch (error) {
        console.error('Error loading library:', error);
    }
}

// Render library items in modal
function renderLibraryModal(media) {
    const grid = document.getElementById('libraryModalGrid');
    if (!grid) return;

    if (media.length === 0) {
        grid.innerHTML = '<p class="empty-message">No media in library yet</p>';
        return;
    }

    grid.innerHTML = media.map(item => `
        <div class="library-modal-item ${selectedLibraryMedia.find(m => m.id === item.id) ? 'selected' : ''}"
             data-media-id="${item.id}" onclick="toggleLibraryItem('${item.id}')">
            <div class="item-checkbox">
                <input type="checkbox" ${selectedLibraryMedia.find(m => m.id === item.id) ? 'checked' : ''}>
            </div>
            ${item.type === 'image' ?
                `<img src="${item.thumbnail_url || item.url}" alt="${item.filename}">` :
                `<div class="video-thumb">
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <polygon points="5 3 19 12 5 21 5 3"></polygon>
                    </svg>
                </div>`}
            <div class="item-info">
                <span class="item-name">${item.filename}</span>
                <span class="item-meta">${item.file_size}</span>
            </div>
        </div>
    `).join('');

    updateModalSelectionCount();
}

// Toggle library item selection
function toggleLibraryItem(mediaId) {
    const existingIndex = selectedLibraryMedia.findIndex(m => m.id === mediaId);

    if (existingIndex >= 0) {
        selectedLibraryMedia.splice(existingIndex, 1);
    } else {
        // Fetch media details and add to selection
        fetch('/api/library')
            .then(res => res.json())
            .then(media => {
                const item = media.find(m => m.id === mediaId);
                if (item) {
                    selectedLibraryMedia.push(item);
                    updateModalSelectionCount();
                }
            });
    }

    // Update visual state
    const itemElement = document.querySelector(`[data-media-id="${mediaId}"]`);
    if (itemElement) {
        itemElement.classList.toggle('selected');
        const checkbox = itemElement.querySelector('input[type="checkbox"]');
        if (checkbox) checkbox.checked = !checkbox.checked;
    }
}

// Update selection count in modal
function updateModalSelectionCount() {
    const countElement = document.getElementById('modalSelectionCount');
    if (countElement) {
        countElement.textContent = `${selectedLibraryMedia.length} selected`;
    }
}

// Add selected library items to post
function addSelectedToPost() {
    updateMediaPreview();
    closeLibraryModal();
    showNotification(`Added ${selectedLibraryMedia.length} items from library`, 'success');
}

// Remove library media from selection
function removeLibraryMedia(mediaId) {
    selectedLibraryMedia = selectedLibraryMedia.filter(m => m.id !== mediaId);
    updateMediaPreview();
}

// Remove uploaded file from selection
function removeUploadedFile(index) {
    uploadedFiles.splice(index, 1);
    updateMediaPreview();
}

// Modal search functionality
document.addEventListener('DOMContentLoaded', function() {
    const modalSearch = document.getElementById('modalLibrarySearch');
    if (modalSearch) {
        modalSearch.addEventListener('input', debounce(async (e) => {
            const query = e.target.value.trim();
            if (query) {
                const response = await fetch(`/api/library/search?q=${encodeURIComponent(query)}`);
                const results = await response.json();
                renderLibraryModal(results);
            } else {
                loadLibraryForSelection();
            }
        }, 300));
    }

    // Modal filter buttons
    document.querySelectorAll('.btn-modal-filter').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            document.querySelectorAll('.btn-modal-filter').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const filter = btn.dataset.filter;
            const url = filter === 'all' ? '/api/library' : `/api/library?media_type=${filter}`;
            const response = await fetch(url);
            const media = await response.json();
            renderLibraryModal(media);
        });
    });
});

// Show notification
function showNotification(message, type = 'info') {
    const notifications = document.getElementById('notifications');
    if (!notifications) return;

    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;

    notifications.appendChild(notification);

    // Auto-remove after 5 seconds
    setTimeout(() => {
        notification.classList.add('fade-out');
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

// Update dashboard statistics
async function updateDashboardStats() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();

        // Update counts
        const queueCount = document.getElementById('queueCount');
        const historyCount = document.getElementById('historyCount');

        if (queueCount) {
            queueCount.textContent = `${data.queue_count} scheduled posts`;
        }
        if (historyCount) {
            historyCount.textContent = `${data.completed_count} completed posts`;
        }

        // Update system status
        updateSystemStatus(data.online);
    } catch (error) {
        console.error('Error updating stats:', error);
    }
}

// Update system status indicator
function updateSystemStatus(isOnline) {
    const statusDot = document.querySelector('.status-dot');
    const statusText = document.querySelector('.status-text');

    if (!statusDot || !statusText) return;

    if (isOnline) {
        statusDot.className = 'status-dot online';
        statusText.textContent = 'System Online';
    } else {
        statusDot.className = 'status-dot offline';
        statusText.textContent = 'System Offline';
    }
}

// Load caption suggestions for post composer
async function loadCaptionSuggestions() {
    try {
        // Load popular captions
        const response = await fetch('/api/captions/popular?limit=5');
        if (response.ok) {
            const captions = await response.json();
            displayCaptionSuggestions(captions);
        }
    } catch (error) {
        console.error('Error loading caption suggestions:', error);
    }
}

// Display caption suggestions
function displayCaptionSuggestions(captions) {
    const container = document.getElementById('suggestionPills');
    if (!container) return;

    // Add styles for the suggestions
    const style = document.createElement('style');
    style.textContent = `
        .caption-suggestions-compact {
            margin-top: 8px;
            padding: 8px;
            background: var(--bg-secondary, #f5f5f5);
            border-radius: 6px;
        }
        .suggestions-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 6px;
        }
        .suggestion-pills-container {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }
        .caption-pill {
            background: var(--accent-gradient, linear-gradient(135deg, #FFDEE2 0%, #FFE8EC 100%));
            color: #0a0a0f;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            white-space: nowrap;
            max-width: 200px;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .caption-pill:hover {
            transform: translateY(-1px);
            background: #FFC4CC;
            box-shadow: 0 2px 6px rgba(255, 222, 226, 0.2);
        }
    `;
    document.head.appendChild(style);

    // Clear existing pills
    container.innerHTML = '';

    // Add caption pills
    captions.forEach(caption => {
        const pill = document.createElement('span');
        pill.className = 'caption-pill';
        pill.textContent = caption.text.length > 30
            ? caption.text.substring(0, 30) + '...'
            : caption.text;
        pill.title = caption.text; // Show full text on hover
        pill.onclick = () => insertCaption(caption.text, caption.id);
        container.appendChild(pill);
    });

    // Add "more" link if no captions
    if (captions.length === 0) {
        container.innerHTML = '<small style="color: #999; font-size: 0.7rem;">No captions yet. <a href="/captions-compact">Add some!</a></small>';
    }
}

// Insert caption into textarea
function insertCaption(text, captionId) {
    const textarea = document.getElementById('content');
    if (!textarea) return;

    // Insert at cursor or append
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const currentValue = textarea.value;

    if (start !== undefined) {
        // Insert at cursor position
        textarea.value = currentValue.substring(0, start) + text + currentValue.substring(end);
        // Move cursor to end of inserted text
        textarea.selectionStart = textarea.selectionEnd = start + text.length;
    } else {
        // Append to existing content
        textarea.value = currentValue + (currentValue ? ' ' : '') + text;
    }

    // Focus the textarea
    textarea.focus();

    // Track usage
    if (captionId) {
        fetch(`/api/captions/${captionId}/use`, { method: 'POST' })
            .catch(err => console.error('Error tracking caption usage:', err));
    }

    // Show feedback
    showNotification('Caption added to post', 'success');
}

// Queue Management Functions
async function cancelPost(postId) {
    if (!confirm('Are you sure you want to cancel this post?')) return;

    try {
        const response = await fetch(`/api/queue/${postId}/cancel`, {
            method: 'POST'
        });

        if (response.ok) {
            showNotification('Post cancelled successfully', 'success');
            location.reload();
        } else {
            showNotification('Failed to cancel post', 'error');
        }
    } catch (error) {
        showNotification('Error: ' + error.message, 'error');
    }
}

async function deletePost(postId) {
    if (!confirm('Are you sure you want to delete this post? This action cannot be undone.')) return;

    try {
        const response = await fetch(`/api/queue/${postId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            showNotification('Post deleted successfully', 'success');
            location.reload();
        } else {
            showNotification('Failed to delete post', 'error');
        }
    } catch (error) {
        showNotification('Error: ' + error.message, 'error');
    }
}

// Edit post functionality
function editPost(postId) {
    const modal = document.getElementById('editModal');
    if (!modal) return;

    const postCard = document.querySelector(`[data-post-id="${postId}"]`);
    const postText = postCard.querySelector('.post-text').textContent;

    document.getElementById('editPostId').value = postId;
    document.getElementById('editContent').value = postText;
    modal.style.display = 'block';
}

function closeEditModal() {
    const modal = document.getElementById('editModal');
    if (modal) {
        modal.style.display = 'none';
    }
}

// Initialize edit form if present
const editForm = document.getElementById('editForm');
if (editForm) {
    editForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const postId = document.getElementById('editPostId').value;
        const content = document.getElementById('editContent').value;
        const scheduleTime = document.getElementById('editScheduleTime').value;

        try {
            const response = await fetch(`/api/queue/${postId}/edit`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    content,
                    models: selectedModels,
                    schedule_time: scheduleTime
                })
            });

            if (response.ok) {
                showNotification('Post updated successfully', 'success');
                location.reload();
            } else {
                showNotification('Failed to update post', 'error');
            }
        } catch (error) {
            showNotification('Error: ' + error.message, 'error');
        }
    });
}

// Tab switching functionality
function switchTab(tab) {
    const queueTab = document.getElementById('queueTab');
    const historyTab = document.getElementById('historyTab');
    const tabBtns = document.querySelectorAll('.tab-btn');

    if (!queueTab || !historyTab) return;

    if (tab === 'queue') {
        queueTab.classList.add('active');
        historyTab.classList.remove('active');
        if (tabBtns[0]) tabBtns[0].classList.add('active');
        if (tabBtns[1]) tabBtns[1].classList.remove('active');
    } else {
        historyTab.classList.add('active');
        queueTab.classList.remove('active');
        if (tabBtns[1]) tabBtns[1].classList.add('active');
        if (tabBtns[0]) tabBtns[0].classList.remove('active');
    }
}

// Check for hash in URL to switch tabs
if (window.location.hash === '#history') {
    switchTab('history');
}

// WebSocket connection for real-time updates (optional)
function initializeWebSocket() {
    const ws = new WebSocket('ws://localhost:8000/ws');

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === 'status_update') {
            updateDashboardStats();
        }
    };

    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
    };

    ws.onclose = () => {
        // Attempt to reconnect after 5 seconds
        setTimeout(initializeWebSocket, 5000);
    };
}

// Initialize WebSocket if needed
// Uncomment to enable real-time updates
// initializeWebSocket();