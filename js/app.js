/**
 * FreightForecast Pro — Main Application Controller
 * State management, panel routing, data orchestration, rendering.
 */

import { PORTS, getDischargePorts, getLoadingPorts, canVesselBerth, estimateTurnaround, getSeasonalRisk } from './data/portDatabase.js';
import { VESSEL_CLASSES, getVesselClasses } from './data/vesselDatabase.js';
import { ROUTES, findRoute, getRoutesFromOrigin, getRoutesToDest, getAllRoutes } from './data/routeDatabase.js';
import { generateAllData, generateFreightRates, generateCongestionData } from './data/syntheticData.js';
import { runForecast } from './models/forecastEngine.js';
import { optimizeVessel, compareContracts } from './models/vesselOptimizer.js';
import { marketEntryScore, generateRiskAlerts, rollingVolatility, analyzeIdleScenarios } from './models/riskAnalyzer.js';
import { initTelematicsMap } from './models/telematicsEngine.js';
import { initAIAssistant } from './models/aiEngine.js';
import { applyChartDefaults, createChart, createForecastChart, createGradientFromHex, CHART_THEME } from './utils/chartManager.js';
import { formatCurrency, formatNumber, formatPercent, formatDays, formatMT, formatNM, formatDateDisplay, $, setHTML, trendArrow, trendClass, lastN, gaugeArc, mean } from './utils/helpers.js';
import { wsClient } from './utils/wsClient.js';
import { toastManager } from './utils/notificationToast.js';


// ================================================================
//  APPLICATION STATE
// ================================================================

const state = {
  activePanel: 'forecast',
  data: null,
  forecastResults: {},
  selectedVessel: 'CAPESIZE',
  forecastHorizon: 90,
  historyDays: 365,
  wsStatus: 'CONNECTING',
  latencyMs: null,
  liveRates: {}
};


// ================================================================
//  INITIALIZATION
// ================================================================

document.addEventListener('DOMContentLoaded', () => {
  console.log('FreightForecast Pro — Initializing...');

  // Apply Chart.js theme
  applyChartDefaults();

  // Generate synthetic data
  state.data = generateAllData(3, 42);

  // Setup navigation
  setupNavigation();

  // Load saved preferences
  loadPreferences();

  // Populate select dropdowns
  populateSelects();

  // Start clock
  updateClock();
  setInterval(updateClock, 60000);

  // Run initial forecast
  runForecastPanel();

  // Setup event listeners
  setupEventListeners();

  // Update KPI bar
  updateKPIBar();

  // Initialize Real-Time WebSocket
  initWebSocket();

  // Expose app for sidebar toggle
  window.app = { toggleSidebar };

  console.log('FreightForecast Pro — Ready');
});


// ================================================================
//  NAVIGATION
// ================================================================

function setupNavigation() {
  const navItems = document.querySelectorAll('.nav-item[data-panel]');
  navItems.forEach(item => {
    item.addEventListener('click', () => {
      const panelId = item.dataset.panel;
      switchPanel(panelId);
    });
  });
}

function switchPanel(panelId) {
  // Update nav active state
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  const activeNav = document.querySelector(`.nav-item[data-panel="${panelId}"]`);
  if (activeNav) activeNav.classList.add('active');

  // Update panel visibility
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  const activePanel = $(`panel-${panelId}`);
  if (activePanel) activePanel.classList.add('active');

  // Update title
  const titles = {
    forecast: 'Rate Forecast',
    vessel: 'Vessel Optimizer',
    route: 'Route Analysis',
    port: 'Port Infrastructure',
    risk: 'Risk Alerts',
    contract: 'Contract Strategy',
    idle: 'Idle Management',
    telematics: 'Global Fleet Telematics',
    ai: 'Freight AI Assistant'
  };
  setHTML('pageTitle', titles[panelId] || panelId);

  state.activePanel = panelId;

  // Lazy-load panels
  if (panelId === 'port') renderPortPanel();
  if (panelId === 'risk') renderRiskPanel();
  if (panelId === 'telematics') {
    setTimeout(() => {
      initTelematicsMap('map-container');
    }, 100);
  }
  if (panelId === 'ai') {
    initAIAssistant();
  }
}

function toggleSidebar() {
  const sidebar = $('sidebar');
  sidebar.classList.toggle('collapsed');
}


// ================================================================
//  POPULATE SELECTS
// ================================================================

function populateSelects() {
  const loadPorts = getLoadingPorts();
  const dischPorts = getDischargePorts();

  // Vessel optimizer
  populatePortSelect('vesselOriginSelect', loadPorts);
  populatePortSelect('vesselDestSelect', dischPorts);

  // Route analysis
  populatePortSelect('routeOriginSelect', loadPorts);

  // Idle management
  populatePortSelect('idlePortSelect', dischPorts);
}

function populatePortSelect(selectId, ports) {
  const select = $(selectId);
  if (!select) return;
  select.innerHTML = ports.map(p =>
    `<option value="${p.id}">${p.name} (${p.country})</option>`
  ).join('');
}


// ================================================================
//  EVENT LISTENERS
// ================================================================

function setupEventListeners() {
  // Forecast controls
  $('runForecastBtn')?.addEventListener('click', runForecastPanel);
  $('forecastVesselSelect')?.addEventListener('change', runForecastPanel);
  $('forecastHorizonSelect')?.addEventListener('change', runForecastPanel);

  // History period buttons
  document.querySelectorAll('#historyPeriodGroup .btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('#historyPeriodGroup .btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      state.historyDays = parseInt(btn.dataset.period);
      runForecastPanel();
    });
  });

  // Vessel optimizer
  $('optimizeVesselBtn')?.addEventListener('click', runVesselOptimizer);

  // Route comparison
  $('compareRoutesBtn')?.addEventListener('click', runRouteComparison);

  // Port type toggle
  document.querySelectorAll('#portTypeGroup .btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('#portTypeGroup .btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderPortPanel(btn.dataset.type);
    });
  });

  // Contract analyzer
  $('analyzeContractBtn')?.addEventListener('click', runContractAnalysis);

  // Idle analyzer
  $('analyzeIdleBtn')?.addEventListener('click', runIdleAnalysis);
}


// ================================================================
//  KPI BAR
// ================================================================

function updateKPIBar() {
  const bdi = state.data.bdi;
  const latest = bdi[bdi.length - 1];
  const prev = bdi[bdi.length - 2];
  const bdiChange = ((latest.bdi - prev.bdi) / prev.bdi * 100);

  const capeRate = state.data.rates.CAPESIZE;
  const latestCape = capeRate[capeRate.length - 1].rate;
  const prevCape = capeRate[capeRate.length - 8].rate;
  const capeChange = ((latestCape - prevCape) / prevCape * 100);

  const kpiHtml = `
    <div class="kpi-item" id="kpi-bdi-item">
      <span class="kpi-label">BDI</span>
      <span class="kpi-value" id="kpi-bdi-val">${formatNumber(latest.bdi)}</span>
      <span class="kpi-change ${trendClass(bdiChange)}">${trendArrow(bdiChange)} ${formatPercent(bdiChange)}</span>
    </div>
    <div class="kpi-item" id="kpi-cape-item">
      <span class="kpi-label">Cape</span>
      <span class="kpi-value" id="kpi-cape-val">${formatCurrency(latestCape)}</span>
      <span class="kpi-change ${trendClass(capeChange)}">${formatPercent(capeChange)}</span>
    </div>
    <div class="kpi-item" id="kpi-coal-item">
      <span class="kpi-label">Coal</span>
      <span class="kpi-value" id="kpi-coal-val">${formatCurrency(state.data.coal[state.data.coal.length - 1].price, 1)}</span>
    </div>
  `;
  setHTML('kpiBar', kpiHtml);
}

function updateClock() {
  const now = new Date();
  setHTML('clockDisplay', now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }) + ' IST');
}


// ================================================================
//  FORECAST PANEL
// ================================================================

function runForecastPanel() {
  const vesselId = $('forecastVesselSelect')?.value || 'CAPESIZE';
  const horizon = parseInt($('forecastHorizonSelect')?.value || '90');
  const vessel = VESSEL_CLASSES[vesselId];

  state.selectedVessel = vesselId;
  state.forecastHorizon = horizon;
  savePreferences();

  // Get rate data (trim to history window)
  const allRates = state.data.rates[vesselId];
  const rates = lastN(allRates, state.historyDays);

  // Run forecast
  const results = runForecast(rates, horizon);
  state.forecastResults[vesselId] = results;

  // Update subtitle
  setHTML('forecastChartSubtitle', `TC Rate ($/day) — ${vessel.name}`);

  // Render stat cards
  renderForecastStats(results, vessel);

  // Render main chart
  renderForecastChart(results, vessel);

  // Render market entry score
  renderMarketEntryScore(rates, results);

  // Render decomposition charts
  renderDecompositionCharts(results);

  // Render accuracy metrics
  renderAccuracyMetrics(results);

  // Update risk badge
  updateRiskBadge(rates, results);
}

function renderForecastStats(results, vessel) {
  const { trend, accuracy } = results;
  const change = trend.currentRate - trend.avgRate30d;
  const changePct = (change / trend.avgRate30d) * 100;

  const forecastAvg = Math.round(mean(results.forecast.values));
  const forecastChange = ((forecastAvg - trend.currentRate) / trend.currentRate) * 100;

  setHTML('forecastStats', `
    <div class="stat-card animate-fade-in stagger-1">
      <div class="stat-header">
        <div class="stat-icon" style="background: rgba(6, 182, 212, 0.15); color: var(--accent-cyan);">📊</div>
        <span class="stat-label">Current Rate</span>
      </div>
      <div class="stat-value">${formatCurrency(trend.currentRate)}</div>
      <div class="stat-change ${trendClass(changePct)}">
        ${trendArrow(changePct)} ${formatPercent(changePct)} vs 30d avg
      </div>
    </div>
    <div class="stat-card animate-fade-in stagger-2">
      <div class="stat-header">
        <div class="stat-icon" style="background: rgba(168, 85, 247, 0.15); color: var(--accent-purple);">🔮</div>
        <span class="stat-label">Forecast Avg (${state.forecastHorizon}d)</span>
      </div>
      <div class="stat-value">${formatCurrency(forecastAvg)}</div>
      <div class="stat-change ${trendClass(forecastChange)}">
        ${trendArrow(forecastChange)} ${formatPercent(forecastChange)} from current
      </div>
    </div>
    <div class="stat-card animate-fade-in stagger-3">
      <div class="stat-header">
        <div class="stat-icon" style="background: rgba(245, 158, 11, 0.15); color: var(--accent-amber);">📈</div>
        <span class="stat-label">30d Trend</span>
      </div>
      <div class="stat-value">${trend.direction === 'rising' ? '▲ Rising' : '▼ Falling'}</div>
      <div class="stat-change ${trendClass(trend.magnitude)}">
        ${formatPercent(trend.magnitude)} momentum
      </div>
    </div>
    <div class="stat-card animate-fade-in stagger-4">
      <div class="stat-header">
        <div class="stat-icon" style="background: rgba(16, 185, 129, 0.15); color: var(--accent-emerald);">🎯</div>
        <span class="stat-label">Forecast MAPE</span>
      </div>
      <div class="stat-value">${accuracy.mape.toFixed(1)}%</div>
      <div class="stat-change" style="color: var(--text-tertiary);">
        MAE: ${formatCurrency(accuracy.mae)}
      </div>
    </div>
  `);
}

function renderForecastChart(results, vessel) {
  const { historical, forecast } = results;

  // Trim history for display
  const displayDays = state.historyDays;
  const histDates = lastN(historical.dates, displayDays);
  const histRates = lastN(historical.rates, displayDays);

  createForecastChart(
    'mainForecastChart',
    histDates,
    histRates,
    forecast.dates,
    forecast.values,
    forecast.intervals,
    vessel.color
  );

  // Render legend
  setHTML('forecastLegend', `
    <div class="chart-legend-item"><span class="chart-legend-color" style="background: #e2e8f0;"></span> Actual</div>
    <div class="chart-legend-item"><span class="chart-legend-color dashed" style="border-color: ${vessel.color};"></span> Forecast</div>
    <div class="chart-legend-item"><span class="chart-legend-color" style="background: rgba(6, 182, 212, 0.2);"></span> 80% CI</div>
    <div class="chart-legend-item"><span class="chart-legend-color" style="background: rgba(6, 182, 212, 0.08);"></span> 95% CI</div>
  `);
}

function renderMarketEntryScore(rates, forecastData) {
  const entry = marketEntryScore(rates, forecastData);

  const scoreColor = entry.score >= 55 ? 'var(--color-success)' : entry.score >= 40 ? 'var(--color-warning)' : 'var(--color-danger)';
  const clampedScore = Math.min(100, Math.max(0, entry.score));
  const arcLength = 150.8;
  const strokeOffset = (arcLength * (1 - clampedScore / 100)).toFixed(1);

  setHTML('marketEntryContent', `
    <div class="market-entry-wrapper">
      <!-- Top Hero Row -->
      <div class="entry-hero-row">
        <!-- Left: Radial Gauge -->
        <div class="entry-gauge-container">
          <div class="gauge-svg-wrap">
            <svg viewBox="0 0 120 72" class="entry-gauge-svg">
              <!-- Background Track -->
              <path d="M 12 62 A 48 48 0 0 1 108 62" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="9" stroke-linecap="round"/>
              <!-- Active Score Track -->
              <path d="M 12 62 A 48 48 0 0 1 108 62" fill="none" stroke="${scoreColor}" stroke-width="9" stroke-linecap="round"
                    stroke-dasharray="${arcLength}"
                    stroke-dashoffset="${strokeOffset}"
                    style="filter: drop-shadow(0 0 6px ${scoreColor}88); transition: stroke-dashoffset 0.8s cubic-bezier(0.16, 1, 0.3, 1);"/>
            </svg>
            <div class="gauge-center-content">
              <span class="entry-score-num" style="color: ${scoreColor};">${entry.score}</span>
              <span class="entry-score-den">/ 100</span>
            </div>
          </div>
        </div>

        <!-- Right: Strategic Signal Box -->
        <div class="entry-signal-box">
          <div class="entry-signal-header">
            <span class="text-xs text-muted font-semi" style="letter-spacing: 0.05em;">CHARTER SIGNAL</span>
            <span class="badge badge-${entry.color === 'success' ? 'success' : entry.color === 'danger' ? 'danger' : 'warning'} pulse-badge">
              ${entry.recommendation}
            </span>
          </div>
          <div class="entry-signal-desc">
            ${entry.score >= 55 
              ? 'Favorable market entry. Locking forward contracts (COA/Time Charter) is recommended.' 
              : entry.score >= 40 
              ? 'Balanced rate environment. Spot exposure acceptable; monitor upcoming seasonal turns.' 
              : 'Softening forward market. Defer long charter commitments; favor spot voyages.'}
          </div>
        </div>
      </div>

      <div class="divider" style="margin: var(--space-2) 0;"></div>

      <!-- Bottom: 2x2 Factor Breakdown Grid -->
      <div class="entry-breakdown-grid">
        ${Object.entries(entry.breakdown).map(([key, b]) => `
          <div class="entry-factor-card">
            <div class="flex justify-between items-center" style="margin-bottom: 4px;">
              <span class="factor-name">${key}</span>
              <span class="factor-score mono">${b.score}<span class="factor-max">/${b.max}</span></span>
            </div>
            <div class="progress-bar" style="height: 4px; margin-bottom: 4px;">
              <div class="progress-fill gradient" style="width: ${(b.score / b.max) * 100}%;"></div>
            </div>
            <div class="factor-detail" title="${b.detail}">${b.detail}</div>
          </div>
        `).join('')}
      </div>
    </div>
  `);
}

function renderDecompositionCharts(results) {
  const { decomposition } = results;
  const displayLen = Math.min(365, decomposition.trend.length);
  const trendData = lastN(decomposition.trend.filter(v => v !== null), displayLen);
  const seasonalData = lastN(decomposition.seasonal, displayLen);

  // Trend chart
  createChart('decompTrendChart', {
    type: 'line',
    data: {
      labels: trendData.map((_, i) => i),
      datasets: [{
        data: trendData,
        borderColor: '#38bdf8',
        borderWidth: 1.5,
        fill: true,
        backgroundColor: 'rgba(56, 189, 248, 0.05)',
        pointRadius: 0,
        tension: 0.4,
      }],
    },
    options: {
      scales: {
        x: { display: false },
        y: {
          grid: { color: 'rgba(255,255,255,0.03)' },
          ticks: { color: '#64748b', font: { family: "'JetBrains Mono'", size: 10 }, callback: v => '$' + (v / 1000).toFixed(0) + 'k' },
          border: { display: false },
        },
      },
      plugins: { legend: { display: false }, tooltip: { enabled: false } },
    },
  });

  // Seasonal chart
  createChart('decompSeasonalChart', {
    type: 'bar',
    data: {
      labels: seasonalData.slice(0, 30).map((_, i) => i + 1),
      datasets: [{
        data: seasonalData.slice(0, 30),
        backgroundColor: seasonalData.slice(0, 30).map(v => v >= 0 ? 'rgba(16, 185, 129, 0.5)' : 'rgba(239, 68, 68, 0.5)'),
        borderRadius: 2,
      }],
    },
    options: {
      scales: {
        x: { grid: { display: false }, ticks: { color: '#64748b', font: { size: 9 } } },
        y: {
          grid: { color: 'rgba(255,255,255,0.03)' },
          ticks: { color: '#64748b', font: { family: "'JetBrains Mono'", size: 10 } },
          border: { display: false },
        },
      },
      plugins: { legend: { display: false }, tooltip: { enabled: false } },
    },
  });
}

function renderAccuracyMetrics(results) {
  const { accuracy } = results;
  setHTML('accuracyMetrics', `
    <div style="display: flex; flex-direction: column; gap: var(--space-4); padding: var(--space-3) 0;">
      <div class="flex justify-between items-center">
        <span class="text-secondary">MAPE</span>
        <span class="data-value text-lg ${accuracy.mape < 10 ? 'text-emerald' : accuracy.mape < 15 ? 'text-amber' : 'text-rose'}">${accuracy.mape.toFixed(2)}%</span>
      </div>
      <div class="progress-bar"><div class="progress-fill ${accuracy.mape < 10 ? 'emerald' : accuracy.mape < 15 ? 'amber' : 'rose'}" style="width: ${Math.min(100, accuracy.mape * 5)}%;"></div></div>

      <div class="flex justify-between items-center">
        <span class="text-secondary">RMSE</span>
        <span class="data-value text-lg">${formatCurrency(accuracy.rmse)}</span>
      </div>

      <div class="flex justify-between items-center">
        <span class="text-secondary">MAE</span>
        <span class="data-value text-lg">${formatCurrency(accuracy.mae)}</span>
      </div>

      <div class="divider"></div>

      <div class="alert alert-info" style="padding: var(--space-3);">
        <span class="alert-icon">💡</span>
        <div class="alert-content">
          <div class="text-xs text-secondary">MAPE ${accuracy.mape < 10 ? 'under 10% indicates high forecast accuracy' : accuracy.mape < 15 ? 'under 15% indicates acceptable accuracy' : 'above 15% — consider more data or parameter tuning'}.</div>
        </div>
      </div>
    </div>
  `);
}

function updateRiskBadge(rates, forecastData) {
  const alerts = generateRiskAlerts(rates, forecastData, null);
  setHTML('riskBadge', alerts.length.toString());
}


// ================================================================
//  VESSEL OPTIMIZER PANEL
// ================================================================

function runVesselOptimizer() {
  const originId = $('vesselOriginSelect')?.value;
  const destId = $('vesselDestSelect')?.value;
  const cargoMT = parseInt($('vesselCargoInput')?.value || '75000');

  const results = optimizeVessel({ originId, destId, cargoMT });

  const origin = PORTS[originId];
  const dest = PORTS[destId];

  let html = `
    <div style="margin-bottom: var(--space-4);">
      <div class="text-sm text-secondary">
        <strong>${origin.name}</strong> → <strong>${dest.name}</strong> | Cargo: <strong>${formatMT(cargoMT)}</strong>
      </div>
    </div>
    <div class="panel-grid panel-grid-2" style="margin-bottom: var(--space-5);">
  `;

  results.forEach((r, idx) => {
    const isTop = idx === 0 && r.feasible;
    html += `
      <div class="rec-card ${isTop ? 'recommended' : ''} animate-fade-in stagger-${idx + 1}">
        ${isTop ? '<span class="rec-badge">Recommended</span>' : ''}
        <div class="flex items-center gap-3" style="margin-bottom: var(--space-4);">
          <div style="width: 44px; height: 44px; border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center; font-size: 1.5rem; background: ${r.feasible ? `rgba(${hexToRgb(r.vesselClass.color)}, 0.15)` : 'var(--color-danger-bg)'};">
            🚢
          </div>
          <div>
            <div class="text-lg font-semi">${r.vesselClass.name}</div>
            <div class="text-xs text-muted">${r.vesselClass.cargoCapacity}</div>
          </div>
        </div>

        <div class="flex gap-2" style="margin-bottom: var(--space-3);">
          <span class="badge ${r.originCheck.feasible ? 'badge-success' : 'badge-danger'}">
            Origin: ${r.originCheck.feasible ? '✓' : '✗ ' + r.originCheck.limitingFactor}
          </span>
          <span class="badge ${r.destCheck.feasible ? 'badge-success' : 'badge-danger'}">
            Dest: ${r.destCheck.feasible ? '✓' : '✗ ' + r.destCheck.limitingFactor}
          </span>
        </div>

        ${!r.feasible ? '<div class="alert alert-danger" style="margin-bottom: var(--space-3);"><span class="alert-icon">⛔</span><div class="alert-content"><div class="alert-title">Not Feasible</div><div class="alert-message">Vessel exceeds port restrictions.</div></div></div>' : ''}

        ${r.needsLighterage ? '<div class="alert alert-warning" style="margin-bottom: var(--space-3);"><span class="alert-icon">⚠️</span><div class="alert-content"><div class="alert-message">' + r.lighterageNote + '</div></div></div>' : ''}

        <div class="data-table-wrapper" style="margin-bottom: var(--space-3);">
          <table class="data-table">
            <tbody>
              <tr><td class="text-muted">Voyages Needed</td><td class="mono-cell text-right">${r.voyages}</td></tr>
              <tr><td class="text-muted">Cargo / Voyage</td><td class="mono-cell text-right">${formatMT(r.cargoPerVoyage)}</td></tr>
              <tr><td class="text-muted">Utilization</td><td class="mono-cell text-right">${(r.utilization * 100).toFixed(0)}%</td></tr>
              <tr><td class="text-muted">Transit Time</td><td class="mono-cell text-right">${formatDays(r.transitDays)}</td></tr>
              <tr><td class="text-muted">Total Voyage</td><td class="mono-cell text-right">${formatDays(r.totalVoyageDays)}</td></tr>
              <tr><td class="text-muted">Freight Rate</td><td class="mono-cell text-right">${formatCurrency(r.freightRate, 2)}/MT</td></tr>
              <tr><td class="text-muted">Cost / Ton</td><td class="mono-cell text-right" style="color: var(--accent-cyan); font-weight: 600;">${formatCurrency(r.totalCostPerTon, 2)}/MT</td></tr>
              <tr><td class="text-muted">Total Cost</td><td class="mono-cell text-right font-semi">${formatCurrency(r.totalCost)}</td></tr>
              <tr><td class="text-muted">Idle Risk</td><td class="mono-cell text-right"><span class="badge ${r.idleRisk < 30 ? 'badge-success' : r.idleRisk < 60 ? 'badge-warning' : 'badge-danger'}">${r.idleRisk}/100</span></td></tr>
            </tbody>
          </table>
        </div>
      </div>
    `;
  });

  html += '</div>';
  setHTML('vesselResults', html);
}


// ================================================================
//  ROUTE COMPARISON PANEL
// ================================================================

function runRouteComparison() {
  const originId = $('routeOriginSelect')?.value;
  const origin = PORTS[originId];
  const routes = getRoutesFromOrigin(originId);

  if (!routes.length) {
    setHTML('routeResults', '<div class="alert alert-warning"><span class="alert-icon">⚠️</span><div class="alert-content"><div class="alert-title">No routes found</div><div class="alert-message">No routes available from this origin.</div></div></div>');
    return;
  }

  let tableHtml = `
    <div class="dash-card animate-fade-in" style="margin-bottom: var(--space-5);">
      <div class="dash-card-header">
        <div class="dash-card-title">Routes from ${origin.name} (${origin.country})</div>
      </div>
      <div class="data-table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th>Destination</th>
              <th class="text-right">Distance (NM)</th>
              <th class="text-right">Transit (days)</th>
              <th>Chokepoints</th>
              <th>Capesize?</th>
              <th class="text-right">Max Draft (m)</th>
              <th class="text-right">Handling Rate</th>
              <th class="text-right">Congestion</th>
            </tr>
          </thead>
          <tbody>
  `;

  routes.forEach(r => {
    const destPort = PORTS[r.dest];
    if (!destPort) return;

    tableHtml += `
      <tr>
        <td><strong>${destPort.name}</strong></td>
        <td class="text-right mono-cell">${formatNumber(r.distanceNM)}</td>
        <td class="text-right mono-cell">${r.transitDays.min}–${r.transitDays.max}</td>
        <td><span class="text-xs text-muted">${r.chokepoints.join(', ') || '—'}</span></td>
        <td class="text-center">${destPort.canHandleCapesize ? '<span class="check-icon">✓</span>' : '<span class="cross-icon">✗</span>'}</td>
        <td class="text-right mono-cell">${destPort.maxDraft}</td>
        <td class="text-right mono-cell">${formatNumber(destPort.cargoHandlingRate)} MT/d</td>
        <td class="text-right"><span class="badge ${destPort.avgCongestionDays <= 2 ? 'badge-success' : destPort.avgCongestionDays <= 3 ? 'badge-warning' : 'badge-danger'}">${destPort.avgCongestionDays}d avg</span></td>
      </tr>
    `;
  });

  tableHtml += '</tbody></table></div></div>';

  // Transit comparison chart
  tableHtml += `
    <div class="panel-grid panel-grid-2">
      <div class="dash-card">
        <div class="dash-card-title" style="margin-bottom: var(--space-3);">Distance Comparison</div>
        <div class="chart-container chart-md"><canvas id="routeDistanceChart"></canvas></div>
      </div>
      <div class="dash-card">
        <div class="dash-card-title" style="margin-bottom: var(--space-3);">Transit Time Range</div>
        <div class="chart-container chart-md"><canvas id="routeTransitChart"></canvas></div>
      </div>
    </div>
  `;

  setHTML('routeResults', tableHtml);

  // Render charts after DOM update
  setTimeout(() => {
    const labels = routes.map(r => PORTS[r.dest]?.name || r.dest).filter(Boolean);
    const distances = routes.map(r => r.distanceNM);
    const transitMin = routes.map(r => r.transitDays.min);
    const transitMax = routes.map(r => r.transitDays.max);

    createChart('routeDistanceChart', {
      type: 'bar',
      data: {
        labels,
        datasets: [{
          data: distances,
          backgroundColor: distances.map((_, i) => `hsla(${180 + i * 25}, 70%, 55%, 0.6)`),
          borderRadius: 4,
        }],
      },
      options: {
        indexAxis: 'y',
        scales: {
          x: { grid: { color: 'rgba(255,255,255,0.03)' }, ticks: { color: '#94a3b8', callback: v => v.toLocaleString() + ' NM' }, border: { display: false } },
          y: { grid: { display: false }, ticks: { color: '#e2e8f0', font: { size: 11 } } },
        },
        plugins: { legend: { display: false } },
      },
    });

    createChart('routeTransitChart', {
      type: 'bar',
      data: {
        labels,
        datasets: [
          { label: 'Min', data: transitMin, backgroundColor: 'rgba(6, 182, 212, 0.5)', borderRadius: 4 },
          { label: 'Max', data: transitMax, backgroundColor: 'rgba(168, 85, 247, 0.5)', borderRadius: 4 },
        ],
      },
      options: {
        indexAxis: 'y',
        scales: {
          x: { grid: { color: 'rgba(255,255,255,0.03)' }, ticks: { color: '#94a3b8', callback: v => v + 'd' }, border: { display: false } },
          y: { grid: { display: false }, ticks: { color: '#e2e8f0', font: { size: 11 } } },
        },
        plugins: { legend: { display: true, labels: { color: '#94a3b8', font: { size: 11 } } } },
      },
    });
  }, 50);
}


// ================================================================
//  PORT INFRASTRUCTURE PANEL
// ================================================================

function renderPortPanel(type = 'discharge') {
  const ports = type === 'discharge' ? getDischargePorts() : getLoadingPorts();

  let html = '<div class="panel-grid panel-grid-2">';
  ports.forEach((p, i) => {
    const risks = getSeasonalRisk(p, new Date().getMonth() + 1);
    html += `
      <div class="dash-card animate-fade-in stagger-${(i % 8) + 1}">
        <div class="flex items-center gap-3" style="margin-bottom: var(--space-4);">
          <div style="width: 40px; height: 40px; border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center; font-size: 1.2rem; background: rgba(6, 182, 212, 0.12);">⚓</div>
          <div>
            <div class="text-md font-semi">${p.name}</div>
            <div class="text-xs text-muted">${p.country} • ${p.unlocode || ''}</div>
          </div>
          <div style="margin-left: auto;">
            ${p.canHandleCapesize ? '<span class="badge badge-success">Capesize ✓</span>' : '<span class="badge badge-neutral">No Capesize</span>'}
          </div>
        </div>

        <div class="data-table-wrapper" style="margin-bottom: var(--space-3);">
          <table class="data-table">
            <tbody>
              <tr><td class="text-muted">Max LOA</td><td class="mono-cell text-right">${p.maxLOA === 999 ? 'No limit' : p.maxLOA + ' m'}</td></tr>
              <tr><td class="text-muted">Max Beam</td><td class="mono-cell text-right">${p.maxBeam === 999 ? 'No limit' : p.maxBeam + ' m'}</td></tr>
              <tr><td class="text-muted">Max Draft</td><td class="mono-cell text-right">${p.maxDraft} m</td></tr>
              <tr><td class="text-muted">Handling Rate</td><td class="mono-cell text-right">${formatNumber(p.cargoHandlingRate)} MT/d</td></tr>
              <tr><td class="text-muted">Avg Congestion</td><td class="mono-cell text-right"><span class="badge ${p.avgCongestionDays <= 2 ? 'badge-success' : p.avgCongestionDays <= 3 ? 'badge-warning' : 'badge-danger'}">${p.avgCongestionDays} days</span></td></tr>
              <tr><td class="text-muted">Port Charges</td><td class="mono-cell text-right">${formatCurrency(p.portCharges, 1)}/MT</td></tr>
              <tr><td class="text-muted">Tidal</td><td class="text-right">${p.tidalDependent ? '<span class="badge badge-warning">Yes</span>' : '<span class="badge badge-success">No</span>'}</td></tr>
            </tbody>
          </table>
        </div>

        ${risks.length ? `
          <div style="display: flex; gap: var(--space-2); flex-wrap: wrap;">
            ${risks.map(r => `<span class="badge ${r.impact === 'high' || r.impact === 'very_high' ? 'badge-danger' : 'badge-warning'}">${r.type}: +${r.delayDays}d delay</span>`).join('')}
          </div>
        ` : ''}

        ${p.notes ? `<div class="text-xs text-muted" style="margin-top: var(--space-3); line-height: 1.5;">${p.notes}</div>` : ''}
      </div>
    `;
  });
  html += '</div>';

  setHTML('portCards', html);
}


// ================================================================
//  RISK PANEL
// ================================================================

function renderRiskPanel() {
  const vesselId = state.selectedVessel;
  const rates = state.data.rates[vesselId];
  const forecastData = state.forecastResults[vesselId];
  const alerts = generateRiskAlerts(rates, forecastData, null);
  const rateValues = rates.map(r => r.rate);

  // Volatility data
  const vol = rollingVolatility(rateValues, [7, 30, 90]);
  const currentVol7 = vol.vol7d[vol.vol7d.length - 1];
  const currentVol30 = vol.vol30d[vol.vol30d.length - 1];
  const currentVol90 = vol.vol90d[vol.vol90d.length - 1] || 0;

  // Stats
  setHTML('riskStats', `
    <div class="stat-card animate-fade-in stagger-1">
      <div class="stat-header"><div class="stat-icon" style="background: var(--color-danger-bg); color: var(--color-danger);">⚠️</div><span class="stat-label">Active Alerts</span></div>
      <div class="stat-value">${alerts.length}</div>
    </div>
    <div class="stat-card animate-fade-in stagger-2">
      <div class="stat-header"><div class="stat-icon" style="background: var(--color-warning-bg); color: var(--color-warning);">⚡</div><span class="stat-label">7d Volatility</span></div>
      <div class="stat-value">${formatCurrency(currentVol7)}</div>
    </div>
    <div class="stat-card animate-fade-in stagger-3">
      <div class="stat-header"><div class="stat-icon" style="background: var(--color-info-bg); color: var(--color-info);">📊</div><span class="stat-label">30d Volatility</span></div>
      <div class="stat-value">${formatCurrency(currentVol30)}</div>
    </div>
    <div class="stat-card animate-fade-in stagger-4">
      <div class="stat-header"><div class="stat-icon" style="background: rgba(168, 85, 247, 0.15); color: var(--accent-purple);">🔍</div><span class="stat-label">90d Volatility</span></div>
      <div class="stat-value">${formatCurrency(currentVol90)}</div>
    </div>
  `);

  // Alert list
  if (alerts.length === 0) {
    setHTML('riskAlertsList', '<div class="empty-state" style="padding: var(--space-6);"><div class="empty-state-icon">✅</div><div class="empty-state-title">No Active Alerts</div><div class="empty-state-desc">Market conditions are stable.</div></div>');
  } else {
    setHTML('riskAlertsList', alerts.map((a, i) => `
      <div class="alert alert-${a.type}" style="margin-bottom: var(--space-3); animation: fadeIn 0.3s ease-out ${i * 0.08}s both;">
        <span class="alert-icon">${a.icon}</span>
        <div class="alert-content">
          <div class="alert-title">${a.title}</div>
          <div class="alert-message">${a.message}</div>
        </div>
      </div>
    `).join(''));
  }

  // Volatility chart
  setTimeout(() => {
    const volData = lastN(vol.vol30d.filter(v => v !== null), 180);
    createChart('volatilityChart', {
      type: 'line',
      data: {
        labels: volData.map((_, i) => i),
        datasets: [{
          label: '30d Volatility',
          data: volData,
          borderColor: '#f59e0b',
          borderWidth: 2,
          fill: true,
          backgroundColor: 'rgba(245, 158, 11, 0.08)',
          pointRadius: 0,
          tension: 0.3,
        }],
      },
      options: {
        scales: {
          x: { display: false },
          y: {
            grid: { color: 'rgba(255,255,255,0.03)' },
            ticks: { color: '#94a3b8', font: { family: "'JetBrains Mono'", size: 11 }, callback: v => '$' + v.toLocaleString() },
            border: { display: false },
          },
        },
        plugins: { legend: { display: false } },
      },
    });
  }, 50);
}


// ================================================================
//  CONTRACT STRATEGY PANEL
// ================================================================

function runContractAnalysis() {
  const vesselId = $('contractVesselSelect')?.value || 'CAPESIZE';
  const cargoMT = parseInt($('contractCargoInput')?.value || '75000');
  const voyagesPerYear = parseInt($('contractVoyagesInput')?.value || '10');

  // Ensure forecast exists
  if (!state.forecastResults[vesselId]) {
    const rates = state.data.rates[vesselId];
    state.forecastResults[vesselId] = runForecast(rates, 90);
  }

  const forecastData = state.forecastResults[vesselId];
  const tcRate = forecastData.trend.currentRate;

  // Assuming a standard voyage of 25 days (20 days transit + 5 days port)
  const standardVoyageDays = 25;
  const tcToMT = standardVoyageDays / cargoMT;
  const currentRateMT = tcRate * tcToMT;

  const comparison = compareContracts(currentRateMT, forecastData, cargoMT, voyagesPerYear, tcToMT);

  const recMap = { SPOT: 'spot', SHORT_TERM: 'shortTerm', MID_TERM: 'midTerm' };
  const recKey = recMap[comparison.recommendation];

  setHTML('contractResults', `
    <div class="panel-grid panel-grid-3" style="margin-bottom: var(--space-5);">
      ${['spot', 'shortTerm', 'midTerm'].map(key => {
        const c = comparison[key];
        const isRec = key === recKey;
        return `
          <div class="rec-card ${isRec ? 'recommended' : ''} animate-fade-in">
            ${isRec ? '<span class="rec-badge">Recommended</span>' : ''}
            <div class="text-lg font-semi" style="margin-bottom: var(--space-3);">${c.type}</div>
            <div class="data-table-wrapper">
              <table class="data-table">
                <tbody>
                  <tr><td class="text-muted">Rate</td><td class="mono-cell text-right">${formatCurrency(c.rate * 100, 2)}/MT</td></tr>
                  <tr><td class="text-muted">Annual Cost</td><td class="mono-cell text-right font-semi">${formatCurrency(c.annualCost)}</td></tr>
                  <tr><td class="text-muted">Flexibility</td><td class="text-right">${c.flexibility}</td></tr>
                  ${c.discount ? `<tr><td class="text-muted">Discount</td><td class="text-right"><span class="badge badge-success">${c.discount}</span></td></tr>` : ''}
                </tbody>
              </table>
            </div>
            <div class="text-xs text-muted" style="margin-top: var(--space-3);">${c.riskExposure}</div>
          </div>
        `;
      }).join('')}
    </div>

    <div class="dash-card animate-fade-in">
      <div class="dash-card-header">
        <div class="dash-card-title">Savings Analysis</div>
      </div>
      <div class="panel-grid panel-grid-2">
        <div>
          <div class="text-sm text-secondary" style="margin-bottom: var(--space-2);">Short-Term COA Savings vs Spot</div>
          <div class="data-value text-2xl text-emerald">${formatCurrency(comparison.savings.shortTerm)}</div>
          <div class="text-sm text-muted">${formatPercent(comparison.savings.shortTermPct)} annual reduction</div>
        </div>
        <div>
          <div class="text-sm text-secondary" style="margin-bottom: var(--space-2);">Mid-Term COA Savings vs Spot</div>
          <div class="data-value text-2xl text-emerald">${formatCurrency(comparison.savings.midTerm)}</div>
          <div class="text-sm text-muted">${formatPercent(comparison.savings.midTermPct)} annual reduction</div>
        </div>
      </div>
      <div class="divider"></div>
      <div class="alert alert-info">
        <span class="alert-icon">📋</span>
        <div class="alert-content">
          <div class="alert-title">Recommendation Rationale</div>
          <div class="alert-message">${comparison.rationale}</div>
        </div>
      </div>
    </div>
  `);
}


// ================================================================
//  IDLE MANAGEMENT PANEL
// ================================================================

function runIdleAnalysis() {
  const vesselId = $('idleVesselSelect')?.value || 'CAPESIZE';
  const portId = $('idlePortSelect')?.value;
  const vessel = VESSEL_CLASSES[vesselId];
  const port = PORTS[portId];

  const scenarios = analyzeIdleScenarios(vessel, null, port, null);

  setHTML('idleResults', `
    <div class="stat-cards" style="margin-bottom: var(--space-5);">
      <div class="stat-card animate-fade-in stagger-1">
        <div class="stat-header"><div class="stat-icon" style="background: var(--color-info-bg); color: var(--color-info);">⏱️</div><span class="stat-label">Idle Scenarios</span></div>
        <div class="stat-value">${scenarios.length}</div>
      </div>
      <div class="stat-card animate-fade-in stagger-2">
        <div class="stat-header"><div class="stat-icon" style="background: var(--color-warning-bg); color: var(--color-warning);">💰</div><span class="stat-label">Daily Idle Cost</span></div>
        <div class="stat-value">${formatCurrency(vessel.dailyCost.mid)}</div>
        <div class="stat-change text-muted">${vessel.name} TC rate</div>
      </div>
      <div class="stat-card animate-fade-in stagger-3">
        <div class="stat-header"><div class="stat-icon" style="background: var(--color-danger-bg); color: var(--color-danger);">📊</div><span class="stat-label">Port Congestion</span></div>
        <div class="stat-value">${port?.avgCongestionDays || 0}d</div>
        <div class="stat-change text-muted">avg waiting time</div>
      </div>
    </div>

    <div style="display: flex; flex-direction: column; gap: var(--space-4);">
      ${scenarios.map((s, i) => `
        <div class="dash-card animate-fade-in stagger-${i + 1}">
          <div class="flex items-center gap-3" style="margin-bottom: var(--space-3);">
            <span class="badge ${s.severity === 'high' ? 'badge-danger' : s.severity === 'medium' ? 'badge-warning' : 'badge-info'}">${s.severity.toUpperCase()}</span>
            <div class="text-md font-semi">${s.title}</div>
          </div>
          <p class="text-sm" style="margin-bottom: var(--space-3);">${s.description}</p>
          <div class="text-xs font-semi text-cyan" style="margin-bottom: var(--space-2);">MITIGATION STRATEGIES</div>
          <ul style="list-style: none; padding: 0; display: flex; flex-direction: column; gap: var(--space-2);">
            ${s.mitigation.map(m => `<li class="text-sm text-secondary" style="padding-left: var(--space-4); position: relative;"><span style="position: absolute; left: 0; color: var(--accent-cyan);">→</span>${m}</li>`).join('')}
          </ul>
        </div>
      `).join('')}
    </div>
  `);
}


// ================================================================
//  REAL-TIME WEBSOCKET & RESILIENCE MANAGEMENT
// ================================================================

function initWebSocket() {
  const statusDot = $('wsStatusDot');
  const statusText = $('wsStatusText');
  const latencyBadge = $('wsLatencyBadge');
  const statusPill = $('connectionStatusPill');

  // Listen to connection status
  wsClient.on('status_change', ({ status, latencyMs, stats }) => {
    state.wsStatus = status;
    state.latencyMs = latencyMs;

    if (status === 'CONNECTED') {
      if (statusDot) {
        statusDot.className = 'status-dot connected';
      }
      if (statusText) statusText.innerText = 'Live WS';
      if (latencyBadge) {
        latencyBadge.style.display = 'inline-block';
        latencyBadge.className = 'badge badge-success badge-sm';
        latencyBadge.innerText = `${latencyMs || 15}ms`;
      }
    } else if (status === 'RECONNECTING') {
      if (statusDot) {
        statusDot.className = 'status-dot reconnecting';
      }
      if (statusText) statusText.innerText = 'Reconnecting...';
      if (latencyBadge) latencyBadge.style.display = 'none';
    } else if (status === 'FALLBACK') {
      if (statusDot) {
        statusDot.className = 'status-dot fallback';
      }
      if (statusText) statusText.innerText = 'Standalone Mode';
      if (latencyBadge) {
        latencyBadge.style.display = 'inline-block';
        latencyBadge.className = 'badge badge-info badge-sm';
        latencyBadge.innerText = 'Resilient';
      }
    }
  });

  // Handle live market rate updates
  wsClient.on('rate_tick', (rates) => {
    state.liveRates = rates;
    handleLiveRateTick(rates);
  });

  // Handle live operational risk alerts
  wsClient.on('risk_alert', (alert) => {
    toastManager.show({
      title: alert.title || 'Port / Market Risk Alert',
      message: alert.message || '',
      type: alert.severity || 'warning',
      duration: 7000
    });

    // Update risk badge counter in sidebar
    const badge = $('riskBadge');
    if (badge) {
      const current = parseInt(badge.innerText || '0') + 1;
      badge.innerText = current;
      badge.style.animation = 'pulse 1s 2';
    }
  });

  // Click on status indicator to show diagnostics
  if (statusPill) {
    statusPill.addEventListener('click', () => {
      const stats = wsClient.stats;
      const modeText = stats.fallbackActive ? 'Standalone Offline Simulation' : 'Connected to ws://127.0.0.1:8765';
      toastManager.show({
        title: `Connection Diagnostics [${state.wsStatus}]`,
        message: `Packets: ${stats.packetsReceived} | Latency: ${state.latencyMs || '—'}ms | Mode: ${modeText}`,
        type: stats.fallbackActive ? 'info' : 'success',
        duration: 5000
      });
    });
  }
}

function handleLiveRateTick(rates) {
  if (!rates) return;

  // Animate Top KPI Bar
  if (rates.BDI) {
    const bdiVal = $('kpi-bdi-val');
    if (bdiVal) {
      bdiVal.innerText = formatNumber(rates.BDI.rate);
      flashElement(bdiVal, rates.BDI.delta >= 0 ? 'flash-red' : 'flash-green');
    }
  }

  if (rates.CAPESIZE) {
    const capeVal = $('kpi-cape-val');
    if (capeVal) {
      capeVal.innerText = formatCurrency(rates.CAPESIZE.rate);
      flashElement(capeVal, rates.CAPESIZE.delta >= 0 ? 'flash-red' : 'flash-green');
    }
  }

  // If currently viewing forecast panel with matching vessel, flash the stat card
  if (state.activePanel === 'forecast' && rates[state.selectedVessel]) {
    const statVal = document.querySelector('#forecastStats .stat-value');
    if (statVal) {
      statVal.innerText = formatCurrency(rates[state.selectedVessel].rate);
      flashElement(statVal, rates[state.selectedVessel].delta >= 0 ? 'flash-red' : 'flash-green');
    }
  }
}

function flashElement(el, flashClass) {
  if (!el) return;
  el.classList.remove('flash-green', 'flash-red');
  void el.offsetWidth; // trigger browser reflow
  el.classList.add(flashClass);
  setTimeout(() => el.classList.remove(flashClass), 1200);
}

function loadPreferences() {
  try {
    const saved = localStorage.getItem('freight_forecast_prefs');
    if (saved) {
      const prefs = JSON.parse(saved);
      if (prefs.selectedVessel) state.selectedVessel = prefs.selectedVessel;
      if (prefs.forecastHorizon) state.forecastHorizon = prefs.forecastHorizon;
      if (prefs.historyDays) state.historyDays = prefs.historyDays;
    }
  } catch (err) {
    console.warn('[Storage] Unable to load preferences:', err);
  }
}

function savePreferences() {
  try {
    localStorage.setItem('freight_forecast_prefs', JSON.stringify({
      selectedVessel: state.selectedVessel,
      forecastHorizon: state.forecastHorizon,
      historyDays: state.historyDays,
    }));
  } catch (err) {
    console.warn('[Storage] Unable to save preferences:', err);
  }
}



// ================================================================
//  HELPERS
// ================================================================

function hexToRgb(hex) {
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);
  return `${r}, ${g}, ${b}`;
}
