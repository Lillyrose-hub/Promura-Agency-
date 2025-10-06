/**
 * PROMURA Authentication Module
 * Handles authentication, session management, and permission checks
 */

class AuthManager {
    constructor() {
        this.token = localStorage.getItem('promura_token');
        this.user = this.loadUser();
        this.authCallbacks = [];
    }

    loadUser() {
        const userStr = localStorage.getItem('promura_user');
        if (userStr) {
            try {
                return JSON.parse(userStr);
            } catch {
                return null;
            }
        }
        return null;
    }

    isAuthenticated() {
        return !!this.token && !!this.user;
    }

    getToken() {
        return this.token;
    }

    getUser() {
        return this.user;
    }

    hasPermission(permission) {
        if (!this.user) return false;
        const perms = this.user.permissions || [];
        return perms.includes('all') || perms.includes(permission);
    }

    async verifyToken() {
        if (!this.token) return false;

        try {
            const response = await fetch('/api/auth/me', {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (response.ok) {
                const userData = await response.json();
                this.user = userData;
                localStorage.setItem('promura_user', JSON.stringify(userData));
                return true;
            } else {
                this.logout();
                return false;
            }
        } catch (error) {
            console.error('Token verification failed:', error);
            return false;
        }
    }

    async login(username, password) {
        try {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();

            if (response.ok && data.success) {
                this.token = data.access_token;
                this.user = data.user;
                localStorage.setItem('promura_token', this.token);
                localStorage.setItem('promura_user', JSON.stringify(this.user));
                this.notifyAuthChange(true);
                return { success: true, user: this.user };
            } else {
                return { success: false, error: data.detail || 'Login failed' };
            }
        } catch (error) {
            console.error('Login error:', error);
            return { success: false, error: 'Connection error' };
        }
    }

    async logout() {
        if (this.token) {
            try {
                await fetch('/api/auth/logout', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${this.token}`
                    }
                });
            } catch (error) {
                console.error('Logout error:', error);
            }
        }

        this.token = null;
        this.user = null;
        localStorage.removeItem('promura_token');
        localStorage.removeItem('promura_user');
        this.notifyAuthChange(false);
        window.location.href = '/login';
    }

    onAuthChange(callback) {
        this.authCallbacks.push(callback);
    }

    notifyAuthChange(isAuthenticated) {
        this.authCallbacks.forEach(callback => callback(isAuthenticated));
    }

    // Add authorization header to fetch requests
    async authFetch(url, options = {}) {
        if (!this.token) {
            throw new Error('Not authenticated');
        }

        const headers = {
            ...options.headers,
            'Authorization': `Bearer ${this.token}`
        };

        const response = await fetch(url, { ...options, headers });

        // If unauthorized, redirect to login
        if (response.status === 401) {
            this.logout();
            throw new Error('Session expired');
        }

        return response;
    }

    updateUIForUser() {
        if (!this.user) return;

        // Update user info display
        const userInfoElements = document.querySelectorAll('.user-info');
        userInfoElements.forEach(elem => {
            elem.innerHTML = `
                <span class="user-name">👤 ${this.user.full_name || this.user.username}</span>
                <span class="user-role">(${this.user.role})</span>
                <button onclick="auth.logout()" class="logout-btn">Logout</button>
            `;
        });

        // Hide/show elements based on permissions
        document.querySelectorAll('[data-permission]').forEach(elem => {
            const permission = elem.getAttribute('data-permission');
            if (!this.hasPermission(permission)) {
                elem.style.display = 'none';
            }
        });

        // Add user indicator to header
        const header = document.querySelector('.dashboard-header');
        if (header && !header.querySelector('.user-info')) {
            const userDiv = document.createElement('div');
            userDiv.className = 'user-info';
            userDiv.style.cssText = `
                position: absolute;
                top: 20px;
                right: 20px;
                background: rgba(255, 255, 255, 0.1);
                padding: 10px 20px;
                border-radius: 10px;
                color: white;
                display: flex;
                align-items: center;
                gap: 10px;
                backdrop-filter: blur(10px);
            `;
            userDiv.innerHTML = `
                <span class="user-name">👤 ${this.user.full_name || this.user.username}</span>
                <span class="user-role" style="opacity: 0.8;">(${this.user.role})</span>
                <button onclick="auth.logout()" class="logout-btn" style="
                    background: rgba(255, 255, 255, 0.2);
                    border: 1px solid rgba(255, 255, 255, 0.3);
                    color: white;
                    padding: 5px 15px;
                    border-radius: 5px;
                    cursor: pointer;
                    transition: all 0.3s ease;
                ">Logout</button>
            `;
            header.appendChild(userDiv);
        }
    }

    requireAuth() {
        if (!this.isAuthenticated()) {
            window.location.href = '/login';
            return false;
        }
        return true;
    }

    requirePermission(permission) {
        if (!this.requireAuth()) return false;

        if (!this.hasPermission(permission)) {
            alert(`Permission denied. You need "${permission}" permission to access this feature.`);
            return false;
        }
        return true;
    }
}

// Create global auth instance
const auth = new AuthManager();

// Check authentication on page load
document.addEventListener('DOMContentLoaded', async () => {
    // Skip auth check on login page
    if (window.location.pathname === '/login') return;

    if (!auth.isAuthenticated()) {
        window.location.href = '/login';
        return;
    }

    // Verify token is still valid
    const isValid = await auth.verifyToken();
    if (!isValid) {
        window.location.href = '/login';
        return;
    }

    // Update UI for authenticated user
    auth.updateUIForUser();
});

// Add auth headers to all API calls
const originalFetch = window.fetch;
window.fetch = function(url, options = {}) {
    // Only add auth header to API calls
    if (url.startsWith('/api/') && auth.token) {
        options.headers = {
            ...options.headers,
            'Authorization': `Bearer ${auth.token}`
        };
    }
    return originalFetch(url, options);
};