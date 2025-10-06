// Content Library Management System
class ContentLibraryManager {
    constructor() {
        this.media = [];
        this.currentFilter = 'all';
        this.currentSort = 'recent';
        this.selectedMedia = [];
        this.init();
    }

    async init() {
        await this.loadLibrary();
        this.setupEventListeners();
        await this.loadStats();
    }

    async loadLibrary() {
        try {
            const response = await fetch('/api/library');
            this.media = await response.json();
            this.renderLibrary();
        } catch (error) {
            console.error('Error loading library:', error);
        }
    }

    async loadStats() {
        try {
            const response = await fetch('/api/library/stats');
            const stats = await response.json();
            this.updateStats(stats);
        } catch (error) {
            console.error('Error loading stats:', error);
        }
    }

    updateStats(stats) {
        document.getElementById('libraryTotalItems').textContent = `${stats.total_items} items`;
        document.getElementById('libraryTotalSize').textContent = stats.total_size || '0 MB';
    }

    setupEventListeners() {
        // Filter buttons
        document.querySelectorAll('.btn-library-filter').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.btn-library-filter').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                this.currentFilter = btn.dataset.filter;
                this.renderLibrary();
            });
        });

        // Search
        const searchInput = document.getElementById('librarySearch');
        if (searchInput) {
            searchInput.addEventListener('input', debounce(async (e) => {
                if (e.target.value.trim()) {
                    await this.searchLibrary(e.target.value);
                } else {
                    await this.loadLibrary();
                }
            }, 300));
        }

        // Sort
        const sortSelect = document.getElementById('librarySort');
        if (sortSelect) {
            sortSelect.addEventListener('change', (e) => {
                this.currentSort = e.target.value;
                this.sortMedia();
                this.renderLibrary();
            });
        }
    }

    async searchLibrary(query) {
        try {
            const response = await fetch(`/api/library/search?q=${encodeURIComponent(query)}`);
            this.media = await response.json();
            this.renderLibrary();
        } catch (error) {
            console.error('Error searching library:', error);
        }
    }

    sortMedia() {
        switch(this.currentSort) {
            case 'popular':
                this.media.sort((a, b) => b.used_count - a.used_count);
                break;
            case 'name':
                this.media.sort((a, b) => a.filename.localeCompare(b.filename));
                break;
            case 'recent':
            default:
                this.media.sort((a, b) => new Date(b.upload_date) - new Date(a.upload_date));
        }
    }

    filterMedia() {
        if (this.currentFilter === 'all') {
            return this.media;
        }
        return this.media.filter(item => item.type === this.currentFilter);
    }

    renderLibrary() {
        const grid = document.getElementById('libraryGrid');
        if (!grid) return;

        const filteredMedia = this.filterMedia();

        if (filteredMedia.length === 0) {
            grid.innerHTML = `
                <div class="library-empty">
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
                        <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                        <circle cx="8.5" cy="8.5" r="1.5"></circle>
                        <polyline points="21 15 16 10 5 21"></polyline>
                    </svg>
                    <p>No media found</p>
                </div>
            `;
            return;
        }

        grid.innerHTML = filteredMedia.map(item => this.createMediaCard(item)).join('');
    }

    createMediaCard(item) {
        const isImage = item.type === 'image';
        const thumbnail = item.thumbnail_url || item.url;
        const uploadDate = new Date(item.upload_date).toLocaleDateString();

        return `
            <div class="media-card" data-id="${item.id}" data-type="${item.type}">
                <div class="media-preview">
                    ${isImage ?
                        `<img src="${thumbnail}" alt="${item.filename}" loading="lazy">` :
                        `<div class="video-thumbnail">
                            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                <polygon points="5 3 19 12 5 21 5 3"></polygon>
                            </svg>
                        </div>`
                    }
                    <div class="media-overlay">
                        <button class="btn-media-preview" onclick="previewMedia('${item.id}')">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                                <circle cx="12" cy="12" r="3"></circle>
                            </svg>
                        </button>
                    </div>
                </div>
                <div class="media-info">
                    <span class="media-name">${this.truncateFilename(item.filename)}</span>
                    <div class="media-meta">
                        <span class="media-size">${item.file_size}</span>
                        <span class="media-date">${uploadDate}</span>
                    </div>
                    <div class="media-stats">
                        <span class="usage-count">Used ${item.used_count} time${item.used_count !== 1 ? 's' : ''}</span>
                    </div>
                    ${item.tags && item.tags.length > 0 ?
                        `<div class="media-tags">
                            ${item.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                        </div>` : ''
                    }
                    <div class="media-actions">
                        <button class="btn-use-media" onclick="useInPost('${item.id}')">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                <line x1="12" y1="5" x2="12" y2="19"></line>
                                <line x1="5" y1="12" x2="19" y2="12"></line>
                            </svg>
                            Use in Post
                        </button>
                        <button class="btn-delete-media" onclick="deleteFromLibrary('${item.id}')">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                <polyline points="3 6 5 6 21 6"></polyline>
                                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    truncateFilename(filename, maxLength = 20) {
        if (filename.length <= maxLength) return filename;
        const ext = filename.split('.').pop();
        const name = filename.substring(0, maxLength - ext.length - 4);
        return `${name}...${ext}`;
    }
}

// Utility function for debouncing
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

// Global functions for button actions
async function useInPost(mediaId) {
    try {
        // Get media details
        const media = libraryManager.media.find(m => m.id === mediaId);
        if (!media) return;

        // Add to current post form
        const mediaInput = document.getElementById('media_files');
        if (mediaInput) {
            // Create a visual indicator that media was added
            const mediaPreview = document.getElementById('mediaPreview');
            if (mediaPreview) {
                const previewItem = document.createElement('div');
                previewItem.className = 'media-preview-item';
                previewItem.innerHTML = media.type === 'image' ?
                    `<img src="${media.url}" alt="${media.filename}">` :
                    `<video src="${media.url}"></video>`;
                mediaPreview.appendChild(previewItem);
            }
        }

        // Update usage count
        await fetch(`/api/library/${mediaId}/use`, { method: 'POST' });

        // Notify user
        showNotification('Media added to post', 'success');

        // Reload library to show updated usage count
        await libraryManager.loadLibrary();
    } catch (error) {
        console.error('Error using media:', error);
        showNotification('Failed to add media', 'error');
    }
}

async function deleteFromLibrary(mediaId) {
    if (!confirm('Are you sure you want to delete this media from library?')) {
        return;
    }

    try {
        const response = await fetch(`/api/library/${mediaId}`, { method: 'DELETE' });
        if (response.ok) {
            showNotification('Media deleted from library', 'success');
            await libraryManager.loadLibrary();
            await libraryManager.loadStats();
        } else {
            showNotification('Failed to delete media', 'error');
        }
    } catch (error) {
        console.error('Error deleting media:', error);
        showNotification('Error deleting media', 'error');
    }
}

function previewMedia(mediaId) {
    const media = libraryManager.media.find(m => m.id === mediaId);
    if (!media) return;

    // Create modal for preview
    const modal = document.createElement('div');
    modal.className = 'media-preview-modal';
    modal.innerHTML = `
        <div class="modal-content">
            <span class="modal-close" onclick="this.parentElement.parentElement.remove()">&times;</span>
            ${media.type === 'image' ?
                `<img src="${media.url}" alt="${media.filename}">` :
                `<video src="${media.url}" controls></video>`
            }
            <div class="modal-info">
                <h3>${media.filename}</h3>
                <p>Size: ${media.file_size} | Used: ${media.used_count} times</p>
            </div>
        </div>
    `;
    document.body.appendChild(modal);
}

function openLibraryUpload() {
    // Create upload modal
    const modal = document.createElement('div');
    modal.className = 'library-upload-modal';
    modal.innerHTML = `
        <div class="modal-content">
            <span class="modal-close" onclick="this.parentElement.parentElement.remove()">&times;</span>
            <h2>Upload to Library</h2>
            <form id="libraryUploadForm">
                <div class="form-group">
                    <label>Select File</label>
                    <input type="file" id="libraryFile" accept="image/*,video/*" required>
                </div>
                <div class="form-group">
                    <label>Tags (comma separated)</label>
                    <input type="text" id="libraryTags" placeholder="e.g., promo, selfie, professional">
                </div>
                <div class="form-group">
                    <label>Description</label>
                    <textarea id="libraryDescription" placeholder="Optional description"></textarea>
                </div>
                <button type="submit" class="btn">Upload to Library</button>
            </form>
        </div>
    `;
    document.body.appendChild(modal);

    // Handle form submission
    document.getElementById('libraryUploadForm').addEventListener('submit', async (e) => {
        e.preventDefault();

        const file = document.getElementById('libraryFile').files[0];
        const tags = document.getElementById('libraryTags').value;
        const description = document.getElementById('libraryDescription').value;

        const formData = new FormData();
        formData.append('file', file);
        formData.append('tags', tags);
        formData.append('description', description);

        try {
            const response = await fetch('/api/library/upload', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                showNotification('File uploaded to library', 'success');
                modal.remove();
                await libraryManager.loadLibrary();
                await libraryManager.loadStats();
            } else {
                showNotification('Upload failed', 'error');
            }
        } catch (error) {
            console.error('Upload error:', error);
            showNotification('Upload error', 'error');
        }
    });
}

// Initialize library manager when DOM is ready
let libraryManager;
document.addEventListener('DOMContentLoaded', () => {
    libraryManager = new ContentLibraryManager();
});