/**
 * FreightForecast Pro — Risk Analyzer
 * Volatility analysis, risk scoring, market entry signals,
 * and early warning system.
 */

// ================================================================
//  VOLATILITY ANALYSIS
// ================================================================

/**
 * Calculate rolling volatility (standard deviation) for given windows.
 */
export function rollingVolatility(rates, windows = [7, 30, 90]) {
  const result = {};

  for (const w of windows) {
    const vol = [];
    for (let i = 0; i < rates.length; i++) {
      if (i < w - 1) {
        vol.push(null);
        continue;
      }
      const slice = rates.slice(i - w + 1, i + 1);
      vol.push(Math.round(stddev(slice)));
    }
    result[`vol${w}d`] = vol;
  }

  return result;
}

/**
 * Calculate historical percentile rank for current rate.
 * @returns {number} 0-100 percentile
 */
export function ratePercentile(currentRate, historicalRates) {
  const sorted = [...historicalRates].sort((a, b) => a - b);
  const below = sorted.filter(r => r < currentRate).length;
  return Math.round((below / sorted.length) * 100);
}


// ================================================================
//  MARKET ENTRY SCORING
// ================================================================

/**
 * Calculate Market Entry Score (0-100).
 * Higher score = better time to enter (lock in a charter).
 * Based on: percentile position, trend direction, volatility, seasonality.
 */
export function marketEntryScore(rateData, forecastData) {
  const rates = rateData.map(r => r.rate);
  const currentRate = rates[rates.length - 1];

  // 1. Percentile Score (0-40 points)
  // Lower percentile = lower rate = better entry
  const percentile = ratePercentile(currentRate, rates);
  const percentileScore = Math.round((100 - percentile) * 0.4);

  // 2. Trend Score (0-25 points)
  // Falling trend = rates going down = might be good to wait
  // Rising trend = rates going up = enter now before it gets worse
  const recent30 = rates.slice(-30);
  const recent7 = rates.slice(-7);
  const trend30 = ((recent30[recent30.length - 1] - recent30[0]) / recent30[0]) * 100;
  const trend7 = ((recent7[recent7.length - 1] - recent7[0]) / recent7[0]) * 100;

  let trendScore;
  if (trend30 < -5) trendScore = 5;       // Strongly falling — wait
  else if (trend30 < -2) trendScore = 10;  // Falling — consider waiting
  else if (trend30 < 2) trendScore = 20;   // Stable — decent entry
  else if (trend30 < 5) trendScore = 22;   // Rising — enter soon
  else trendScore = 25;                     // Strongly rising — enter now

  // 3. Volatility Score (0-20 points)
  // Low volatility = stable market = safer entry
  const vol30 = stddev(recent30);
  const avgRate = mean(recent30);
  const cv = vol30 / avgRate; // Coefficient of variation

  let volScore;
  if (cv < 0.03) volScore = 20;     // Very stable
  else if (cv < 0.06) volScore = 15; // Moderate
  else if (cv < 0.10) volScore = 10; // Volatile
  else volScore = 5;                  // Very volatile

  // 4. Forecast Score (0-15 points)
  // If forecast shows rates will rise, enter now
  let forecastScore = 10;
  if (forecastData && forecastData.forecast) {
    const forecastAvg = mean(forecastData.forecast.values.slice(0, 30));
    const forecastDiff = ((forecastAvg - currentRate) / currentRate) * 100;

    if (forecastDiff > 5) forecastScore = 15;      // Forecast rising — enter
    else if (forecastDiff > 0) forecastScore = 12;
    else if (forecastDiff > -3) forecastScore = 8;
    else forecastScore = 3;                         // Forecast falling — wait
  }

  const total = percentileScore + trendScore + volScore + forecastScore;

  // Determine recommendation
  let recommendation, color;
  if (total >= 75) { recommendation = 'STRONG BUY'; color = 'success'; }
  else if (total >= 55) { recommendation = 'BUY'; color = 'success'; }
  else if (total >= 40) { recommendation = 'HOLD'; color = 'warning'; }
  else if (total >= 25) { recommendation = 'WAIT'; color = 'danger'; }
  else { recommendation = 'STRONG WAIT'; color = 'danger'; }

  return {
    score: total,
    recommendation,
    color,
    breakdown: {
      percentile: { score: percentileScore, max: 40, detail: `Rate at ${percentile}th percentile` },
      trend: { score: trendScore, max: 25, detail: `30d trend: ${trend30 > 0 ? '+' : ''}${Math.round(trend30 * 100) / 100}%` },
      volatility: { score: volScore, max: 20, detail: `CV: ${Math.round(cv * 10000) / 100}%` },
      forecast: { score: forecastScore, max: 15, detail: forecastData ? 'Based on 30d forecast' : 'No forecast data' },
    },
  };
}


// ================================================================
//  RISK ALERTS
// ================================================================

/**
 * Generate risk alerts based on current market conditions.
 */
export function generateRiskAlerts(rateData, forecastData, portId) {
  const alerts = [];
  const rates = rateData.map(r => r.rate);
  const currentRate = rates[rates.length - 1];
  const currentMonth = new Date().getMonth() + 1;

  // 1. Rate spike alert
  const avg30 = mean(rates.slice(-30));
  const rateDiff = ((currentRate - avg30) / avg30) * 100;

  if (rateDiff > 10) {
    alerts.push({
      id: 'rate_spike',
      type: 'danger',
      icon: '📈',
      title: 'Rate Spike Detected',
      message: `Current rate is ${Math.round(rateDiff)}% above 30-day average. Consider delaying non-urgent charters.`,
      priority: 1,
    });
  } else if (rateDiff < -10) {
    alerts.push({
      id: 'rate_dip',
      type: 'success',
      icon: '📉',
      title: 'Rate Dip — Opportunity',
      message: `Current rate is ${Math.abs(Math.round(rateDiff))}% below 30-day average. Consider locking in rates.`,
      priority: 2,
    });
  }

  // 2. High volatility alert
  const vol7 = stddev(rates.slice(-7));
  const vol30 = stddev(rates.slice(-30));
  if (vol7 > vol30 * 1.5) {
    alerts.push({
      id: 'high_volatility',
      type: 'warning',
      icon: '⚡',
      title: 'Elevated Market Volatility',
      message: '7-day volatility significantly exceeds 30-day average. Exercise caution with spot bookings.',
      priority: 2,
    });
  }

  // 3. Seasonal risk alerts
  const seasonalAlerts = getSeasonalAlerts(currentMonth);
  alerts.push(...seasonalAlerts);

  // 4. Trend reversal alert
  const trend7 = rates[rates.length - 1] - rates[rates.length - 8];
  const trend30 = rates[rates.length - 1] - rates[rates.length - 31];
  if ((trend7 > 0 && trend30 < 0) || (trend7 < 0 && trend30 > 0)) {
    alerts.push({
      id: 'trend_reversal',
      type: 'info',
      icon: '🔄',
      title: 'Potential Trend Reversal',
      message: 'Short-term trend diverges from 30-day trend. Market direction may be shifting.',
      priority: 3,
    });
  }

  // 5. Forecast divergence
  if (forecastData && forecastData.forecast) {
    const forecast7 = mean(forecastData.forecast.values.slice(0, 7));
    const forecastDiff = ((forecast7 - currentRate) / currentRate) * 100;
    if (Math.abs(forecastDiff) > 8) {
      alerts.push({
        id: 'forecast_divergence',
        type: forecastDiff > 0 ? 'warning' : 'info',
        icon: '🔮',
        title: forecastDiff > 0 ? 'Rates Expected to Rise' : 'Rates Expected to Fall',
        message: `7-day forecast suggests a ${Math.abs(Math.round(forecastDiff))}% ${forecastDiff > 0 ? 'increase' : 'decrease'} from current levels.`,
        priority: 2,
      });
    }
  }

  return alerts.sort((a, b) => a.priority - b.priority);
}

/**
 * Get seasonal alerts based on current month
 */
function getSeasonalAlerts(month) {
  const alerts = [];

  // Monsoon season (Jun-Sep)
  if (month >= 5 && month <= 9) {
    if (month === 5) {
      alerts.push({
        id: 'monsoon_approaching',
        type: 'warning',
        icon: '🌧️',
        title: 'Monsoon Season Approaching',
        message: 'SW Monsoon expected Jun-Sep. Plan for 1-5 day delays at Indian East Coast ports.',
        priority: 2,
      });
    } else {
      alerts.push({
        id: 'monsoon_active',
        type: 'danger',
        icon: '🌊',
        title: 'Monsoon Season Active',
        message: 'Increased port delays and weather disruptions. Factor additional buffer time into chartering plans.',
        priority: 1,
      });
    }
  }

  // Cyclone season (Oct-Dec)
  if (month >= 10 || month <= 1) {
    alerts.push({
      id: 'cyclone_season',
      type: 'warning',
      icon: '🌀',
      title: 'Cyclone Season — Bay of Bengal',
      message: 'October–December is peak cyclone season. Monitor weather advisories for East Coast India ports.',
      priority: 2,
    });
  }

  // Chinese New Year (late Jan/Feb)
  if (month === 1 || month === 2) {
    alerts.push({
      id: 'cny_demand',
      type: 'info',
      icon: '🏮',
      title: 'Chinese New Year Period',
      message: 'Reduced demand from Chinese buyers may lead to temporary rate softening. Potential chartering opportunity.',
      priority: 3,
    });
  }

  // Australian cyclone season
  if (month >= 11 || month <= 3) {
    alerts.push({
      id: 'au_cyclone',
      type: 'info',
      icon: '🌴',
      title: 'Australian Cyclone Season',
      message: 'Queensland coal ports (Hay Point, DBCT) may face weather disruptions Nov–Mar.',
      priority: 3,
    });
  }

  return alerts;
}


// ================================================================
//  IDLE SCENARIO ANALYSIS
// ================================================================

/**
 * Analyze idle risk and suggest mitigation strategies.
 */
export function analyzeIdleScenarios(vesselClass, origin, dest, forecastData) {
  const scenarios = [];
  const currentMonth = new Date().getMonth() + 1;

  // Low demand periods
  const lowDemandMonths = [1, 2, 7, 8]; // CNY + monsoon
  const isLowDemand = lowDemandMonths.includes(currentMonth);

  if (isLowDemand) {
    scenarios.push({
      type: 'low_demand',
      severity: 'medium',
      title: 'Low Demand Period',
      description: 'Current month historically shows lower cargo demand. Higher risk of vessel idle time.',
      mitigation: [
        'Consider triangulation routes (e.g., backhaul from Indian port to China with iron ore)',
        'Explore spot cargo aggregation to fill partial loads',
        'Pre-negotiate COA with multiple charterers for split cargoes',
      ],
    });
  }

  // Port congestion scenario
  if (dest && dest.avgCongestionDays > 2) {
    scenarios.push({
      type: 'port_congestion',
      severity: 'high',
      title: 'Discharge Port Congestion Risk',
      description: `${dest.name} averages ${dest.avgCongestionDays} days congestion. Vessel may be idle at anchorage.`,
      mitigation: [
        'Negotiate NOR (Notice of Readiness) terms to start laytime at anchorage',
        'Consider alternative discharge port with less congestion',
        `Pre-book berth slot at ${dest.name} in advance`,
      ],
    });
  }

  // Ballast positioning
  scenarios.push({
    type: 'ballast_positioning',
    severity: 'low',
    title: 'Ballast Voyage Optimization',
    description: 'After discharge, vessel will likely ballast to next load port.',
    mitigation: [
      'Explore backhaul cargo opportunities on return leg',
      'Position vessel at a port hub with multiple cargo options',
      'Consider India coastal movements for domestic coal redistribution',
    ],
  });

  // Seasonal weather delays
  for (const [riskType, riskData] of Object.entries(dest?.seasonalRisks || {})) {
    if (riskData.months.includes(currentMonth)) {
      scenarios.push({
        type: 'weather_delay',
        severity: riskData.impact === 'high' || riskData.impact === 'very_high' ? 'high' : 'medium',
        title: `${riskType.charAt(0).toUpperCase() + riskType.slice(1)} Weather Risk`,
        description: `${riskType} conditions may cause up to ${riskData.delayDays} days of additional idle time.`,
        mitigation: [
          'Build weather buffer into voyage schedule',
          'Include weather-related force majeure clauses in charter party',
          'Monitor weather forecasts and adjust ETA planning',
        ],
      });
    }
  }

  return scenarios;
}


// ================================================================
//  Statistical Helpers
// ================================================================

function mean(arr) {
  return arr.reduce((a, b) => a + b, 0) / arr.length;
}

function stddev(arr) {
  const m = mean(arr);
  const variance = arr.reduce((sum, val) => sum + (val - m) ** 2, 0) / arr.length;
  return Math.sqrt(variance);
}
