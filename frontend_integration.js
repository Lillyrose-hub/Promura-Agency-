// Smart Caption Library - Frontend Integration
// This file demonstrates how to integrate with the FastAPI backend

class CaptionLibraryAPI {
    constructor(baseURL = 'http://localhost:8000') {
        this.baseURL = baseURL;
    }

    /**
     * Upload Excel file containing captions
     * @param {File} file - Excel file to upload
     * @returns {Promise} Response with upload status
     */
    async uploadExcel(file) {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch(`${this.baseURL}/api/upload-captions`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error uploading file:', error);
            throw error;
        }
    }

    /**
     * Search and filter captions
     * @param {string} category - Optional category filter
     * @param {string} searchTerm - Optional search term
     * @returns {Promise} List of matching captions
     */
    async searchCaptions(category = '', searchTerm = '') {
        const params = new URLSearchParams();

        if (category) params.append('category', category);
        if (searchTerm) params.append('search', searchTerm);

        try {
            const response = await fetch(`${this.baseURL}/api/captions?${params.toString()}`);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error fetching captions:', error);
            throw error;
        }
    }

    /**
     * Get all available categories
     * @returns {Promise} List of categories with caption counts
     */
    async getCategories() {
        try {
            const response = await fetch(`${this.baseURL}/api/categories`);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error fetching categories:', error);
            throw error;
        }
    }

    /**
     * Track caption usage when copied
     * @param {string} captionId - ID of the caption being copied
     * @returns {Promise} Updated usage count
     */
    async trackCaptionCopy(captionId) {
        try {
            const response = await fetch(`${this.baseURL}/api/copy-caption`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ caption_id: captionId })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error tracking caption copy:', error);
            throw error;
        }
    }

    /**
     * Get usage analytics
     * @returns {Promise} Analytics data including top captions and statistics
     */
    async getAnalytics() {
        try {
            const response = await fetch(`${this.baseURL}/api/analytics`);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error fetching analytics:', error);
            throw error;
        }
    }

    /**
     * Delete a specific caption
     * @param {string} captionId - ID of the caption to delete
     * @returns {Promise} Deletion status
     */
    async deleteCaption(captionId) {
        try {
            const response = await fetch(`${this.baseURL}/api/caption/${captionId}`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error deleting caption:', error);
            throw error;
        }
    }
}

// Example usage in a web application
class CaptionLibraryUI {
    constructor() {
        this.api = new CaptionLibraryAPI();
        this.currentCaptions = [];
        this.currentCategory = '';
        this.init();
    }

    init() {
        // Set up event listeners
        this.setupEventListeners();
        // Load initial data
        this.loadCategories();
        this.loadCaptions();
    }

    setupEventListeners() {
        // File upload
        const fileInput = document.getElementById('excel-upload');
        if (fileInput) {
            fileInput.addEventListener('change', (e) => this.handleFileUpload(e));
        }

        // Search input
        const searchInput = document.getElementById('search-input');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => this.handleSearch(e.target.value));
        }

        // Category filter
        const categorySelect = document.getElementById('category-select');
        if (categorySelect) {
            categorySelect.addEventListener('change', (e) => this.handleCategoryChange(e.target.value));
        }
    }

    async handleFileUpload(event) {
        const file = event.target.files[0];
        if (!file) return;

        try {
            // Show loading state
            this.showLoading(true);

            const result = await this.api.uploadExcel(file);

            // Show success message
            this.showMessage(`Successfully uploaded! Added ${result.new_captions_added} captions.`, 'success');

            // Reload categories and captions
            await this.loadCategories();
            await this.loadCaptions();
        } catch (error) {
            this.showMessage('Error uploading file: ' + error.message, 'error');
        } finally {
            this.showLoading(false);
        }
    }

    async handleSearch(searchTerm) {
        try {
            const result = await this.api.searchCaptions(this.currentCategory, searchTerm);
            this.displayCaptions(result.captions);
        } catch (error) {
            this.showMessage('Error searching captions: ' + error.message, 'error');
        }
    }

    async handleCategoryChange(category) {
        this.currentCategory = category;
        await this.loadCaptions();
    }

    async loadCategories() {
        try {
            const result = await this.api.getCategories();
            this.displayCategories(result.categories);
        } catch (error) {
            console.error('Error loading categories:', error);
        }
    }

    async loadCaptions() {
        try {
            const result = await this.api.searchCaptions(this.currentCategory);
            this.currentCaptions = result.captions;
            this.displayCaptions(result.captions);
        } catch (error) {
            console.error('Error loading captions:', error);
        }
    }

    displayCategories(categories) {
        const categorySelect = document.getElementById('category-select');
        if (!categorySelect) return;

        categorySelect.innerHTML = '<option value="">All Categories</option>';

        categories.forEach(category => {
            const option = document.createElement('option');
            option.value = category.name;
            option.textContent = `${category.name} (${category.count})`;
            categorySelect.appendChild(option);
        });
    }

    displayCaptions(captions) {
        const container = document.getElementById('captions-container');
        if (!container) return;

        container.innerHTML = '';

        if (captions.length === 0) {
            container.innerHTML = '<p class="no-results">No captions found</p>';
            return;
        }

        captions.forEach(caption => {
            const captionElement = this.createCaptionElement(caption);
            container.appendChild(captionElement);
        });
    }

    createCaptionElement(caption) {
        const div = document.createElement('div');
        div.className = 'caption-card';
        div.innerHTML = `
            <div class="caption-header">
                <span class="caption-category">${caption.category}</span>
                <span class="caption-usage">Used ${caption.usage_count} times</span>
            </div>
            <div class="caption-text">${caption.text}</div>
            <div class="caption-actions">
                <button class="copy-btn" data-id="${caption.id}" data-text="${caption.text.replace(/"/g, '&quot;')}">
                    📋 Copy
                </button>
                <button class="delete-btn" data-id="${caption.id}">
                    🗑️ Delete
                </button>
            </div>
        `;

        // Add copy functionality
        const copyBtn = div.querySelector('.copy-btn');
        copyBtn.addEventListener('click', () => this.copyCaption(caption.id, caption.text));

        // Add delete functionality
        const deleteBtn = div.querySelector('.delete-btn');
        deleteBtn.addEventListener('click', () => this.deleteCaption(caption.id));

        return div;
    }

    async copyCaption(captionId, text) {
        try {
            // Copy to clipboard
            await navigator.clipboard.writeText(text);

            // Track usage
            await this.api.trackCaptionCopy(captionId);

            // Show success message
            this.showMessage('Caption copied to clipboard!', 'success');

            // Update UI to reflect new usage count
            await this.loadCaptions();
        } catch (error) {
            this.showMessage('Error copying caption: ' + error.message, 'error');
        }
    }

    async deleteCaption(captionId) {
        if (!confirm('Are you sure you want to delete this caption?')) {
            return;
        }

        try {
            await this.api.deleteCaption(captionId);
            this.showMessage('Caption deleted successfully', 'success');
            await this.loadCaptions();
        } catch (error) {
            this.showMessage('Error deleting caption: ' + error.message, 'error');
        }
    }

    showMessage(message, type = 'info') {
        const messageContainer = document.getElementById('message-container');
        if (!messageContainer) return;

        const messageElement = document.createElement('div');
        messageElement.className = `message message-${type}`;
        messageElement.textContent = message;

        messageContainer.appendChild(messageElement);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            messageElement.remove();
        }, 5000);
    }

    showLoading(show) {
        const loader = document.getElementById('loading-indicator');
        if (loader) {
            loader.style.display = show ? 'block' : 'none';
        }
    }
}

// Initialize when DOM is ready
if (typeof document !== 'undefined') {
    document.addEventListener('DOMContentLoaded', () => {
        new CaptionLibraryUI();
    });
}

// Export for use in modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { CaptionLibraryAPI, CaptionLibraryUI };
}