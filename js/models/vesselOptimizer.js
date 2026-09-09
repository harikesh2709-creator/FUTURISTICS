/**
 * FreightForecast Pro — Vessel Optimizer
 * Constraint satisfaction, cost optimization, and vessel-route matching.
 */

import { PORTS, canVesselBerth, estimateTurnaround } from '../data/portDatabase.js';
import { VESSEL_CLASSES, calculateFuelCost } from '../data/vesselDatabase.js';
import { findRoute } from '../data/routeDatabase.js';

/**
 * Run full vessel optimization for a given cargo requirement.
 * @param {Object} params
 * @param {string} params.originId      - Loading port ID
 * @param {string} params.destId        - Discharge port ID
 * @param {number} params.cargoMT       - Cargo quantity in metric tonnes
 * @param {number} [params.freightRate] - Current freight rate $/MT (optional, uses estimate)
 * @param {number} [params.fuelPrice]   - Fuel price $/MT (default 550)
 * @returns {Array} Ranked list of vessel recommendations
 */
export function optimizeVessel(params) {
  const { originId, destId, cargoMT, freightRate, fuelPrice = 550 } = params;

  const origin = PORTS[originId];
  const dest = PORTS[destId];
  const route = findRoute(originId, destId);

  if (!origin || !dest) return [];

  const results = [];

  for (const [classId, vessel] of Object.entries(VESSEL_CLASSES)) {
    // Create representative vessel dimensions
    const vesselSpec = {
      loa: vessel.loa.typical,
      beam: vessel.beam.typical,
      maxDraft: vessel.maxDraft.typical,
    };

    // Port feasibility checks
    const originCheck = canVesselBerth(vesselSpec, origin);
    const destCheck = canVesselBerth(vesselSpec, dest);
    const feasible = originCheck.feasible && destCheck.feasible;

    // Calculate number of voyages needed
    const voyages = Math.ceil(cargoMT / vessel.dwtMax);
    const cargoPerVoyage = cargoMT / voyages;
    const utilization = cargoPerVoyage / vessel.dwtTypical;

    // Get route distance
    const distance = route ? route.distanceNM : 5000; // fallback

    // Transit time
    const transitDays = distance / (vessel.speed.laden * 24);

    // Port turnaround
    const loadTurnaround = estimateTurnaround(cargoPerVoyage, origin);
    const dischTurnaround = estimateTurnaround(cargoPerVoyage, dest);

    // Fuel cost
    const fuelData = calculateFuelCost(vessel, distance, fuelPrice);

    // Port charges
    const loadPortCost = origin.portCharges * cargoPerVoyage;
    const dischPortCost = dest.portCharges * cargoPerVoyage;

    // Estimated freight cost
    const estimatedRate = freightRate || estimateFreightRate(classId, distance);
    const freightCost = estimatedRate * cargoPerVoyage;

    // Total voyage duration
    const totalVoyageDays = transitDays + loadTurnaround.totalDays + dischTurnaround.totalDays;

    // Total cost per voyage
    const totalPerVoyage = freightCost + loadPortCost + dischPortCost;
    const costPerTon = totalPerVoyage / cargoPerVoyage;

    // Total for all voyages
    const totalCost = totalPerVoyage * voyages;
    const totalCostPerTon = totalCost / cargoMT;

    // Idle risk score (0-100, lower is better)
    const idleRisk = calculateIdleRisk(vessel, dest, transitDays);

    // Overall score (lower is better)
    const score = calculateOverallScore({
      feasible,
      costPerTon,
      utilization,
      voyages,
      idleRisk,
      transitDays,
    });

    // Determine if lighterage is needed at Sagar-Sandheads
    const needsLighterage = destId === 'HALDIA' && vessel.maxDraft.typical > dest.maxDraft;

    results.push({
      vesselClass: vessel,
      classId,
      feasible,
      originCheck,
      destCheck,
      voyages,
      cargoPerVoyage: Math.round(cargoPerVoyage),
      utilization: Math.round(utilization * 100) / 100,
      distance,
      transitDays: Math.round(transitDays * 10) / 10,
      totalVoyageDays: Math.round(totalVoyageDays * 10) / 10,
      loadTurnaround,
      dischTurnaround,
      fuelData,
      loadPortCost: Math.round(loadPortCost),
      dischPortCost: Math.round(dischPortCost),
      freightRate: estimatedRate,
      freightCost: Math.round(freightCost),
      totalPerVoyage: Math.round(totalPerVoyage),
      costPerTon: Math.round(costPerTon * 100) / 100,
      totalCost: Math.round(totalCost),
      totalCostPerTon: Math.round(totalCostPerTon * 100) / 100,
      idleRisk,
      score,
      needsLighterage,
      lighterageNote: needsLighterage ? 'Vessel exceeds Haldia draft. Lighterage at Sagar-Sandheads required.' : null,
    });
  }

  // Sort by score (best first), feasible options always first
  return results.sort((a, b) => {
    if (a.feasible && !b.feasible) return -1;
    if (!a.feasible && b.feasible) return 1;
    return a.score - b.score;
  });
}


/**
 * Estimate freight rate based on vessel class and distance
 */
function estimateFreightRate(classId, distance) {
  const basePer1000NM = {
    HANDYSIZE: 3.5,
    SUPRAMAX: 2.8,
    PANAMAX: 2.2,
    CAPESIZE: 1.6,
  };
  return Math.round((basePer1000NM[classId] || 2.5) * (distance / 1000) * 100) / 100;
}


/**
 * Calculate idle risk score (0-100)
 */
function calculateIdleRisk(vessel, port, transitDays) {
  let risk = 0;

  // Port congestion risk
  risk += port.avgCongestionDays * 8;

  // Tidal dependency
  if (port.tidalDependent) risk += 15;

  // Seasonal risks (check current month)
  const currentMonth = new Date().getMonth() + 1;
  for (const [_, riskData] of Object.entries(port.seasonalRisks)) {
    if (riskData.months.includes(currentMonth)) {
      const impactScores = { low: 5, moderate: 12, high: 25, very_high: 35 };
      risk += impactScores[riskData.impact] || 10;
    }
  }

  // Long transit = more exposure to market changes
  if (transitDays > 25) risk += 10;

  // No cranes at port and vessel is gearless
  if (!vessel.hasCranes && !port.berthCount) risk += 10;

  return Math.min(100, Math.round(risk));
}


/**
 * Calculate overall optimization score (lower = better)
 */
function calculateOverallScore(params) {
  const { feasible, costPerTon, utilization, voyages, idleRisk, transitDays } = params;

  if (!feasible) return 9999;

  // Weighted scoring
  let score = 0;
  score += costPerTon * 3;          // Cost is most important
  score += (1 - utilization) * 10;  // Penalize underutilization
  score += (voyages - 1) * 5;      // Penalize multi-voyage
  score += idleRisk * 0.2;         // Idle risk
  score += transitDays * 0.3;      // Transit time

  return Math.round(score * 100) / 100;
}


/**
 * Compare contract strategies: Spot vs Short-term vs Mid-term
 */
export function compareContracts(currentRateMT, forecastData, cargoMT, voyagesPerYear = 10, tcToMT = 0.0003) {
  const { forecast, trend } = forecastData;
  
  // Averages in TC ($/day)
  const avgForecast30_TC = forecast.values.slice(0, 30).reduce((a, b) => a + b, 0) / 30;
  const avgForecast90_TC = forecast.values.reduce((a, b) => a + b, 0) / forecast.values.length;

  // Convert to $/MT
  const avgForecast30 = avgForecast30_TC * tcToMT;
  const avgForecast90 = avgForecast90_TC * tcToMT;

  // Spot: pay current rate each voyage
  const spotCost = currentRateMT * cargoMT * voyagesPerYear;

  // Short-term COA (3 months, 3 voyages): lock in slightly below forecast average
  const shortTermRate = avgForecast30 * 0.97; // 3% COA discount
  const shortTermVoyages = 3;
  const shortTermCost = shortTermRate * cargoMT * shortTermVoyages;
  const shortTermAnnual = (shortTermCost / shortTermVoyages) * voyagesPerYear;

  // Mid-term COA (12 months, 10 voyages): bigger discount on longer commitment
  const midTermRate = avgForecast90 * 0.93; // 7% COA discount
  const midTermCost = midTermRate * cargoMT * voyagesPerYear;

  // Determine recommendation
  let recommendation;
  if (trend.direction === 'rising' && trend.magnitude > 3) {
    recommendation = 'MID_TERM';
  } else if (trend.direction === 'falling' && trend.magnitude < -3) {
    recommendation = 'SPOT';
  } else {
    recommendation = 'SHORT_TERM';
  }

  const savings = {
    shortTerm: Math.round(spotCost - shortTermAnnual),
    midTerm: Math.round(spotCost - midTermCost),
    shortTermPct: Math.round(((spotCost - shortTermAnnual) / spotCost) * 10000) / 100,
    midTermPct: Math.round(((spotCost - midTermCost) / spotCost) * 10000) / 100,
  };

  return {
    spot: {
      type: 'Spot',
      rate: currentRateMT,
      annualCost: Math.round(spotCost),
      voyages: voyagesPerYear,
      flexibility: 'Maximum',
      riskExposure: 'High — fully exposed to market volatility',
    },
    shortTerm: {
      type: 'Short-Term COA (3 months)',
      rate: Math.round(shortTermRate * 100) / 100,
      annualCost: Math.round(shortTermAnnual),
      voyages: shortTermVoyages,
      flexibility: 'Moderate',
      riskExposure: 'Medium — partial hedge against rate spikes',
      discount: '~3% vs spot',
    },
    midTerm: {
      type: 'Mid-Term COA (12 months)',
      rate: Math.round(midTermRate * 100) / 100,
      annualCost: Math.round(midTermCost),
      voyages: voyagesPerYear,
      flexibility: 'Limited',
      riskExposure: 'Low — locked rate for full year',
      discount: '~7% vs spot',
    },
    recommendation,
    savings,
    rationale: getContractRationale(recommendation, trend, savings),
  };
}

function getContractRationale(rec, trend, savings) {
  switch (rec) {
    case 'MID_TERM':
      return `Market is in an upward trend (+${trend.magnitude}% over 30 days). Locking in a mid-term COA now could save up to $${savings.midTerm.toLocaleString()} annually (${savings.midTermPct}% reduction). Recommended to secure rates before further increases.`;
    case 'SPOT':
      return `Market is declining (${trend.magnitude}% over 30 days). Spot chartering allows you to benefit from falling rates. Avoid locking into long-term contracts at current levels.`;
    case 'SHORT_TERM':
      return `Market is relatively stable. A short-term COA provides a balance between rate certainty and flexibility, with potential savings of $${savings.shortTerm.toLocaleString()} annually (${savings.shortTermPct}% reduction).`;
    default:
      return '';
  }
}
