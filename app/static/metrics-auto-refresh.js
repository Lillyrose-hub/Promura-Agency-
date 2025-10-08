/**
 * Auto-Refresh Metrics System
 * Updates metrics dashboard without page reload
 */

let metricsRefreshInterval = null;
let isRefreshing = false;

// Initialize metrics auto-refresh
document.addEventListener('DOMContentLoaded', function() {
    if (window.location.pathname === '/metrics') {
        startMetricsAutoRefresh();
        console.log('Metrics auto-refresh initialized');
    }
});

// Start auto-refresh
function startMetricsAutoRefresh() {
    // Initial load
    refreshMetrics();

    // Refresh every 5 seconds
    metricsRefreshInterval = setInterval(refreshMetrics, 5000);
}

// Stop auto-refresh
function stopMetricsAutoRefresh() {
    if (metricsRefreshInterval) {
        clearInterval(metricsRefreshInterval);
        metricsRefreshInterval = null;
    }
}

// Refresh metrics data
async function refreshMetrics() {
    if (isRefreshing) return;

    isRefreshing = true;

    try {
        const response = await fetch('/api/metrics');
        const data = await response.json();

        // Update metrics display
        updateMetricsDisplay(data);

        // Update last refresh time
        updateLastRefreshTime();

    } catch (error) {
        console.error('Error refreshing metrics:', error);
    } finally {
        isRefreshing = false;
    }
}

// Update metrics display elements
function updateMetricsDisplay(data) {
    // System metrics
    if (data.system) {
        updateElement('systemStatus', data.system.online ? 'Online' : 'Offline');
        updateElement('scheduledPosts', data.system.scheduled_posts);
        updateElement('completedPosts', data.system.completed_posts);
    }

    // API metrics
    if (data.api && data.api.total_requests) {
        updateElement('totalRequests', formatNumber(data.api.total_requests));
        updateElement('successRate', formatPercentage(data.api.success_rate));
        updateElement('avgResponseTime', formatMs(data.api.avg_response_time));
    }

    // Post statistics
    if (data.posts) {
        updateElement('totalPosts', data.posts.total || 0);
        updateElement('successfulPosts', data.posts.successful || 0);
        updateElement('failedPosts', data.posts.failed || 0);
        updateElement('pendingPosts', data.posts.pending || 0);
    }

    // Recent activity
    if (data.recent_activity && Array.isArray(data.recent_activity)) {
        updateRecentActivity(data.recent_activity);
    }

    // Error logs
    if (data.errors && Array.isArray(data.errors)) {
        updateErrorLogs(data.errors);
    }
}

// Update recent activity list
function updateRecentActivity(activities) {
    const container = document.getElementById('recentActivityList');
    if (!container) return;

    if (activities.length === 0) {
        container.innerHTML = '<p class="empty-message">No recent activity</p>';
        return;
    }

    container.innerHTML = activities.slice(0, 10).map(activity => `
        <div class="activity-item">
            <span class="activity-time">${formatTimeAgo(activity.timestamp)}</span>
            <span class="activity-message">${escapeHtml(activity.message)}</span>
        </div>
    `).join('');
}

// Update error logs
function updateErrorLogs(errors) {
    const container = document.getElementById('errorLogsList');
    if (!container) return;

    if (errors.length === 0) {
        container.innerHTML = '<p class="empty-message">No errors logged</p>';
        return;
    }

    container.innerHTML = errors.slice(0, 10).map(error => `
        <div class="error-item">
            <span class="error-time">${formatTimeAgo(error.timestamp)}</span>
            <span class="error-type">${escapeHtml(error.type)}</span>
            <span class="error-message">${escapeHtml(error.message)}</span>
        </div>
    `).join('');
}

// Helper: Update element text content
function updateElement(id, value) {
    const element = document.getElementById(id);
    if (element) {
        element.textContent = value;
    }
}

// Helper: Format number with commas
function formatNumber(num) {
    if (typeof num !== 'number') return '0';
    return num.toLocaleString();
}

// Helper: Format percentage
function formatPercentage(value) {
    if (typeof value !== 'number') return '0%';
    return `${(value * 100).toFixed(1)}%`;
}

// Helper: Format milliseconds
function formatMs(ms) {
    if (typeof ms !== 'number') return '0ms';
    return `${ms.toFixed(0)}ms`;
}

// Helper: Format time ago
function formatTimeAgo(timestamp) {
    const date = new Date(timestamp);
    const seconds = Math.floor((new Date() - date) / 1000);

    if (seconds < 60) return `${seconds}s ago`;
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
    return `${Math.floor(seconds / 86400)}d ago`;
}

// Helper: Update last refresh time display
function updateLastRefreshTime() {
    const element = document.getElementById('lastRefresh');
    if (element) {
        const now = new Date();
        element.textContent = `Last updated: ${now.toLocaleTimeString()}`;
    }
}

// Helper: Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Pause/resume controls
function pauseMetricsRefresh() {
    stopMetricsAutoRefresh();
    console.log('Metrics auto-refresh paused');
}

function resumeMetricsRefresh() {
    startMetricsAutoRefresh();
    console.log('Metrics auto-refresh resumed');
}

// Export functions for external use
window.metricsAutoRefresh = {
    start: startMetricsAutoRefresh,
    stop: stopMetricsAutoRefresh,
    pause: pauseMetricsRefresh,
    resume: resumeMetricsRefresh,
    refresh: refreshMetrics
};
