// Expense Tracker Mobile App - Utility Functions

// Global app configuration
const ExpenseTracker = {
    // Formatting utilities
    formatCurrency: (amount) => {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    },

    formatDate: (dateString) => {
        return new Intl.DateTimeFormat('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        }).format(new Date(dateString));
    },

    // Form validation utilities
    validateEmail: (email) => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    },

    validateAmount: (amount) => {
        const num = parseFloat(amount);
        return !isNaN(num) && num > 0 && num < 1000000;
    },

    // UI utilities
    showAlert: (message, type = 'info') => {
        const alertContainer = document.createElement('div');
        alertContainer.className = `alert alert-${type} fixed top-4 left-4 right-4 z-50`;
        alertContainer.innerHTML = `
            <div class="flex items-center justify-between">
                <span>${message}</span>
                <button onclick="this.parentElement.parentElement.remove()" class="ml-2 text-current opacity-70 hover:opacity-100">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        document.body.appendChild(alertContainer);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (alertContainer.parentElement) {
                alertContainer.remove();
            }
        }, 5000);
    },

    showLoader: (element) => {
        const originalContent = element.innerHTML;
        element.innerHTML = '<span class="spinner"></span>Loading...';
        element.disabled = true;
        
        return () => {
            element.innerHTML = originalContent;
            element.disabled = false;
        };
    },

    // Local storage utilities
    storage: {
        set: (key, value) => {
            try {
                localStorage.setItem(`expense_tracker_${key}`, JSON.stringify(value));
            } catch (e) {
                console.warn('Failed to save to localStorage:', e);
            }
        },

        get: (key, defaultValue = null) => {
            try {
                const item = localStorage.getItem(`expense_tracker_${key}`);
                return item ? JSON.parse(item) : defaultValue;
            } catch (e) {
                console.warn('Failed to read from localStorage:', e);
                return defaultValue;
            }
        },

        remove: (key) => {
            try {
                localStorage.removeItem(`expense_tracker_${key}`);
            } catch (e) {
                console.warn('Failed to remove from localStorage:', e);
            }
        }
    },

    // Network utilities
    api: {
        get: async (url) => {
            try {
                const response = await fetch(url);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return await response.json();
            } catch (error) {
                console.error('API GET error:', error);
                throw error;
            }
        },

        post: async (url, data) => {
            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return await response.json();
            } catch (error) {
                console.error('API POST error:', error);
                throw error;
            }
        }
    },

    // PWA utilities
    pwa: {
        isInstallable: false,
        deferredPrompt: null,

        init: () => {
            // Check if app is already installed
            if (window.matchMedia('(display-mode: standalone)').matches) {
                console.log('App is running in standalone mode');
                return;
            }

            // Listen for install prompt
            window.addEventListener('beforeinstallprompt', (e) => {
                e.preventDefault();
                ExpenseTracker.pwa.deferredPrompt = e;
                ExpenseTracker.pwa.isInstallable = true;
                ExpenseTracker.pwa.showInstallBanner();
            });

            // Listen for successful installation
            window.addEventListener('appinstalled', (e) => {
                console.log('App was installed');
                ExpenseTracker.pwa.hideInstallBanner();
            });
        },

        install: async () => {
            if (!ExpenseTracker.pwa.deferredPrompt) {
                return false;
            }

            ExpenseTracker.pwa.deferredPrompt.prompt();
            const { outcome } = await ExpenseTracker.pwa.deferredPrompt.userChoice;
            
            if (outcome === 'accepted') {
                console.log('User accepted the install prompt');
            }
            
            ExpenseTracker.pwa.deferredPrompt = null;
            return outcome === 'accepted';
        },

        showInstallBanner: () => {
            const banner = document.createElement('div');
            banner.id = 'install-banner';
            banner.className = 'fixed top-20 left-4 right-4 bg-blue-500 text-white p-4 rounded-lg shadow-lg z-50';
            banner.innerHTML = `
                <div class="flex items-center justify-between">
                    <div>
                        <p class="font-medium">Install App</p>
                        <p class="text-sm opacity-90">Add to home screen for better experience</p>
                    </div>
                    <div class="flex gap-2">
                        <button onclick="ExpenseTracker.pwa.install()" class="bg-white text-blue-500 px-3 py-1 rounded text-sm font-medium">
                            Install
                        </button>
                        <button onclick="ExpenseTracker.pwa.hideInstallBanner()" class="text-white opacity-70 hover:opacity-100">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                </div>
            `;
            document.body.appendChild(banner);

            // Auto-hide after 10 seconds
            setTimeout(() => {
                ExpenseTracker.pwa.hideInstallBanner();
            }, 10000);
        },

        hideInstallBanner: () => {
            const banner = document.getElementById('install-banner');
            if (banner) {
                banner.remove();
            }
        }
    },

    // Theme utilities
    theme: {
        init: () => {
            const saved = ExpenseTracker.storage.get('theme', 'light');
            ExpenseTracker.theme.set(saved);
        },

        set: (theme) => {
            document.documentElement.classList.toggle('dark', theme === 'dark');
            ExpenseTracker.storage.set('theme', theme);
        },

        toggle: () => {
            const current = document.documentElement.classList.contains('dark') ? 'dark' : 'light';
            const newTheme = current === 'dark' ? 'light' : 'dark';
            ExpenseTracker.theme.set(newTheme);
            return newTheme;
        }
    }
};

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('Expense Tracker App initialized');
    
    // Initialize PWA
    ExpenseTracker.pwa.init();
    
    // Initialize theme
    ExpenseTracker.theme.init();
    
    // Add global error handler
    window.addEventListener('error', (e) => {
        console.error('Global error:', e.error);
        ExpenseTracker.showAlert('An unexpected error occurred. Please refresh the page.', 'error');
    });
    
    // Add offline/online handlers
    window.addEventListener('online', () => {
        ExpenseTracker.showAlert('Connection restored', 'success');
    });
    
    window.addEventListener('offline', () => {
        ExpenseTracker.showAlert('Connection lost - some features may be unavailable', 'warning');
    });
});

// Export for global use
window.ExpenseTracker = ExpenseTracker;