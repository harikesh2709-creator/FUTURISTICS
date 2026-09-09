/**
 * FreightForecast Pro — Real-Time Notification Toast System
 * Displays glassmorphic notifications for rate alerts, weather hazards,
 * and port congestion changes without breaking user workflow.
 */

class NotificationToastManager {
  constructor() {
    this.container = null;
    this.init();
  }

  init() {
    if (document.getElementById('toast-container')) {
      this.container = document.getElementById('toast-container');
      return;
    }

    this.container = document.createElement('div');
    this.container.id = 'toast-container';
    this.container.className = 'toast-container';
    document.body.appendChild(this.container);
  }

  show(options) {
    if (!this.container) this.init();

    const {
      title = 'System Alert',
      message = '',
      type = 'info', // 'info', 'warning', 'critical', 'success'
      duration = 6000
    } = options;

    const icons = {
      info: 'ℹ️',
      warning: '⚠️',
      critical: '🚨',
      success: '✅'
    };

    const toast = document.createElement('div');
    toast.className = `toast-item toast-${type}`;
    toast.innerHTML = `
      <div class="toast-icon">${icons[type] || '🔔'}</div>
      <div class="toast-body">
        <div class="toast-title">${title}</div>
        <div class="toast-message">${message}</div>
      </div>
      <button class="toast-close" aria-label="Close">&times;</button>
    `;

    // Click to dismiss
    toast.querySelector('.toast-close').addEventListener('click', () => {
      this.dismiss(toast);
    });

    this.container.appendChild(toast);

    // Auto dismiss
    if (duration > 0) {
      setTimeout(() => {
        this.dismiss(toast);
      }, duration);
    }
  }

  dismiss(toast) {
    if (!toast || !toast.parentNode) return;
    toast.classList.add('toast-hiding');
    setTimeout(() => {
      if (toast.parentNode) {
        toast.parentNode.removeChild(toast);
      }
    }, 300);
  }
}

export const toastManager = new NotificationToastManager();
