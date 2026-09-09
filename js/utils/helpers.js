/**
 * FreightForecast Pro — Utility Helpers
 * Formatting, statistics, DOM utilities.
 */

// ================================================================
//  FORMATTING
// ================================================================

/**
 * Format currency (USD)
 */
export function formatCurrency(value, decimals = 0) {
  if (value == null || isNaN(value)) return '—';
  return '$' + Number(value).toLocaleString('en-US', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
}

/**
 * Format number with locale
 */
export function formatNumber(value, decimals = 0) {
  if (value == null || isNaN(value)) return '—';
  return Number(value).toLocaleString('en-US', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
}

/**
 * Format percentage
 */
export function formatPercent(value, decimals = 1) {
  if (value == null || isNaN(value)) return '—';
  const sign = value > 0 ? '+' : '';
  return sign + value.toFixed(decimals) + '%';
}

/**
 * Format date for display
 */
export function formatDateDisplay(dateStr) {
  const d = new Date(dateStr);
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

/**
 * Format date short
 */
export function formatDateShort(dateStr) {
  const d = new Date(dateStr);
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
}

/**
 * Format days (e.g., "12.5 days")
 */
export function formatDays(days) {
  if (days == null) return '—';
  return days.toFixed(1) + ' days';
}

/**
 * Format metric tonnes
 */
export function formatMT(mt) {
  if (mt >= 1000000) return (mt / 1000000).toFixed(1) + 'M MT';
  if (mt >= 1000) return (mt / 1000).toFixed(0) + 'k MT';
  return formatNumber(mt) + ' MT';
}

/**
 * Format nautical miles
 */
export function formatNM(nm) {
  return formatNumber(nm) + ' NM';
}


// ================================================================
//  STATISTICS
// ================================================================

export function mean(arr) {
  if (!arr.length) return 0;
  return arr.reduce((a, b) => a + b, 0) / arr.length;
}

export function stddev(arr) {
  if (!arr.length) return 0;
  const m = mean(arr);
  const variance = arr.reduce((sum, val) => sum + (val - m) ** 2, 0) / arr.length;
  return Math.sqrt(variance);
}

export function percentile(arr, p) {
  const sorted = [...arr].sort((a, b) => a - b);
  const idx = (p / 100) * (sorted.length - 1);
  const lower = Math.floor(idx);
  const upper = Math.ceil(idx);
  if (lower === upper) return sorted[lower];
  return sorted[lower] + (sorted[upper] - sorted[lower]) * (idx - lower);
}

export function min(arr) { return Math.min(...arr); }
export function max(arr) { return Math.max(...arr); }

export function correlation(x, y) {
  const n = Math.min(x.length, y.length);
  const mx = mean(x.slice(0, n));
  const my = mean(y.slice(0, n));
  let num = 0, dx = 0, dy = 0;
  for (let i = 0; i < n; i++) {
    num += (x[i] - mx) * (y[i] - my);
    dx += (x[i] - mx) ** 2;
    dy += (y[i] - my) ** 2;
  }
  return num / Math.sqrt(dx * dy);
}


// ================================================================
//  DOM UTILITIES
// ================================================================

/**
 * Select element by ID
 */
export function $(id) {
  return document.getElementById(id);
}

/**
 * Select element by CSS selector
 */
export function $$(selector) {
  return document.querySelector(selector);
}

/**
 * Select all elements by CSS selector
 */
export function $$$(selector) {
  return document.querySelectorAll(selector);
}

/**
 * Create HTML element from string
 */
export function html(htmlStr) {
  const template = document.createElement('template');
  template.innerHTML = htmlStr.trim();
  return template.content.firstChild;
}

/**
 * Set innerHTML safely
 */
export function setHTML(element, content) {
  if (typeof element === 'string') element = $(element);
  if (element) element.innerHTML = content;
}

/**
 * Show/hide element
 */
export function show(element) {
  if (typeof element === 'string') element = $(element);
  if (element) element.style.display = '';
}

export function hide(element) {
  if (typeof element === 'string') element = $(element);
  if (element) element.style.display = 'none';
}

/**
 * Add/remove CSS class
 */
export function addClass(element, cls) {
  if (typeof element === 'string') element = $(element);
  if (element) element.classList.add(cls);
}

export function removeClass(element, cls) {
  if (typeof element === 'string') element = $(element);
  if (element) element.classList.remove(cls);
}

export function toggleClass(element, cls) {
  if (typeof element === 'string') element = $(element);
  if (element) element.classList.toggle(cls);
}


// ================================================================
//  DEBOUNCE / THROTTLE
// ================================================================

export function debounce(fn, delay = 300) {
  let timer;
  return function (...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}

export function throttle(fn, limit = 100) {
  let lastCall = 0;
  return function (...args) {
    const now = Date.now();
    if (now - lastCall >= limit) {
      lastCall = now;
      fn.apply(this, args);
    }
  };
}


// ================================================================
//  MISC
// ================================================================

/**
 * Generate date range strings
 */
export function dateRange(startStr, endStr) {
  const dates = [];
  const current = new Date(startStr);
  const end = new Date(endStr);
  while (current <= end) {
    dates.push(current.toISOString().split('T')[0]);
    current.setDate(current.getDate() + 1);
  }
  return dates;
}

/**
 * Get last N items from an array
 */
export function lastN(arr, n) {
  return arr.slice(Math.max(0, arr.length - n));
}

/**
 * Get trend arrow HTML
 */
export function trendArrow(value) {
  if (value > 0) return '<span class="text-emerald">▲</span>';
  if (value < 0) return '<span class="text-rose">▼</span>';
  return '<span class="text-muted">—</span>';
}

/**
 * Get trend class
 */
export function trendClass(value) {
  if (value > 0) return 'up';
  if (value < 0) return 'down';
  return 'flat';
}

/**
 * Create SVG gauge arc path
 */
export function gaugeArc(value, max = 100, radius = 60, thickness = 10) {
  const percentage = Math.min(value / max, 1);
  const startAngle = -Math.PI;
  const endAngle = startAngle + Math.PI * percentage;
  const cx = 70;
  const cy = 70;

  const x1 = cx + radius * Math.cos(startAngle);
  const y1 = cy + radius * Math.sin(startAngle);
  const x2 = cx + radius * Math.cos(endAngle);
  const y2 = cy + radius * Math.sin(endAngle);

  const largeArc = percentage > 0.5 ? 1 : 0;

  return `M ${x1} ${y1} A ${radius} ${radius} 0 ${largeArc} 1 ${x2} ${y2}`;
}
