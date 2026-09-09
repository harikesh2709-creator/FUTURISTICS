/**
 * FreightForecast Pro — Vessel Database
 * Specifications for bulk carrier vessel classes.
 */

export const VESSEL_CLASSES = {
  HANDYSIZE: {
    id: 'HANDYSIZE',
    name: 'Handysize',
    dwtMin: 15000,
    dwtMax: 35000,
    dwtTypical: 28000,
    loa: { min: 150, max: 180, typical: 170 },
    beam: { min: 25, max: 28, typical: 27 },
    maxDraft: { min: 9.5, max: 10.5, typical: 10.0 },
    speed: { laden: 13, ballast: 14 },
    fuelConsumption: { laden: 28, ballast: 24, port: 4 },  // MT/day
    dailyCost: { low: 8000, mid: 10000, high: 12000 },     // USD/day
    hasCranes: true,
    canalTransit: { panama: true, suez: true },
    color: '#22c55e',  // Chart color
    description: 'Most versatile. Self-geared — can operate at ports without cargo-handling infrastructure.',
    idealFor: 'Small parcels, draft-restricted ports (Haldia, Beira), flexibility',
    cargoCapacity: '15,000 – 35,000 MT',
  },

  SUPRAMAX: {
    id: 'SUPRAMAX',
    name: 'Supramax',
    dwtMin: 50000,
    dwtMax: 65000,
    dwtTypical: 58000,
    loa: { min: 180, max: 200, typical: 190 },
    beam: { min: 29, max: 32, typical: 31 },
    maxDraft: { min: 11.5, max: 13.0, typical: 12.5 },
    speed: { laden: 13.5, ballast: 14.5 },
    fuelConsumption: { laden: 33, ballast: 28, port: 5 },
    dailyCost: { low: 12000, mid: 15000, high: 18000 },
    hasCranes: true,
    canalTransit: { panama: true, suez: true },
    color: '#38bdf8',
    description: 'Geared workhorses. Good balance of size and port accessibility.',
    idealFor: 'Medium parcels, moderate-draft ports, Beira, Vanino',
    cargoCapacity: '50,000 – 65,000 MT',
  },

  PANAMAX: {
    id: 'PANAMAX',
    name: 'Panamax',
    dwtMin: 65000,
    dwtMax: 85000,
    dwtTypical: 75000,
    loa: { min: 220, max: 230, typical: 225 },
    beam: { min: 32, max: 33, typical: 32.3 },
    maxDraft: { min: 13.0, max: 14.5, typical: 14.0 },
    speed: { laden: 13.5, ballast: 14.5 },
    fuelConsumption: { laden: 38, ballast: 32, port: 5 },
    dailyCost: { low: 14000, mid: 18000, high: 22000 },
    hasCranes: false,
    canalTransit: { panama: true, suez: true },
    color: '#f59e0b',
    description: 'Originally sized for old Panama Canal locks. Primary coal/grain workhorses.',
    idealFor: 'Major trade routes, Australia-India coal, cost-effective for 65k-85k parcels',
    cargoCapacity: '65,000 – 85,000 MT',
  },

  CAPESIZE: {
    id: 'CAPESIZE',
    name: 'Capesize',
    dwtMin: 120000,
    dwtMax: 200000,
    dwtTypical: 170000,
    loa: { min: 260, max: 300, typical: 285 },
    beam: { min: 40, max: 50, typical: 45 },
    maxDraft: { min: 16.0, max: 18.5, typical: 17.2 },
    speed: { laden: 14, ballast: 15 },
    fuelConsumption: { laden: 52, ballast: 42, port: 6 },
    dailyCost: { low: 18000, mid: 26000, high: 35000 },
    hasCranes: false,
    canalTransit: { panama: false, suez: true },
    color: '#a855f7',
    description: 'Too large for Panama Canal — transit via Cape. Lowest cost-per-ton for large volumes.',
    idealFor: 'Large coal shipments (120k+ MT) to deep ports: Dhamra, Gangavaram, Paradip',
    cargoCapacity: '120,000 – 200,000 MT',
  },
};


// ================================================================
//  Utility Functions
// ================================================================

/**
 * Get all vessel classes as an array
 */
export function getVesselClasses() {
  return Object.values(VESSEL_CLASSES);
}

/**
 * Get a vessel class by ID
 */
export function getVesselClass(id) {
  return VESSEL_CLASSES[id] || null;
}

/**
 * Recommend vessel class(es) for a given cargo volume
 */
export function recommendVesselForCargo(cargoMT) {
  const classes = getVesselClasses();
  const recommendations = [];

  for (const vc of classes) {
    if (cargoMT <= vc.dwtMax) {
      const utilization = cargoMT / vc.dwtMax;
      const loadFactor = cargoMT / vc.dwtTypical;
      recommendations.push({
        vessel: vc,
        utilization: Math.min(utilization, 1),
        loadFactor: Math.min(loadFactor, 1),
        underloaded: utilization < 0.6,
        overloaded: cargoMT > vc.dwtMax,
        voyages: 1,
      });
    }
    // Also consider multi-voyage splitting
    if (cargoMT > vc.dwtMax) {
      const voyages = Math.ceil(cargoMT / vc.dwtTypical);
      const perVoyage = cargoMT / voyages;
      if (perVoyage >= vc.dwtMin && perVoyage <= vc.dwtMax) {
        recommendations.push({
          vessel: vc,
          utilization: perVoyage / vc.dwtMax,
          loadFactor: perVoyage / vc.dwtTypical,
          underloaded: false,
          overloaded: false,
          voyages,
          splitCargo: perVoyage,
        });
      }
    }
  }

  return recommendations.sort((a, b) => {
    // Prefer single voyage, then highest utilization
    if (a.voyages !== b.voyages) return a.voyages - b.voyages;
    return b.utilization - a.utilization;
  });
}

/**
 * Calculate estimated fuel cost for a voyage
 */
export function calculateFuelCost(vesselClass, distanceNM, fuelPrice = 550) {
  const ladenDays = distanceNM / (vesselClass.speed.laden * 24);
  const fuelMT = ladenDays * vesselClass.fuelConsumption.laden;
  return {
    transitDays: Math.round(ladenDays * 10) / 10,
    fuelMT: Math.round(fuelMT),
    fuelCost: Math.round(fuelMT * fuelPrice),
  };
}

/**
 * Calculate total voyage cost estimate
 */
export function estimateVoyageCost(vesselClass, cargoMT, distanceNM, freightRate, portChargesLoad, portChargesDisch) {
  const fuel = calculateFuelCost(vesselClass, distanceNM);
  const freightCost = freightRate * cargoMT;
  const loadPortCharges = portChargesLoad * cargoMT;
  const dischPortCharges = portChargesDisch * cargoMT;
  const totalDays = fuel.transitDays + 5; // 5 days port time approx
  const hireCost = vesselClass.dailyCost.mid * totalDays;

  return {
    freightCost,
    fuelCost: fuel.fuelCost,
    loadPortCharges,
    dischPortCharges,
    hireCost,
    totalCost: freightCost + loadPortCharges + dischPortCharges,
    costPerTon: Math.round((freightCost + loadPortCharges + dischPortCharges) / cargoMT * 100) / 100,
    transitDays: fuel.transitDays,
  };
}
