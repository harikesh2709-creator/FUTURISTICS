/**
 * FreightForecast Pro — Chart Manager
 * Chart.js configuration factory with dark maritime theme.
 */

/**
 * Dark theme defaults for Chart.js
 */
export const CHART_THEME = {
  font: { family: "'Inter', sans-serif", size: 12 },
  monoFont: { family: "'JetBrains Mono', monospace", size: 11 },
  colors: {
    grid: 'rgba(255, 255, 255, 0.04)',
    gridBorder: 'rgba(255, 255, 255, 0.08)',
    text: '#94a3b8',
    textMuted: '#64748b',
    tooltip: {
      bg: '#131b2e',
      border: 'rgba(255, 255, 255, 0.1)',
      title: '#f0f4f8',
      body: '#94a3b8',
    },
  },
  series: {
    handysize: { color: '#22c55e', bg: 'rgba(34, 197, 94, 0.1)' },
    supramax:  { color: '#38bdf8', bg: 'rgba(56, 189, 248, 0.1)' },
    panamax:   { color: '#f59e0b', bg: 'rgba(245, 158, 11, 0.1)' },
    capesize:  { color: '#a855f7', bg: 'rgba(168, 85, 247, 0.1)' },
    forecast:  { color: '#06b6d4', bg: 'rgba(6, 182, 212, 0.08)' },
    ci80:      { color: 'rgba(6, 182, 212, 0.2)' },
    ci95:      { color: 'rgba(6, 182, 212, 0.08)' },
    actual:    { color: '#e2e8f0', bg: 'rgba(226, 232, 240, 0.05)' },
    danger:    { color: '#ef4444', bg: 'rgba(239, 68, 68, 0.1)' },
    success:   { color: '#10b981', bg: 'rgba(16, 185, 129, 0.1)' },
  },
};


/**
 * Apply global Chart.js defaults
 */
export function applyChartDefaults() {
  if (!window.Chart) return;

  Chart.defaults.color = CHART_THEME.colors.text;
  Chart.defaults.font.family = CHART_THEME.font.family;
  Chart.defaults.font.size = CHART_THEME.font.size;
  Chart.defaults.plugins.legend.display = false;
  Chart.defaults.plugins.tooltip.backgroundColor = CHART_THEME.colors.tooltip.bg;
  Chart.defaults.plugins.tooltip.borderColor = CHART_THEME.colors.tooltip.border;
  Chart.defaults.plugins.tooltip.borderWidth = 1;
  Chart.defaults.plugins.tooltip.titleColor = CHART_THEME.colors.tooltip.title;
  Chart.defaults.plugins.tooltip.bodyColor = CHART_THEME.colors.tooltip.body;
  Chart.defaults.plugins.tooltip.padding = 12;
  Chart.defaults.plugins.tooltip.cornerRadius = 8;
  Chart.defaults.plugins.tooltip.titleFont = { weight: '600', size: 13 };
  Chart.defaults.plugins.tooltip.bodyFont = { family: "'JetBrains Mono', monospace", size: 12 };
  Chart.defaults.plugins.tooltip.displayColors = true;
  Chart.defaults.plugins.tooltip.boxPadding = 4;
  Chart.defaults.elements.point.radius = 0;
  Chart.defaults.elements.point.hoverRadius = 5;
  Chart.defaults.elements.point.hoverBorderWidth = 2;
  Chart.defaults.elements.line.borderWidth = 2;
  Chart.defaults.elements.line.tension = 0.3;
  Chart.defaults.animation.duration = 600;
  Chart.defaults.animation.easing = 'easeOutQuart';
  Chart.defaults.responsive = true;
  Chart.defaults.maintainAspectRatio = false;
}


/**
 * Create a gradient fill for area charts.
 */
export function createGradient(ctx, color, opacity1 = 0.3, opacity2 = 0) {
  const gradient = ctx.createLinearGradient(0, 0, 0, ctx.canvas.height);
  gradient.addColorStop(0, color.replace(')', `, ${opacity1})`).replace('rgb', 'rgba').replace('rgbaa','rgba'));

  // Parse and apply with second opacity
  const match = color.match(/\d+/g);
  if (match && match.length >= 3) {
    gradient.addColorStop(1, `rgba(${match[0]}, ${match[1]}, ${match[2]}, ${opacity2})`);
  } else {
    gradient.addColorStop(1, 'transparent');
  }
  return gradient;
}

/**
 * Create gradient from hex color
 */
export function createGradientFromHex(ctx, hex, opacity1 = 0.3, opacity2 = 0) {
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);

  const gradient = ctx.createLinearGradient(0, 0, 0, ctx.canvas.height);
  gradient.addColorStop(0, `rgba(${r}, ${g}, ${b}, ${opacity1})`);
  gradient.addColorStop(1, `rgba(${r}, ${g}, ${b}, ${opacity2})`);
  return gradient;
}


/**
 * Standard axis config for time series charts
 */
export function timeSeriesAxes(unit = 'month') {
  return {
    x: {
      type: 'time',
      time: {
        unit,
        displayFormats: {
          day: 'MMM d',
          week: 'MMM d',
          month: 'MMM yyyy',
        },
      },
      grid: {
        color: CHART_THEME.colors.grid,
        drawBorder: false,
      },
      ticks: {
        color: CHART_THEME.colors.textMuted,
        font: { size: 11 },
        maxRotation: 0,
        autoSkip: true,
        maxTicksLimit: 12,
      },
    },
    y: {
      grid: {
        color: CHART_THEME.colors.grid,
        drawBorder: false,
      },
      ticks: {
        color: CHART_THEME.colors.text,
        font: { family: "'JetBrains Mono', monospace", size: 11 },
        callback: (value) => '$' + value.toLocaleString(),
      },
      border: { display: false },
    },
  };
}

/**
 * Standard axis for category charts (bar charts, etc.)
 */
export function categoryAxes() {
  return {
    x: {
      grid: { display: false },
      ticks: { color: CHART_THEME.colors.text, font: { size: 11 } },
    },
    y: {
      grid: {
        color: CHART_THEME.colors.grid,
        drawBorder: false,
      },
      ticks: {
        color: CHART_THEME.colors.text,
        font: { family: "'JetBrains Mono', monospace", size: 11 },
      },
      border: { display: false },
    },
  };
}


/**
 * Create or update a Chart.js chart instance
 */
export function createChart(canvasId, config) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return null;

  // Destroy existing chart on this canvas
  const existingChart = Chart.getChart(canvas);
  if (existingChart) existingChart.destroy();

  return new Chart(canvas.getContext('2d'), config);
}


/**
 * Create a forecast line chart with confidence bands
 */
export function createForecastChart(canvasId, historicalDates, historicalRates, forecastDates, forecastValues, intervals, vesselColor = '#06b6d4') {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return null;
  const ctx = canvas.getContext('2d');

  const allDates = [...historicalDates, ...forecastDates];
  const actualLine = [...historicalRates, ...new Array(forecastDates.length).fill(null)];
  const forecastLine = [...new Array(historicalRates.length).fill(null), ...forecastValues];

  // Confidence bands
  const upper95 = [...new Array(historicalRates.length).fill(null), ...intervals.map(i => i.upper95)];
  const lower95 = [...new Array(historicalRates.length).fill(null), ...intervals.map(i => i.lower95)];
  const upper80 = [...new Array(historicalRates.length).fill(null), ...intervals.map(i => i.upper80)];
  const lower80 = [...new Array(historicalRates.length).fill(null), ...intervals.map(i => i.lower80)];

  return createChart(canvasId, {
    type: 'line',
    data: {
      labels: allDates,
      datasets: [
        {
          label: '95% CI Upper',
          data: upper95,
          borderColor: 'transparent',
          backgroundColor: CHART_THEME.series.ci95.color,
          fill: '+1',
          pointRadius: 0,
          order: 5,
        },
        {
          label: '95% CI Lower',
          data: lower95,
          borderColor: 'transparent',
          backgroundColor: 'transparent',
          fill: false,
          pointRadius: 0,
          order: 5,
        },
        {
          label: '80% CI Upper',
          data: upper80,
          borderColor: 'transparent',
          backgroundColor: CHART_THEME.series.ci80.color,
          fill: '+1',
          pointRadius: 0,
          order: 4,
        },
        {
          label: '80% CI Lower',
          data: lower80,
          borderColor: 'transparent',
          backgroundColor: 'transparent',
          fill: false,
          pointRadius: 0,
          order: 4,
        },
        {
          label: 'Forecast',
          data: forecastLine,
          borderColor: vesselColor,
          borderDash: [6, 3],
          borderWidth: 2.5,
          backgroundColor: createGradientFromHex(ctx, vesselColor, 0.15, 0),
          fill: true,
          pointRadius: 0,
          order: 2,
        },
        {
          label: 'Actual',
          data: actualLine,
          borderColor: '#e2e8f0',
          borderWidth: 1.5,
          backgroundColor: createGradientFromHex(ctx, '#e2e8f0', 0.05, 0),
          fill: true,
          pointRadius: 0,
          order: 1,
        },
      ],
    },
    options: {
      interaction: { mode: 'index', intersect: false },
      scales: {
        x: {
          grid: { color: CHART_THEME.colors.grid, drawBorder: false },
          ticks: {
            color: CHART_THEME.colors.textMuted,
            font: { size: 10 },
            maxRotation: 0,
            autoSkip: true,
            maxTicksLimit: 10,
          },
        },
        y: {
          grid: { color: CHART_THEME.colors.grid, drawBorder: false },
          ticks: {
            color: CHART_THEME.colors.text,
            font: { family: "'JetBrains Mono', monospace", size: 11 },
            callback: (v) => '$' + v.toLocaleString(),
          },
          border: { display: false },
        },
      },
      plugins: {
        tooltip: {
          filter: (item) => item.dataset.label === 'Actual' || item.dataset.label === 'Forecast',
          callbacks: {
            label: (ctx) => `${ctx.dataset.label}: $${ctx.parsed.y?.toLocaleString() || 'N/A'}/day`,
          },
        },
        annotation: {
          annotations: {
            forecastLine: {
              type: 'line',
              xMin: historicalDates.length - 1,
              xMax: historicalDates.length - 1,
              borderColor: 'rgba(6, 182, 212, 0.4)',
              borderWidth: 1,
              borderDash: [4, 4],
              label: {
                display: true,
                content: 'Forecast →',
                position: 'start',
                backgroundColor: 'rgba(6, 182, 212, 0.15)',
                color: '#06b6d4',
                font: { size: 10, weight: '600' },
                padding: { x: 6, y: 3 },
              },
            },
          },
        },
      },
    },
  });
}


/**
 * Create a sparkline (mini chart)
 */
export function createSparkline(canvasId, data, color = '#06b6d4') {
  return createChart(canvasId, {
    type: 'line',
    data: {
      labels: data.map((_, i) => i),
      datasets: [{
        data,
        borderColor: color,
        borderWidth: 1.5,
        pointRadius: 0,
        tension: 0.4,
        fill: false,
      }],
    },
    options: {
      animation: false,
      scales: { x: { display: false }, y: { display: false } },
      plugins: { legend: { display: false }, tooltip: { enabled: false } },
    },
  });
}
