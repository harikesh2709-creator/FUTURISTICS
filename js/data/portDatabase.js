/**
 * FreightForecast Pro — Port Infrastructure Database
 * Real-world port specifications for East Coast India discharge ports
 * and origin loading ports across Australia, USA, Mozambique, Russia, Indonesia.
 */

export const PORT_TYPES = {
  DISCHARGE: 'discharge',
  LOADING: 'loading',
};

export const REGIONS = {
  INDIA_EAST: 'India (East Coast)',
  AUSTRALIA: 'Australia',
  USA: 'USA',
  MOZAMBIQUE: 'Mozambique',
  RUSSIA: 'Russia',
  INDONESIA: 'Indonesia',
};

/**
 * Comprehensive port database.
 * All dimensions in meters, rates in MT/day, depths in meters.
 */
export const PORTS = {
  // ================================================================
  //  EAST COAST INDIA — DISCHARGE PORTS
  // ================================================================

  PARADIP: {
    id: 'PARADIP',
    name: 'Paradip',
    fullName: 'Paradip Port',
    country: 'India',
    region: REGIONS.INDIA_EAST,
    type: PORT_TYPES.DISCHARGE,
    lat: 20.2650,
    lng: 86.6246,
    unlocode: 'INPRD',
    maxLOA: 300,
    maxBeam: 46,
    maxDraft: 16.5,
    channelDepth: 18.5,
    cargoHandlingRate: 35000,   // MT/day
    berthCount: 14,
    tidalDependent: false,
    pilotageRequired: true,
    nightNavigation: true,
    canHandleCapesize: true,
    portCharges: 2.8,           // $/MT approximate
    avgCongestionDays: 2,
    cargoTypes: ['Coal', 'Iron Ore', 'Chrome Ore', 'Fertilizer', 'POL'],
    seasonalRisks: {
      monsoon: { months: [6, 7, 8, 9], impact: 'moderate', delayDays: 1.5 },
      cyclone: { months: [10, 11, 12], impact: 'high', delayDays: 3 },
    },
    notes: 'Deep water, all-weather port. Recently dredged to 18.5m channel depth. Major coal import hub.',
  },

  VIZAG: {
    id: 'VIZAG',
    name: 'Visakhapatnam',
    fullName: 'Visakhapatnam Port (Outer Harbour)',
    country: 'India',
    region: REGIONS.INDIA_EAST,
    type: PORT_TYPES.DISCHARGE,
    lat: 17.6868,
    lng: 83.2985,
    unlocode: 'INVTZ',
    maxLOA: 280,
    maxBeam: 45,
    maxDraft: 18.1,
    channelDepth: 18.5,
    cargoHandlingRate: 30000,
    berthCount: 24,
    tidalDependent: false,
    pilotageRequired: true,
    nightNavigation: true,
    canHandleCapesize: true,
    portCharges: 3.0,
    avgCongestionDays: 3,
    cargoTypes: ['Coal', 'Iron Ore', 'Alumina', 'Fertilizer', 'Containers', 'POL'],
    seasonalRisks: {
      monsoon: { months: [6, 7, 8, 9], impact: 'moderate', delayDays: 1 },
      cyclone: { months: [10, 11, 12], impact: 'high', delayDays: 3.5 },
    },
    notes: 'Deepest landlocked port in India. Outer harbour for Capesize. Two pilots required for LOA >195m or beam >32m.',
  },

  VIZAG_INNER: {
    id: 'VIZAG_INNER',
    name: 'Visakhapatnam (Inner)',
    fullName: 'Visakhapatnam Port (Inner Harbour)',
    country: 'India',
    region: REGIONS.INDIA_EAST,
    type: PORT_TYPES.DISCHARGE,
    lat: 17.6900,
    lng: 83.2900,
    unlocode: 'INVTZ',
    maxLOA: 240,
    maxBeam: 32,
    maxDraft: 14.5,
    channelDepth: 15.0,
    cargoHandlingRate: 20000,
    berthCount: 20,
    tidalDependent: false,
    pilotageRequired: true,
    nightNavigation: true,
    canHandleCapesize: false,
    portCharges: 3.0,
    avgCongestionDays: 2.5,
    cargoTypes: ['Coal', 'General Cargo', 'Fertilizer'],
    seasonalRisks: {
      monsoon: { months: [6, 7, 8, 9], impact: 'moderate', delayDays: 1 },
      cyclone: { months: [10, 11, 12], impact: 'high', delayDays: 3 },
    },
    notes: 'Inner harbour — limited to Panamax and smaller. No Capesize.',
  },

  GANGAVARAM: {
    id: 'GANGAVARAM',
    name: 'Gangavaram',
    fullName: 'Gangavaram Port',
    country: 'India',
    region: REGIONS.INDIA_EAST,
    type: PORT_TYPES.DISCHARGE,
    lat: 17.6200,
    lng: 83.2400,
    unlocode: 'INGAG',
    maxLOA: 300,
    maxBeam: 50,
    maxDraft: 18.0,
    channelDepth: 21.0,
    cargoHandlingRate: 40000,
    berthCount: 6,
    tidalDependent: false,
    pilotageRequired: true,
    nightNavigation: true,
    canHandleCapesize: true,
    portCharges: 2.5,
    avgCongestionDays: 1.5,
    cargoTypes: ['Coal', 'Iron Ore', 'Limestone', 'Bauxite', 'Sugar'],
    seasonalRisks: {
      monsoon: { months: [6, 7, 8, 9], impact: 'moderate', delayDays: 1 },
      cyclone: { months: [10, 11, 12], impact: 'high', delayDays: 3 },
    },
    notes: 'Modern deep-draft port. 21m channel depth. Can handle Super Capesize.',
  },

  GOPALPUR: {
    id: 'GOPALPUR',
    name: 'Gopalpur',
    fullName: 'Gopalpur Port',
    country: 'India',
    region: REGIONS.INDIA_EAST,
    type: PORT_TYPES.DISCHARGE,
    lat: 19.2583,
    lng: 84.9053,
    unlocode: 'INGOP',
    maxLOA: 300,
    maxBeam: 46,
    maxDraft: 14.5,
    channelDepth: 16.0,
    cargoHandlingRate: 25000,
    berthCount: 3,
    tidalDependent: false,
    pilotageRequired: true,
    nightNavigation: true,
    canHandleCapesize: true,
    portCharges: 2.2,
    avgCongestionDays: 1,
    cargoTypes: ['Coal', 'Iron Ore', 'Limestone', 'Ilmenite', 'Alumina'],
    seasonalRisks: {
      monsoon: { months: [6, 7, 8, 9], impact: 'moderate', delayDays: 1.5 },
      cyclone: { months: [10, 11, 12], impact: 'high', delayDays: 4 },
    },
    notes: 'All-weather, multi-cargo facility. 20 MMTPA capacity. Can handle Capesize with draft restrictions.',
  },

  DHAMRA: {
    id: 'DHAMRA',
    name: 'Dhamra',
    fullName: 'Dhamra Port',
    country: 'India',
    region: REGIONS.INDIA_EAST,
    type: PORT_TYPES.DISCHARGE,
    lat: 20.7800,
    lng: 86.9500,
    unlocode: 'INDHA',
    maxLOA: 290,
    maxBeam: 47,
    maxDraft: 18.0,
    channelDepth: 18.5,
    cargoHandlingRate: 45000,
    berthCount: 4,
    tidalDependent: false,
    pilotageRequired: true,
    nightNavigation: true,
    canHandleCapesize: true,
    portCharges: 2.6,
    avgCongestionDays: 1,
    cargoTypes: ['Coal', 'Iron Ore', 'Limestone', 'Fertilizer'],
    seasonalRisks: {
      monsoon: { months: [6, 7, 8, 9], impact: 'low', delayDays: 1 },
      cyclone: { months: [10, 11, 12], impact: 'high', delayDays: 3 },
    },
    notes: 'Adani-operated. Super Capesize capable (up to 180,000 DWT). Deepest port on east coast.',
  },

  SAGAR_SANDHEADS: {
    id: 'SAGAR_SANDHEADS',
    name: 'Sagar-Sandheads',
    fullName: 'Sagar-Sandheads Anchorage',
    country: 'India',
    region: REGIONS.INDIA_EAST,
    type: PORT_TYPES.DISCHARGE,
    lat: 21.0000,
    lng: 88.0500,
    unlocode: 'INSGR',
    maxLOA: 999,     // No dimensional limit
    maxBeam: 999,
    maxDraft: 10.5,   // NX3 anchorage
    channelDepth: 10.5,
    cargoHandlingRate: 15000,    // Lighterage is slower
    berthCount: 0,               // Anchorage only
    tidalDependent: true,
    pilotageRequired: true,
    nightNavigation: false,
    canHandleCapesize: true,     // Via lighterage
    portCharges: 4.0,            // Higher due to lighterage
    avgCongestionDays: 3,
    cargoTypes: ['Coal', 'Iron Ore'],
    lighterage: true,
    lighterageDetails: {
      NX1: { draft: 9.5 },
      NX2: { draft: 10.0 },
      NX3: { draft: 10.5 },
    },
    seasonalRisks: {
      monsoon: { months: [6, 7, 8, 9], impact: 'high', delayDays: 5 },
      cyclone: { months: [10, 11, 12], impact: 'very_high', delayDays: 7 },
    },
    notes: 'Midstream lighterage anchorage for Kolkata/Haldia. Handles Capesize via ship-to-ship transfer. Weather dependent.',
  },

  HALDIA: {
    id: 'HALDIA',
    name: 'Haldia',
    fullName: 'Haldia Dock Complex (SMP Kolkata)',
    country: 'India',
    region: REGIONS.INDIA_EAST,
    type: PORT_TYPES.DISCHARGE,
    lat: 22.0200,
    lng: 88.0600,
    unlocode: 'INHAL',
    maxLOA: 230,
    maxBeam: 32,
    maxDraft: 8.5,
    channelDepth: 8.5,
    cargoHandlingRate: 12000,
    berthCount: 12,
    tidalDependent: true,
    pilotageRequired: true,
    nightNavigation: false,
    canHandleCapesize: false,
    portCharges: 3.5,
    avgCongestionDays: 4,
    cargoTypes: ['Coal', 'Iron Ore', 'POL', 'Chemicals', 'Containers'],
    seasonalRisks: {
      monsoon: { months: [6, 7, 8, 9], impact: 'high', delayDays: 4 },
      cyclone: { months: [10, 11, 12], impact: 'very_high', delayDays: 5 },
    },
    notes: 'Riverine port on Hooghly River. Severe draft restriction (8.5m). Tidal-dependent. Lighterage often required at Sandheads before entry.',
  },

  // ================================================================
  //  AUSTRALIA — LOADING PORTS
  // ================================================================

  NEWCASTLE: {
    id: 'NEWCASTLE',
    name: 'Newcastle',
    fullName: 'Port of Newcastle (Kooragang)',
    country: 'Australia',
    region: REGIONS.AUSTRALIA,
    type: PORT_TYPES.LOADING,
    lat: -32.9283,
    lng: 151.7817,
    unlocode: 'AUNTL',
    maxLOA: 300,
    maxBeam: 50,
    maxDraft: 16.5,
    channelDepth: 17.0,
    cargoHandlingRate: 80000,
    berthCount: 6,
    tidalDependent: false,
    pilotageRequired: true,
    nightNavigation: true,
    canHandleCapesize: true,
    portCharges: 3.5,
    avgCongestionDays: 2,
    cargoTypes: ['Thermal Coal', 'Met Coal'],
    loadingTerminals: ['Kooragang (PWCS)', 'Carrington (PWCS)', 'NCIG'],
    seasonalRisks: {
      weather: { months: [1, 2, 3, 12], impact: 'low', delayDays: 0.5 },
    },
    notes: 'World\'s largest coal export port. RightShip vetting required.',
  },

  HAY_POINT: {
    id: 'HAY_POINT',
    name: 'Hay Point / DBCT',
    fullName: 'Hay Point & Dalrymple Bay Coal Terminal',
    country: 'Australia',
    region: REGIONS.AUSTRALIA,
    type: PORT_TYPES.LOADING,
    lat: -21.2922,
    lng: 149.3044,
    unlocode: 'AUHPT',
    maxLOA: 300,
    maxBeam: 50,
    maxDraft: 18.5,
    channelDepth: 19.0,
    cargoHandlingRate: 70000,
    berthCount: 5,
    tidalDependent: true,
    pilotageRequired: true,
    nightNavigation: true,
    canHandleCapesize: true,
    portCharges: 3.2,
    avgCongestionDays: 3,
    cargoTypes: ['Met Coal', 'Thermal Coal'],
    loadingTerminals: ['HPCT (BMA)', 'DBCT'],
    seasonalRisks: {
      cyclone: { months: [11, 12, 1, 2, 3], impact: 'moderate', delayDays: 2 },
    },
    notes: 'Offshore berths via jetties. 7.14m tidal range. Can handle 220,000 DWT at DBCT.',
  },

  GLADSTONE: {
    id: 'GLADSTONE',
    name: 'Gladstone',
    fullName: 'Port of Gladstone',
    country: 'Australia',
    region: REGIONS.AUSTRALIA,
    type: PORT_TYPES.LOADING,
    lat: -23.8480,
    lng: 151.2840,
    unlocode: 'AUGLF',
    maxLOA: 280,
    maxBeam: 45,
    maxDraft: 14.0,
    channelDepth: 15.0,
    cargoHandlingRate: 50000,
    berthCount: 4,
    tidalDependent: true,
    pilotageRequired: true,
    nightNavigation: true,
    canHandleCapesize: true,
    portCharges: 3.0,
    avgCongestionDays: 2,
    cargoTypes: ['Thermal Coal', 'Met Coal', 'Alumina'],
    seasonalRisks: {
      cyclone: { months: [11, 12, 1, 2, 3], impact: 'low', delayDays: 1 },
    },
    notes: 'Multi-cargo port. Coal terminals: Wiggins Island and Barney Point (closed for coal).',
  },

  // ================================================================
  //  USA — LOADING PORTS
  // ================================================================

  HAMPTON_ROADS: {
    id: 'HAMPTON_ROADS',
    name: 'Hampton Roads',
    fullName: 'Hampton Roads (Lamberts Point / DTA)',
    country: 'USA',
    region: REGIONS.USA,
    type: PORT_TYPES.LOADING,
    lat: 36.8946,
    lng: -76.3300,
    unlocode: 'USHRP',
    maxLOA: 305,
    maxBeam: 48,
    maxDraft: 15.2,
    channelDepth: 15.2,
    cargoHandlingRate: 60000,
    berthCount: 4,
    tidalDependent: false,
    pilotageRequired: true,
    nightNavigation: true,
    canHandleCapesize: true,
    portCharges: 4.0,
    avgCongestionDays: 2,
    cargoTypes: ['Met Coal', 'Thermal Coal', 'Pet Coke'],
    loadingTerminals: ['Lamberts Point (Norfolk Southern)', 'DTA (Newport News)', 'Pier IX (Kinder Morgan)'],
    seasonalRisks: {
      hurricane: { months: [8, 9, 10], impact: 'low', delayDays: 1 },
      winter: { months: [12, 1, 2], impact: 'low', delayDays: 0.5 },
    },
    notes: 'Largest coal export terminal in Northern Hemisphere. Vessels must be < 20 years old. Gearless single-deck required.',
  },

  BALTIMORE: {
    id: 'BALTIMORE',
    name: 'Baltimore',
    fullName: 'Port of Baltimore (Curtis Bay)',
    country: 'USA',
    region: REGIONS.USA,
    type: PORT_TYPES.LOADING,
    lat: 39.2530,
    lng: -76.5796,
    unlocode: 'USBAL',
    maxLOA: 275,
    maxBeam: 42,
    maxDraft: 12.8,
    channelDepth: 15.2,
    cargoHandlingRate: 40000,
    berthCount: 3,
    tidalDependent: false,
    pilotageRequired: true,
    nightNavigation: true,
    canHandleCapesize: false,
    portCharges: 3.8,
    avgCongestionDays: 1,
    cargoTypes: ['Met Coal', 'Thermal Coal'],
    loadingTerminals: ['Curtis Bay Coal Pier (CSX)', 'Deep Draft Export Pier'],
    seasonalRisks: {
      winter: { months: [12, 1, 2], impact: 'low', delayDays: 0.5 },
    },
    notes: 'Panamax max. Curtis Bay coal pier 40ft MLW. 58ft air draft limit.',
  },

  // ================================================================
  //  MOZAMBIQUE — LOADING PORTS
  // ================================================================

  NACALA: {
    id: 'NACALA',
    name: 'Nacala-a-Velha',
    fullName: 'Nacala-a-Velha Coal Terminal',
    country: 'Mozambique',
    region: REGIONS.MOZAMBIQUE,
    type: PORT_TYPES.LOADING,
    lat: -14.5425,
    lng: 40.6850,
    unlocode: 'MZNVH',
    maxLOA: 280,
    maxBeam: 45,
    maxDraft: 15.0,
    channelDepth: 16.0,
    cargoHandlingRate: 30000,
    berthCount: 2,
    tidalDependent: false,
    pilotageRequired: true,
    nightNavigation: false,
    canHandleCapesize: true,
    portCharges: 3.0,
    avgCongestionDays: 2,
    cargoTypes: ['Met Coal', 'Thermal Coal'],
    seasonalRisks: {
      cyclone: { months: [1, 2, 3, 4], impact: 'moderate', delayDays: 2 },
    },
    notes: 'Dedicated coal export terminal. Natural deep-water port. Rail connected to Moatize mines.',
  },

  BEIRA: {
    id: 'BEIRA',
    name: 'Beira',
    fullName: 'Port of Beira',
    country: 'Mozambique',
    region: REGIONS.MOZAMBIQUE,
    type: PORT_TYPES.LOADING,
    lat: -19.8333,
    lng: 34.8667,
    unlocode: 'MZBEW',
    maxLOA: 230,
    maxBeam: 32,
    maxDraft: 11.0,
    channelDepth: 11.5,
    cargoHandlingRate: 15000,
    berthCount: 3,
    tidalDependent: true,
    pilotageRequired: true,
    nightNavigation: false,
    canHandleCapesize: false,
    portCharges: 3.5,
    avgCongestionDays: 3,
    cargoTypes: ['Thermal Coal', 'Chrome', 'General Cargo'],
    seasonalRisks: {
      cyclone: { months: [1, 2, 3, 4], impact: 'high', delayDays: 4 },
    },
    notes: 'Major Mozambique hub. Limited to Supramax-max due to draft. Siltation issues.',
  },

  // ================================================================
  //  INDONESIA — LOADING PORTS
  // ================================================================

  KALIMANTAN: {
    id: 'KALIMANTAN',
    name: 'Kalimantan (STS)',
    fullName: 'Kalimantan Anchorage / Taboneo',
    country: 'Indonesia',
    region: REGIONS.INDONESIA,
    type: PORT_TYPES.LOADING,
    lat: -3.5000,
    lng: 114.8000,
    unlocode: 'IDTAB',
    maxLOA: 300,
    maxBeam: 50,
    maxDraft: 14.0,
    channelDepth: 14.0,
    cargoHandlingRate: 25000,
    berthCount: 0,       // Anchorage-based
    tidalDependent: false,
    pilotageRequired: true,
    nightNavigation: false,
    canHandleCapesize: true,
    portCharges: 2.5,
    avgCongestionDays: 2,
    cargoTypes: ['Thermal Coal'],
    anchorageBased: true,
    seasonalRisks: {
      monsoon: { months: [11, 12, 1, 2], impact: 'moderate', delayDays: 2 },
    },
    notes: 'Anchorage-based loading via STS/barge transfer. Weather-dependent. Security concerns at some locations.',
  },

  // ================================================================
  //  RUSSIA — LOADING PORTS
  // ================================================================

  VANINO: {
    id: 'VANINO',
    name: 'Vanino',
    fullName: 'Port of Vanino',
    country: 'Russia',
    region: REGIONS.RUSSIA,
    type: PORT_TYPES.LOADING,
    lat: 49.0900,
    lng: 140.2500,
    unlocode: 'RUVNN',
    maxLOA: 260,
    maxBeam: 40,
    maxDraft: 13.5,
    channelDepth: 14.0,
    cargoHandlingRate: 35000,
    berthCount: 4,
    tidalDependent: false,
    pilotageRequired: true,
    nightNavigation: true,
    canHandleCapesize: false,
    portCharges: 3.2,
    avgCongestionDays: 3,
    cargoTypes: ['Thermal Coal', 'Met Coal'],
    seasonalRisks: {
      ice: { months: [12, 1, 2, 3], impact: 'high', delayDays: 4 },
    },
    notes: 'Russian Far East coal export hub. Panamax-max. Ice navigation in winter.',
  },

  VOSTOCHNY: {
    id: 'VOSTOCHNY',
    name: 'Vostochny',
    fullName: 'Port of Vostochny',
    country: 'Russia',
    region: REGIONS.RUSSIA,
    type: PORT_TYPES.LOADING,
    lat: 42.7500,
    lng: 133.0600,
    unlocode: 'RUVVO',
    maxLOA: 290,
    maxBeam: 45,
    maxDraft: 15.5,
    channelDepth: 16.0,
    cargoHandlingRate: 50000,
    berthCount: 6,
    tidalDependent: false,
    pilotageRequired: true,
    nightNavigation: true,
    canHandleCapesize: true,
    portCharges: 3.0,
    avgCongestionDays: 2,
    cargoTypes: ['Thermal Coal', 'Met Coal'],
    seasonalRisks: {
      ice: { months: [12, 1, 2, 3], impact: 'moderate', delayDays: 2 },
    },
    notes: 'Largest coal export terminal in Russian Far East. Can handle Capesize vessels.',
  },
};


// ================================================================
//  Utility Functions
// ================================================================

/**
 * Get all discharge (India East Coast) ports
 */
export function getDischargePorts() {
  return Object.values(PORTS).filter(p => p.type === PORT_TYPES.DISCHARGE);
}

/**
 * Get all loading (origin) ports
 */
export function getLoadingPorts() {
  return Object.values(PORTS).filter(p => p.type === PORT_TYPES.LOADING);
}

/**
 * Get ports by region
 */
export function getPortsByRegion(region) {
  return Object.values(PORTS).filter(p => p.region === region);
}

/**
 * Check if a vessel can berth at a port
 */
export function canVesselBerth(vessel, port) {
  const checks = {
    loa: vessel.loa <= port.maxLOA,
    beam: vessel.beam <= port.maxBeam,
    draft: vessel.maxDraft <= port.maxDraft,
  };
  return {
    ...checks,
    feasible: checks.loa && checks.beam && checks.draft,
    limitingFactor: !checks.draft ? 'draft' : !checks.loa ? 'LOA' : !checks.beam ? 'beam' : null,
  };
}

/**
 * Calculate estimated turnaround time at port
 */
export function estimateTurnaround(cargoMT, port) {
  const handlingDays = cargoMT / port.cargoHandlingRate;
  const congestionDays = port.avgCongestionDays;
  const berthingTime = 0.5; // days for berthing/unberthing
  return {
    handlingDays: Math.round(handlingDays * 10) / 10,
    congestionDays,
    berthingTime,
    totalDays: Math.round((handlingDays + congestionDays + berthingTime) * 10) / 10,
  };
}

/**
 * Get seasonal risk for a port at a given month
 */
export function getSeasonalRisk(port, month) {
  const risks = [];
  for (const [riskType, riskData] of Object.entries(port.seasonalRisks)) {
    if (riskData.months.includes(month)) {
      risks.push({ type: riskType, impact: riskData.impact, delayDays: riskData.delayDays });
    }
  }
  return risks;
}
