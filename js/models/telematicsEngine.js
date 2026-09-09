/**
 * FreightForecast Pro — Live AIS Telematics Engine
 * Subscribes to real-time WebSocket telemetry stream.
 * Features:
 * - Live vessel tracking across Indian Ocean & Bay of Bengal corridors
 * - Interactive AIS vessel inspection popups
 * - Dynamic vessel class filtering (Capesize, Panamax, Supramax, Handysize)
 * - Click-to-focus on map from live voyage feed
 */

import { wsClient } from '../utils/wsClient.js';

let map = null;
let markers = {};
let currentFleet = [];
let currentFilter = 'ALL';
let isInitialized = false;

export function initTelematicsMap(containerId = 'map-container') {
  if (isInitialized && window.telematicsMap) {
    setTimeout(() => window.telematicsMap.invalidateSize(), 150);
    return;
  }

  const container = document.getElementById(containerId);
  if (!container) return;

  // Initialize map centered on Indian Ocean / Bay of Bengal trade lanes
  map = L.map(containerId, {
    center: [6.5, 88.0],
    zoom: 4,
    zoomControl: true,
    attributionControl: false
  });
  window.telematicsMap = map;
  isInitialized = true;

  // Standard OpenStreetMap with dark aesthetic via CSS filter
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '© OpenStreetMap contributors'
  }).addTo(map);

  // Subscribe to WebSocket telematics stream
  wsClient.on('telematics', (fleet) => {
    handleIncomingFleet(fleet);
  });

  // Setup class filter listener if controls exist
  setupFilterControls();

  // Force Leaflet tile recalculation
  setTimeout(() => map.invalidateSize(), 200);
}

function handleIncomingFleet(fleet) {
  if (!Array.isArray(fleet) || !map) return;
  currentFleet = fleet;

  // Update live active count
  const countEl = document.getElementById('active-vessels-count');
  if (countEl) countEl.innerText = fleet.length;

  // Filter fleet based on selection
  const filtered = currentFilter === 'ALL' 
    ? fleet 
    : fleet.filter(v => v.vesselClass && v.vesselClass.toLowerCase() === currentFilter.toLowerCase());

  // Set of active IMOs
  const activeImos = new Set(filtered.map(v => v.imo));

  // Remove markers no longer active or filtered out
  Object.keys(markers).forEach(imo => {
    if (!activeImos.has(imo)) {
      map.removeLayer(markers[imo]);
      delete markers[imo];
    }
  });

  // Update or create markers
  filtered.forEach(v => {
    const lat = v.lat !== undefined ? v.lat : (v.origin.coords[0] + (v.dest.coords[0] - v.origin.coords[0]) * v.progress);
    const lng = v.lng !== undefined ? v.lng : (v.origin.coords[1] + (v.dest.coords[1] - v.origin.coords[1]) * v.progress);
    const isDelayed = v.status && v.status.toLowerCase().includes('delayed');
    const isWaiting = v.status && v.status.toLowerCase().includes('anchorage');
    
    let color = '#34d399'; // Emerald green
    if (isDelayed) color = '#f59e0b'; // Amber warning
    if (isWaiting) color = '#ef4444'; // Red alert

    if (markers[v.imo]) {
      markers[v.imo].setLatLng([lat, lng]);
    } else {
      const icon = L.divIcon({
        html: `
          <div class="vessel-marker" style="--marker-color: ${color};" title="${v.name}">
            <div class="vessel-dot" style="background: ${color}; box-shadow: 0 0 12px ${color};"></div>
          </div>`,
        className: 'vessel-marker-wrapper',
        iconSize: [16, 16],
        iconAnchor: [8, 8]
      });

      const marker = L.marker([lat, lng], { icon }).addTo(map);

      // Interactive Popup
      marker.bindPopup(() => createVesselPopup(v), {
        className: 'vessel-popup-custom',
        maxWidth: 280
      });

      markers[v.imo] = marker;
    }
  });

  // Update the side voyage feed
  renderTelematicsFeed(filtered);
}

function createVesselPopup(v) {
  const originName = v.origin ? v.origin.name : 'Unknown';
  const destName = v.dest ? v.dest.name : 'India Port';
  const isDelayed = v.status && v.status.toLowerCase().includes('delayed');
  const statusColor = isDelayed ? '#f59e0b' : '#34d399';

  return `
    <div style="font-family: var(--font-sans, system-ui); color: #f8fafc; padding: 4px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
        <strong style="font-size: 13px; color: #38bdf8;">${v.name || 'Vessel ' + v.imo}</strong>
        <span style="font-size: 10px; background: rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 4px;">${v.vesselClass || 'Bulk'}</span>
      </div>
      <div style="font-size: 11px; color: #94a3b8; margin-bottom: 6px;">
        IMO: <span style="color: #e2e8f0;">${v.imo}</span> | DWT: <span style="color: #e2e8f0;">${v.dwt ? (v.dwt/1000).toFixed(0) + 'k' : '—'} MT</span>
      </div>
      <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255,255,255,0.08); border-radius: 6px; padding: 8px; margin-bottom: 8px;">
        <div style="font-size: 11px; margin-bottom: 3px;"><strong>Route:</strong> ${originName} ➔ <span style="color: #38bdf8;">${destName}</span></div>
        <div style="font-size: 11px; margin-bottom: 3px;"><strong>Speed:</strong> ${v.speed} knots</div>
        <div style="font-size: 11px; margin-bottom: 3px;"><strong>ETA:</strong> ${v.etaDays ? v.etaDays + ' days' : 'In transit'}</div>
        <div style="font-size: 11px;"><strong>Status:</strong> <span style="color: ${statusColor}; font-weight: 600;">${v.status || 'Active'}</span></div>
      </div>
      ${v.demurrageRiskUSD ? `<div style="font-size: 10px; color: #f87171;">⚠️ Demurrage Exposure: $${v.demurrageRiskUSD.toLocaleString()}</div>` : ''}
    </div>
  `;
}

function renderTelematicsFeed(fleet) {
  const feed = document.getElementById('telematics-feed');
  if (!feed) return;

  const sorted = [...fleet].sort((a, b) => (b.progress || 0) - (a.progress || 0)).slice(0, 10);

  feed.innerHTML = sorted.map(v => {
    const isDelayed = v.status && v.status.toLowerCase().includes('delayed');
    const color = isDelayed ? '#f59e0b' : '#34d399';
    const progressPct = Math.min(100, Math.round((v.progress || 0) * 100));

    return `
      <div class="voyage-feed-card" data-imo="${v.imo}" style="background: rgba(255,255,255,0.03); border: 1px solid var(--glass-border); padding: 12px; border-radius: 8px; cursor: pointer; transition: all 0.2s ease;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
          <span style="color: #fff; font-size: 12px; font-weight: 600;">${v.name || v.imo}</span>
          <span style="color: ${color}; font-size: 10px; font-weight: 600; text-transform: uppercase;">${v.status || 'In Transit'}</span>
        </div>
        <div style="color: #94a3b8; font-size: 11px; margin-bottom: 6px;">
          ${v.origin ? v.origin.name : 'Port'} ➔ <strong style="color: #38bdf8;">${v.dest ? v.dest.name : 'East Coast'}</strong>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 10px; color: #64748b; margin-bottom: 4px;">
          <span>${v.vesselClass || 'Bulk'}</span>
          <span>${v.speed} kts | ${progressPct}%</span>
        </div>
        <div style="height: 4px; background: rgba(255,255,255,0.1); border-radius: 2px; overflow: hidden;">
          <div style="height: 100%; width: ${progressPct}%; background: ${color}; transition: width 0.4s ease;"></div>
        </div>
      </div>
    `;
  }).join('');

  // Add click-to-focus listeners on feed cards
  feed.querySelectorAll('.voyage-feed-card').forEach(card => {
    card.addEventListener('click', () => {
      const imo = card.dataset.imo;
      if (markers[imo] && map) {
        const marker = markers[imo];
        map.flyTo(marker.getLatLng(), 6, { duration: 1.2 });
        setTimeout(() => marker.openPopup(), 1300);
      }
    });
  });
}

function setupFilterControls() {
  const filterContainer = document.getElementById('telematics-class-filters');
  if (!filterContainer) return;

  filterContainer.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      filterContainer.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentFilter = btn.dataset.class || 'ALL';
      if (currentFleet.length > 0) {
        handleIncomingFleet(currentFleet);
      }
    });
  });
}
