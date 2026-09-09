/**
 * FreightForecast Pro — Trade Route Database
 * Distances, transit times, and route characteristics for
 * all origin-destination pairs.
 */

/**
 * Route definitions: distances in nautical miles, transit times in days.
 * Key: `${originId}_${destId}`
 */
export const ROUTES = {
  // ================================================================
  //  AUSTRALIA → INDIA EAST COAST
  // ================================================================

  NEWCASTLE_PARADIP:       { origin: 'NEWCASTLE', dest: 'PARADIP',        distanceNM: 6050, transitDays: { min: 18, max: 22 }, chokepoints: ['Torres Strait'], tradeLane: 'Australia-India East', backhaul: 'Iron Ore (India → China possible)' },
  NEWCASTLE_VIZAG:         { origin: 'NEWCASTLE', dest: 'VIZAG',          distanceNM: 5900, transitDays: { min: 17, max: 21 }, chokepoints: ['Torres Strait'], tradeLane: 'Australia-India East', backhaul: 'Iron Ore' },
  NEWCASTLE_GANGAVARAM:    { origin: 'NEWCASTLE', dest: 'GANGAVARAM',     distanceNM: 5880, transitDays: { min: 17, max: 21 }, chokepoints: ['Torres Strait'], tradeLane: 'Australia-India East', backhaul: 'Iron Ore' },
  NEWCASTLE_GOPALPUR:      { origin: 'NEWCASTLE', dest: 'GOPALPUR',       distanceNM: 6000, transitDays: { min: 18, max: 22 }, chokepoints: ['Torres Strait'], tradeLane: 'Australia-India East', backhaul: 'Iron Ore' },
  NEWCASTLE_DHAMRA:        { origin: 'NEWCASTLE', dest: 'DHAMRA',         distanceNM: 6150, transitDays: { min: 19, max: 23 }, chokepoints: ['Torres Strait'], tradeLane: 'Australia-India East', backhaul: 'Iron Ore' },
  NEWCASTLE_SAGAR:         { origin: 'NEWCASTLE', dest: 'SAGAR_SANDHEADS',distanceNM: 6250, transitDays: { min: 19, max: 23 }, chokepoints: ['Torres Strait'], tradeLane: 'Australia-India East', backhaul: 'Iron Ore' },
  NEWCASTLE_HALDIA:        { origin: 'NEWCASTLE', dest: 'HALDIA',         distanceNM: 6300, transitDays: { min: 19, max: 24 }, chokepoints: ['Torres Strait'], tradeLane: 'Australia-India East', backhaul: 'Iron Ore' },

  HAY_POINT_PARADIP:       { origin: 'HAY_POINT', dest: 'PARADIP',        distanceNM: 5800, transitDays: { min: 17, max: 21 }, chokepoints: ['Torres Strait'], tradeLane: 'Australia-India East', backhaul: 'Iron Ore' },
  HAY_POINT_VIZAG:         { origin: 'HAY_POINT', dest: 'VIZAG',          distanceNM: 5650, transitDays: { min: 16, max: 20 }, chokepoints: ['Torres Strait'], tradeLane: 'Australia-India East', backhaul: 'Iron Ore' },
  HAY_POINT_GANGAVARAM:    { origin: 'HAY_POINT', dest: 'GANGAVARAM',     distanceNM: 5700, transitDays: { min: 17, max: 20 }, chokepoints: ['Torres Strait'], tradeLane: 'Australia-India East', backhaul: 'Iron Ore' },
  HAY_POINT_DHAMRA:        { origin: 'HAY_POINT', dest: 'DHAMRA',         distanceNM: 5950, transitDays: { min: 18, max: 22 }, chokepoints: ['Torres Strait'], tradeLane: 'Australia-India East', backhaul: 'Iron Ore' },

  GLADSTONE_PARADIP:       { origin: 'GLADSTONE', dest: 'PARADIP',        distanceNM: 5900, transitDays: { min: 17, max: 21 }, chokepoints: ['Torres Strait'], tradeLane: 'Australia-India East', backhaul: 'Alumina' },
  GLADSTONE_VIZAG:         { origin: 'GLADSTONE', dest: 'VIZAG',          distanceNM: 5750, transitDays: { min: 17, max: 20 }, chokepoints: ['Torres Strait'], tradeLane: 'Australia-India East', backhaul: 'Alumina' },
  GLADSTONE_GANGAVARAM:    { origin: 'GLADSTONE', dest: 'GANGAVARAM',     distanceNM: 5730, transitDays: { min: 17, max: 20 }, chokepoints: ['Torres Strait'], tradeLane: 'Australia-India East', backhaul: 'Alumina' },

  // ================================================================
  //  USA → INDIA EAST COAST
  // ================================================================

  HAMPTON_ROADS_PARADIP:   { origin: 'HAMPTON_ROADS', dest: 'PARADIP',        distanceNM: 10200, transitDays: { min: 30, max: 35 }, chokepoints: ['Suez Canal / Cape of Good Hope'], tradeLane: 'US East-India', backhaul: 'Ballast (typically)' },
  HAMPTON_ROADS_VIZAG:     { origin: 'HAMPTON_ROADS', dest: 'VIZAG',          distanceNM: 10050, transitDays: { min: 29, max: 34 }, chokepoints: ['Suez Canal / Cape of Good Hope'], tradeLane: 'US East-India', backhaul: 'Ballast' },
  HAMPTON_ROADS_GANGAVARAM:{ origin: 'HAMPTON_ROADS', dest: 'GANGAVARAM',     distanceNM: 10030, transitDays: { min: 29, max: 34 }, chokepoints: ['Suez Canal / Cape of Good Hope'], tradeLane: 'US East-India', backhaul: 'Ballast' },
  HAMPTON_ROADS_DHAMRA:    { origin: 'HAMPTON_ROADS', dest: 'DHAMRA',         distanceNM: 10400, transitDays: { min: 31, max: 36 }, chokepoints: ['Suez Canal / Cape of Good Hope'], tradeLane: 'US East-India', backhaul: 'Ballast' },
  HAMPTON_ROADS_HALDIA:    { origin: 'HAMPTON_ROADS', dest: 'HALDIA',         distanceNM: 10500, transitDays: { min: 31, max: 37 }, chokepoints: ['Suez Canal / Cape of Good Hope'], tradeLane: 'US East-India', backhaul: 'Ballast' },

  BALTIMORE_PARADIP:       { origin: 'BALTIMORE', dest: 'PARADIP',        distanceNM: 10300, transitDays: { min: 30, max: 36 }, chokepoints: ['Suez Canal / Cape of Good Hope'], tradeLane: 'US East-India', backhaul: 'Ballast' },
  BALTIMORE_VIZAG:         { origin: 'BALTIMORE', dest: 'VIZAG',          distanceNM: 10150, transitDays: { min: 30, max: 35 }, chokepoints: ['Suez Canal / Cape of Good Hope'], tradeLane: 'US East-India', backhaul: 'Ballast' },

  // ================================================================
  //  MOZAMBIQUE → INDIA EAST COAST
  // ================================================================

  NACALA_PARADIP:          { origin: 'NACALA', dest: 'PARADIP',        distanceNM: 4050, transitDays: { min: 11, max: 14 }, chokepoints: ['Mozambique Channel'], tradeLane: 'Mozambique-India East', backhaul: 'Ballast / General Cargo' },
  NACALA_VIZAG:            { origin: 'NACALA', dest: 'VIZAG',          distanceNM: 3900, transitDays: { min: 11, max: 14 }, chokepoints: ['Mozambique Channel'], tradeLane: 'Mozambique-India East', backhaul: 'Ballast' },
  NACALA_GANGAVARAM:       { origin: 'NACALA', dest: 'GANGAVARAM',     distanceNM: 3880, transitDays: { min: 11, max: 13 }, chokepoints: ['Mozambique Channel'], tradeLane: 'Mozambique-India East', backhaul: 'Ballast' },
  NACALA_DHAMRA:           { origin: 'NACALA', dest: 'DHAMRA',         distanceNM: 4200, transitDays: { min: 12, max: 15 }, chokepoints: ['Mozambique Channel'], tradeLane: 'Mozambique-India East', backhaul: 'Ballast' },
  NACALA_GOPALPUR:         { origin: 'NACALA', dest: 'GOPALPUR',       distanceNM: 3950, transitDays: { min: 11, max: 14 }, chokepoints: ['Mozambique Channel'], tradeLane: 'Mozambique-India East', backhaul: 'Ballast' },

  BEIRA_PARADIP:           { origin: 'BEIRA', dest: 'PARADIP',        distanceNM: 4300, transitDays: { min: 12, max: 16 }, chokepoints: ['Mozambique Channel'], tradeLane: 'Mozambique-India East', backhaul: 'Ballast' },
  BEIRA_VIZAG:             { origin: 'BEIRA', dest: 'VIZAG',          distanceNM: 4150, transitDays: { min: 12, max: 15 }, chokepoints: ['Mozambique Channel'], tradeLane: 'Mozambique-India East', backhaul: 'Ballast' },

  // ================================================================
  //  INDONESIA → INDIA EAST COAST
  // ================================================================

  KALIMANTAN_PARADIP:      { origin: 'KALIMANTAN', dest: 'PARADIP',        distanceNM: 2400, transitDays: { min: 7, max: 9 },  chokepoints: ['Malacca Strait'], tradeLane: 'Indonesia-India East', backhaul: 'Ballast' },
  KALIMANTAN_VIZAG:        { origin: 'KALIMANTAN', dest: 'VIZAG',          distanceNM: 2250, transitDays: { min: 6, max: 8 },  chokepoints: ['Malacca Strait'], tradeLane: 'Indonesia-India East', backhaul: 'Ballast' },
  KALIMANTAN_GANGAVARAM:   { origin: 'KALIMANTAN', dest: 'GANGAVARAM',     distanceNM: 2230, transitDays: { min: 6, max: 8 },  chokepoints: ['Malacca Strait'], tradeLane: 'Indonesia-India East', backhaul: 'Ballast' },
  KALIMANTAN_GOPALPUR:     { origin: 'KALIMANTAN', dest: 'GOPALPUR',       distanceNM: 2350, transitDays: { min: 7, max: 9 },  chokepoints: ['Malacca Strait'], tradeLane: 'Indonesia-India East', backhaul: 'Ballast' },
  KALIMANTAN_DHAMRA:       { origin: 'KALIMANTAN', dest: 'DHAMRA',         distanceNM: 2500, transitDays: { min: 7, max: 10 }, chokepoints: ['Malacca Strait'], tradeLane: 'Indonesia-India East', backhaul: 'Ballast' },
  KALIMANTAN_SAGAR:        { origin: 'KALIMANTAN', dest: 'SAGAR_SANDHEADS',distanceNM: 2550, transitDays: { min: 7, max: 10 }, chokepoints: ['Malacca Strait'], tradeLane: 'Indonesia-India East', backhaul: 'Ballast' },
  KALIMANTAN_HALDIA:       { origin: 'KALIMANTAN', dest: 'HALDIA',         distanceNM: 2600, transitDays: { min: 8, max: 10 }, chokepoints: ['Malacca Strait'], tradeLane: 'Indonesia-India East', backhaul: 'Ballast' },

  // ================================================================
  //  RUSSIA → INDIA EAST COAST
  // ================================================================

  VANINO_PARADIP:          { origin: 'VANINO', dest: 'PARADIP',        distanceNM: 4750, transitDays: { min: 14, max: 17 }, chokepoints: [], tradeLane: 'Russia Far East-India', backhaul: 'Ballast' },
  VANINO_VIZAG:            { origin: 'VANINO', dest: 'VIZAG',          distanceNM: 4800, transitDays: { min: 14, max: 17 }, chokepoints: [], tradeLane: 'Russia Far East-India', backhaul: 'Ballast' },
  VANINO_DHAMRA:           { origin: 'VANINO', dest: 'DHAMRA',         distanceNM: 4900, transitDays: { min: 14, max: 18 }, chokepoints: [], tradeLane: 'Russia Far East-India', backhaul: 'Ballast' },

  VOSTOCHNY_PARADIP:       { origin: 'VOSTOCHNY', dest: 'PARADIP',    distanceNM: 4700, transitDays: { min: 14, max: 17 }, chokepoints: [], tradeLane: 'Russia Far East-India', backhaul: 'Ballast' },
  VOSTOCHNY_VIZAG:         { origin: 'VOSTOCHNY', dest: 'VIZAG',      distanceNM: 4750, transitDays: { min: 14, max: 17 }, chokepoints: [], tradeLane: 'Russia Far East-India', backhaul: 'Ballast' },
  VOSTOCHNY_GANGAVARAM:    { origin: 'VOSTOCHNY', dest: 'GANGAVARAM', distanceNM: 4730, transitDays: { min: 14, max: 17 }, chokepoints: [], tradeLane: 'Russia Far East-India', backhaul: 'Ballast' },
  VOSTOCHNY_DHAMRA:        { origin: 'VOSTOCHNY', dest: 'DHAMRA',     distanceNM: 4850, transitDays: { min: 14, max: 18 }, chokepoints: [], tradeLane: 'Russia Far East-India', backhaul: 'Ballast' },
};


// ================================================================
//  Utility Functions
// ================================================================

/**
 * Get route key from origin and destination IDs
 */
export function getRouteKey(originId, destId) {
  return `${originId}_${destId}`;
}

/**
 * Find a route between two ports
 */
export function findRoute(originId, destId) {
  const key = getRouteKey(originId, destId);
  return ROUTES[key] || null;
}

/**
 * Get all routes from a given origin
 */
export function getRoutesFromOrigin(originId) {
  return Object.entries(ROUTES)
    .filter(([_, r]) => r.origin === originId)
    .map(([key, r]) => ({ key, ...r }));
}

/**
 * Get all routes to a given destination
 */
export function getRoutesToDest(destId) {
  return Object.entries(ROUTES)
    .filter(([_, r]) => r.dest === destId)
    .map(([key, r]) => ({ key, ...r }));
}

/**
 * Get all unique trade lanes
 */
export function getTradeLanes() {
  const lanes = new Set(Object.values(ROUTES).map(r => r.tradeLane));
  return Array.from(lanes);
}

/**
 * Calculate estimated transit time for a given vessel speed
 */
export function calculateTransit(distanceNM, speedKnots) {
  return Math.round((distanceNM / (speedKnots * 24)) * 10) / 10;
}

/**
 * Get route comparison for same cargo to different destinations
 */
export function compareRoutes(originId, destIds) {
  return destIds.map(destId => {
    const route = findRoute(originId, destId);
    return route ? { destId, ...route } : null;
  }).filter(Boolean);
}

/**
 * Get all routes as an array with computed key
 */
export function getAllRoutes() {
  return Object.entries(ROUTES).map(([key, r]) => ({ key, ...r }));
}
