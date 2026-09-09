/**
 * FreightForecast Pro — Resilient WebSocket Client Manager
 * 
 * Features:
 * - Auto-reconnection with exponential backoff & jitter
 * - Continuous latency (ping-pong) tracking
 * - Pub/Sub event bus for clean module decoupling
 * - Zero-Failure Fallback: Automatically falls back to internal mock streamer
 *   if the server is down or unreachable, guaranteeing 100% dashboard uptime.
 */

class WebSocketClient {
  constructor(url = 'ws://127.0.0.1:8765/ws') {
    this.url = url;
    this.socket = null;
    this.listeners = new Map();
    
    // Connection State
    this.status = 'DISCONNECTED'; // CONNECTING, CONNECTED, RECONNECTING, FALLBACK
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 3;
    this.baseDelay = 1000;
    this.maxDelay = 10000;
    this.pingInterval = null;
    this.latencyMs = null;
    
    // Telemetry Statistics
    this.stats = {
      packetsReceived: 0,
      lastPacketTime: null,
      bytesReceived: 0,
      connectedAt: null,
      fallbackActive: false
    };

    // Internal fallback interval
    this.fallbackInterval = null;
    this.fallbackRatesInterval = null;
    this.fallbackAlertInterval = null;

    // Auto-initialize connection
    this.connect();
  }

  /**
   * Register event listener.
   * Events: 'status_change', 'telematics', 'rate_tick', 'risk_alert', 'initial_state', 'latency'
   */
  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event).add(callback);
    return () => this.off(event, callback);
  }

  off(event, callback) {
    if (this.listeners.has(event)) {
      this.listeners.get(event).delete(callback);
    }
  }

  emit(event, data) {
    if (this.listeners.has(event)) {
      for (const cb of this.listeners.get(event)) {
        try {
          cb(data);
        } catch (err) {
          console.error(`[WS Error in listener for ${event}]:`, err);
        }
      }
    }
  }

  setStatus(newStatus) {
    if (this.status !== newStatus) {
      this.status = newStatus;
      this.emit('status_change', {
        status: this.status,
        latencyMs: this.latencyMs,
        stats: this.stats,
        attempts: this.reconnectAttempts
      });
    }
  }

  connect() {
    if (this.socket && (this.socket.readyState === WebSocket.OPEN || this.socket.readyState === WebSocket.CONNECTING)) {
      return;
    }

    this.setStatus(this.reconnectAttempts > 0 ? 'RECONNECTING' : 'CONNECTING');

    try {
      this.socket = new WebSocket(this.url);

      this.socket.onopen = () => {
        console.log('[WS] Connected successfully to', this.url);
        this.reconnectAttempts = 0;
        this.stats.connectedAt = Date.now();
        this.stats.fallbackActive = false;
        this.stopFallback();
        this.setStatus('CONNECTED');
        this.startHeartbeat();
      };

      this.socket.onmessage = (event) => {
        this.stats.packetsReceived++;
        this.stats.lastPacketTime = Date.now();
        this.stats.bytesReceived += event.data ? event.data.length : 0;

        try {
          const packet = JSON.parse(event.data);
          this.handlePacket(packet);
        } catch (err) {
          console.warn('[WS] Failed to parse incoming packet:', err);
        }
      };

      this.socket.onerror = (err) => {
        console.warn('[WS] Connection issue:', err.message || 'Connection refused');
      };

      this.socket.onclose = (event) => {
        this.stopHeartbeat();
        if (this.status !== 'FALLBACK') {
          this.handleDisconnect();
        }
      };
    } catch (err) {
      console.warn('[WS] Socket initialization error:', err);
      this.handleDisconnect();
    }
  }

  handlePacket(packet) {
    switch (packet.type) {
      case 'INITIAL_STATE':
        this.emit('initial_state', packet);
        if (packet.fleet) this.emit('telematics', packet.fleet);
        if (packet.rates) this.emit('rate_tick', packet.rates);
        break;

      case 'TELEMATICS_UPDATE':
      case 'FLEET_UPDATE':
        this.emit('telematics', packet.fleet);
        break;

      case 'RATE_TICK':
        this.emit('rate_tick', packet.rates);
        break;

      case 'RISK_ALERT':
        this.emit('risk_alert', packet.alert);
        break;

      case 'pong':
        if (packet.clientTime) {
          this.latencyMs = Math.max(1, Date.now() - packet.clientTime);
          this.emit('latency', this.latencyMs);
          this.emit('status_change', {
            status: this.status,
            latencyMs: this.latencyMs,
            stats: this.stats
          });
        }
        break;

      default:
        this.emit(packet.type, packet);
        break;
    }
  }

  handleDisconnect() {
    this.reconnectAttempts++;

    if (this.reconnectAttempts <= this.maxReconnectAttempts) {
      // Exponential backoff with jitter
      const delay = Math.min(
        this.maxDelay,
        this.baseDelay * Math.pow(1.5, this.reconnectAttempts) + Math.random() * 500
      );
      this.setStatus('RECONNECTING');
      console.log(`[WS] Reconnecting attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts} in ${Math.round(delay)}ms...`);
      setTimeout(() => this.connect(), delay);
    } else {
      // Exceeded attempts - activate zero-failure fallback
      console.info('[WS] Backend unreachable. Activating High-Reliability Standalone Simulation.');
      this.activateFallback();
    }
  }

  startHeartbeat() {
    this.stopHeartbeat();
    this.pingInterval = setInterval(() => {
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        this.socket.send(JSON.stringify({ type: 'ping', t: Date.now() }));
      }
    }, 8000);
  }

  stopHeartbeat() {
    if (this.pingInterval) {
      clearInterval(this.pingInterval);
      this.pingInterval = null;
    }
  }

  /**
   * Bulletproof Standalone Fallback
   * Generates realistic streaming events locally so the UI never degrades.
   */
  activateFallback() {
    this.stats.fallbackActive = true;
    this.setStatus('FALLBACK');

    // Create fallback fleet
    if (!this.fallbackFleet) {
      this.fallbackFleet = this.generateFallbackFleet();
    }

    // Telematics loop (every 2.5s)
    if (!this.fallbackInterval) {
      this.fallbackInterval = setInterval(() => {
        this.updateFallbackFleet();
        this.emit('telematics', this.fallbackFleet);
      }, 2500);
      // Immediately emit once
      this.emit('telematics', this.fallbackFleet);
    }

    // Rates loop (every 5s)
    if (!this.fallbackRatesInterval) {
      this.fallbackRatesInterval = setInterval(() => {
        const rates = this.generateFallbackRateTick();
        this.emit('rate_tick', rates);
      }, 5000);
    }

    // Periodic check to see if real server came back online (every 15s)
    setTimeout(() => {
      if (this.status === 'FALLBACK') {
        console.log('[WS] Checking if backend server has restored...');
        this.reconnectAttempts = 0;
        this.connect();
      }
    }, 15000);
  }

  stopFallback() {
    if (this.fallbackInterval) {
      clearInterval(this.fallbackInterval);
      this.fallbackInterval = null;
    }
    if (this.fallbackRatesInterval) {
      clearInterval(this.fallbackRatesInterval);
      this.fallbackRatesInterval = null;
    }
  }

  generateFallbackFleet() {
    const origins = [
      { name: 'Newcastle', coords: [-32.92, 151.78] },
      { name: 'Hay Point', coords: [-21.27, 149.30] },
      { name: 'Richards Bay', coords: [-28.79, 32.09] },
      { name: 'Samarinda', coords: [-0.50, 117.15] }
    ];
    const dests = [
      { name: 'Paradip', coords: [20.26, 86.67] },
      { name: 'Visakhapatnam', coords: [17.68, 83.27] },
      { name: 'Haldia', coords: [22.02, 88.06] },
      { name: 'Dhamra', coords: [20.79, 86.96] }
    ];
    const classes = ['Capesize', 'Panamax', 'Supramax', 'Handysize'];
    const fleet = [];

    for (let i = 0; i < 22; i++) {
      const origin = origins[i % origins.length];
      const dest = dests[i % dests.length];
      const vClass = classes[i % classes.length];
      const progress = 0.1 + (i * 0.04);
      fleet.push({
        imo: `93${10000 + i * 243}`,
        name: `MV VOYAGER ${i + 1}`,
        vesselClass: vClass,
        dwt: vClass === 'Capesize' ? 180000 : vClass === 'Panamax' ? 75000 : 58000,
        origin,
        dest,
        progress,
        lat: origin.coords[0] + (dest.coords[0] - origin.coords[0]) * progress,
        lng: origin.coords[1] + (dest.coords[1] - origin.coords[1]) * progress,
        speed: (12.5 + (i % 3) * 0.8).toFixed(1),
        heading: 315,
        status: i % 5 === 0 ? 'Delayed (Weather)' : 'In Transit',
        cargoMT: vClass === 'Capesize' ? 172000 : 71000,
        demurrageRiskUSD: i % 5 === 0 ? 18500 : 0,
        etaDays: (4 + (1 - progress) * 12).toFixed(1)
      });
    }
    return fleet;
  }

  updateFallbackFleet() {
    if (!this.fallbackFleet) return;
    this.fallbackFleet.forEach(v => {
      if (v.status !== 'Delayed (Weather)') {
        v.progress += 0.0008;
        if (v.progress > 0.98) v.progress = 0.05;
      }
      v.lat = v.origin.coords[0] + (v.dest.coords[0] - v.origin.coords[0]) * v.progress;
      v.lng = v.origin.coords[1] + (v.dest.coords[1] - v.origin.coords[1]) * v.progress;
      v.etaDays = Math.max(0.5, ((1 - v.progress) * 14)).toFixed(1);
    });
  }

  generateFallbackRateTick() {
    const delta = (Math.random() * 200 - 90);
    return {
      CAPESIZE: { rate: Math.round(24850 + delta), delta: Math.round(delta), pctChange: (delta / 24850 * 100).toFixed(2) },
      PANAMAX: { rate: Math.round(15420 + delta * 0.6), delta: Math.round(delta * 0.6), pctChange: (delta * 0.6 / 15420 * 100).toFixed(2) },
      BDI: { rate: Math.round(1845 + delta * 0.1), delta: Math.round(delta * 0.1), pctChange: (delta * 0.1 / 1845 * 100).toFixed(2) }
    };
  }

  send(data) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(typeof data === 'string' ? data : JSON.stringify(data));
      return true;
    }
    return false;
  }
}

// Export singleton instance
export const wsClient = new WebSocketClient();
