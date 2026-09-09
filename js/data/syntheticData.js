/**
 * FreightForecast Pro — Synthetic Freight Rate Data Generator
 * Generates realistic daily freight rate data modeled after Baltic Exchange patterns.
 * Models seasonality, volatility, cross-class correlations, and macro trends.
 */

/**
 * Seeded pseudo-random number generator (mulberry32)
 * Ensures reproducible synthetic data across sessions.
 */
function createRNG(seed) {
  let s = seed | 0;
  return function () {
    s = (s + 0x6D2B79F5) | 0;
    let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/**
 * Box-Muller transform for normal distribution
 */
function normalRandom(rng, mean = 0, stddev = 1) {
  const u1 = rng();
  const u2 = rng();
  const z = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
  return mean + stddev * z;
}

/**
 * Base freight rate profiles for each vessel class ($/day time charter equivalent)
 */
const BASE_RATES = {
  HANDYSIZE: { base: 10500, volatility: 1800,  seasonalAmp: 1500,  trendAmp: 2000 },
  SUPRAMAX:  { base: 14500, volatility: 2500,  seasonalAmp: 2200,  trendAmp: 3000 },
  PANAMAX:   { base: 17500, volatility: 3200,  seasonalAmp: 2800,  trendAmp: 4000 },
  CAPESIZE:  { base: 24000, volatility: 6000,  seasonalAmp: 5000,  trendAmp: 8000 },
};

/**
 * Seasonal pattern: models Indian coal import demand, monsoon effects,
 * Chinese New Year dip, and Australian cyclone season.
 * Returns a multiplier [-1, 1] for a given day-of-year.
 */
function getSeasonalFactor(dayOfYear) {
  // Primary annual cycle — peak in Q4 (pre-monsoon stocking + winter demand)
  const primary = Math.sin((dayOfYear - 60) / 365 * 2 * Math.PI) * 0.4;
  // Secondary cycle — mini-peak in Q2 (post-Chinese New Year restocking)
  const secondary = Math.sin((dayOfYear - 30) / 182.5 * 2 * Math.PI) * 0.2;
  // Chinese New Year dip (around day 35-50)
  const cnyDip = dayOfYear > 25 && dayOfYear < 55 ? -0.3 * Math.exp(-((dayOfYear - 40) ** 2) / 50) : 0;
  // Monsoon suppression (India, Jun-Aug, days 152-243)
  const monsoon = dayOfYear > 152 && dayOfYear < 243 ? -0.15 * Math.sin((dayOfYear - 152) / 91 * Math.PI) : 0;

  return primary + secondary + cnyDip + monsoon;
}

/**
 * Generate a multi-year macro trend component.
 * Models boom-bust cycles (~3-4 year period).
 */
function getMacroTrend(dayIndex, totalDays, rng) {
  const cyclePeriod = 365 * 3.5; // ~3.5 year cycle
  const phase = rng() * Math.PI * 2;
  return Math.sin((dayIndex / cyclePeriod) * 2 * Math.PI + phase);
}

/**
 * Generate synthetic daily freight rates for a vessel class.
 * @param {string} vesselClassId - e.g. 'CAPESIZE'
 * @param {number} years - number of years of history
 * @param {number} seed - random seed for reproducibility
 * @returns {Array<{date: string, rate: number, bdi: number}>}
 */
export function generateFreightRates(vesselClassId, years = 3, seed = 42) {
  const rng = createRNG(seed + vesselClassId.charCodeAt(0));
  const profile = BASE_RATES[vesselClassId];
  if (!profile) throw new Error(`Unknown vessel class: ${vesselClassId}`);

  const totalDays = years * 365;
  const rates = [];
  let prevRate = profile.base;
  const macroPhase = rng() * Math.PI * 2;

  // Start date: 3 years before today
  const startDate = new Date();
  startDate.setFullYear(startDate.getFullYear() - years);
  startDate.setHours(0, 0, 0, 0);

  for (let i = 0; i < totalDays; i++) {
    const date = new Date(startDate);
    date.setDate(date.getDate() + i);

    const dayOfYear = getDayOfYear(date);

    // Seasonal component
    const seasonal = getSeasonalFactor(dayOfYear) * profile.seasonalAmp;

    // Macro trend (boom-bust)
    const macro = Math.sin((i / (365 * 3.5)) * 2 * Math.PI + macroPhase) * profile.trendAmp * 0.5;

    // Mean-reverting random walk
    const meanReversion = (profile.base - prevRate) * 0.02;
    const randomShock = normalRandom(rng, 0, profile.volatility * 0.08);

    // Occasional market events (spikes/crashes)
    let eventShock = 0;
    if (rng() < 0.005) { // ~0.5% chance per day = ~1.8 events/year
      eventShock = normalRandom(rng, 0, profile.volatility * 0.8);
    }

    let rate = prevRate + meanReversion + randomShock + eventShock;
    rate += seasonal * 0.01;  // Gradual seasonal influence
    rate += macro * 0.005;    // Slow macro influence

    // Ensure rate stays positive and within reasonable bounds
    rate = Math.max(profile.base * 0.3, Math.min(profile.base * 2.5, rate));

    prevRate = rate;
    rates.push({
      date: formatDate(date),
      dateObj: date,
      rate: Math.round(rate),
      dayOfYear,
    });
  }

  // Apply seasonal overlay more firmly (blend with running average)
  const smoothed = applySeasonalSmoothing(rates, profile);

  return smoothed;
}

/**
 * Apply seasonal smoothing to make seasonal patterns more visible
 */
function applySeasonalSmoothing(rates, profile) {
  return rates.map((r, i) => {
    const seasonal = getSeasonalFactor(r.dayOfYear) * profile.seasonalAmp;
    // Blend: 70% random walk + 30% seasonal pattern
    const blendedRate = r.rate * 0.7 + (profile.base + seasonal) * 0.3;
    return {
      ...r,
      rate: Math.round(blendedRate),
    };
  });
}

/**
 * Generate a composite BDI-like index from individual vessel class rates
 */
export function generateBDI(years = 3, seed = 42) {
  const handyRates = generateFreightRates('HANDYSIZE', years, seed);
  const supraRates = generateFreightRates('SUPRAMAX', years, seed);
  const panaRates = generateFreightRates('PANAMAX', years, seed);
  const capeRates = generateFreightRates('CAPESIZE', years, seed);

  return handyRates.map((_, i) => {
    // BDI is a weighted composite (Capesize has highest weight)
    const bdi = Math.round(
      capeRates[i].rate * 0.40 +
      panaRates[i].rate * 0.30 +
      supraRates[i].rate * 0.20 +
      handyRates[i].rate * 0.10
    ) / 10; // Scale down to BDI-like range

    return {
      date: handyRates[i].date,
      dateObj: handyRates[i].dateObj,
      bdi: Math.round(bdi),
      handysize: handyRates[i].rate,
      supramax: supraRates[i].rate,
      panamax: panaRates[i].rate,
      capesize: capeRates[i].rate,
    };
  });
}

/**
 * Generate route-specific freight rates ($/MT) from time charter rates
 */
export function generateRouteRates(vesselClassId, distanceNM, years = 3, seed = 42) {
  const tcRates = generateFreightRates(vesselClassId, years, seed);

  // Convert TC rate to $/MT using rough capacity and voyage economics
  const capacityMap = {
    HANDYSIZE: 28000,
    SUPRAMAX: 58000,
    PANAMAX: 75000,
    CAPESIZE: 170000,
  };
  const capacity = capacityMap[vesselClassId] || 58000;
  const speedKnots = 13.5;
  const voyageDays = distanceNM / (speedKnots * 24);

  return tcRates.map(r => {
    const voyageCost = r.rate * (voyageDays + 5); // +5 for port days
    const ratPerMT = voyageCost / capacity;
    return {
      ...r,
      ratePerMT: Math.round(ratPerMT * 100) / 100,
      voyageDays: Math.round(voyageDays * 10) / 10,
    };
  });
}

/**
 * Generate port congestion data
 */
export function generateCongestionData(portId, years = 1, seed = 42) {
  const rng = createRNG(seed + (portId.charCodeAt(0) * 100));
  const totalDays = years * 365;
  const data = [];

  const startDate = new Date();
  startDate.setFullYear(startDate.getFullYear() - years);

  for (let i = 0; i < totalDays; i++) {
    const date = new Date(startDate);
    date.setDate(date.getDate() + i);
    const dayOfYear = getDayOfYear(date);

    // Base congestion with seasonal pattern
    let vessels = Math.round(3 + rng() * 5 + Math.sin(dayOfYear / 365 * Math.PI * 2) * 3);
    vessels = Math.max(0, vessels);

    // Monsoon spike for Indian ports
    if (dayOfYear > 152 && dayOfYear < 243) {
      vessels += Math.round(rng() * 4);
    }

    data.push({
      date: formatDate(date),
      vesselsWaiting: vessels,
      avgWaitDays: Math.round((1 + vessels * 0.4 + rng() * 1.5) * 10) / 10,
    });
  }

  return data;
}

/**
 * Generate commodity price data (coal)
 */
export function generateCoalPrices(years = 3, seed = 99) {
  const rng = createRNG(seed);
  const totalDays = years * 365;
  const data = [];
  let prevPrice = 140; // $/MT Newcastle benchmark

  const startDate = new Date();
  startDate.setFullYear(startDate.getFullYear() - years);

  for (let i = 0; i < totalDays; i++) {
    const date = new Date(startDate);
    date.setDate(date.getDate() + i);

    const meanReversion = (140 - prevPrice) * 0.01;
    const shock = normalRandom(rng, 0, 3);
    let price = prevPrice + meanReversion + shock;
    price = Math.max(60, Math.min(300, price));
    prevPrice = price;

    data.push({
      date: formatDate(date),
      price: Math.round(price * 100) / 100,
    });
  }

  return data;
}


// ================================================================
//  Helpers
// ================================================================

function getDayOfYear(date) {
  const start = new Date(date.getFullYear(), 0, 0);
  const diff = date - start;
  return Math.floor(diff / (1000 * 60 * 60 * 24));
}

function formatDate(date) {
  return date.toISOString().split('T')[0];
}

/**
 * Pre-generate and cache all data for the dashboard
 */
export function generateAllData(years = 3, seed = 42) {
  return {
    bdi: generateBDI(years, seed),
    rates: {
      HANDYSIZE: generateFreightRates('HANDYSIZE', years, seed),
      SUPRAMAX: generateFreightRates('SUPRAMAX', years, seed),
      PANAMAX: generateFreightRates('PANAMAX', years, seed),
      CAPESIZE: generateFreightRates('CAPESIZE', years, seed),
    },
    coal: generateCoalPrices(years, seed + 10),
  };
}
