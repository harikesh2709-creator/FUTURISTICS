/**
 * FreightForecast Pro — Forecast Engine
 * Implements Triple Exponential Smoothing (Holt-Winters),
 * Weighted Moving Average, and Seasonal Decomposition
 * for freight rate time-series forecasting.
 */

// ================================================================
//  HOLT-WINTERS (Triple Exponential Smoothing)
// ================================================================

/**
 * Holt-Winters additive model.
 * @param {number[]} data       - Historical rate values
 * @param {number}   seasonLen  - Season length (e.g. 365 for daily annual)
 * @param {number}   forecastH  - Forecast horizon (number of periods)
 * @param {number}   alpha      - Level smoothing (0-1)
 * @param {number}   beta       - Trend smoothing (0-1)
 * @param {number}   gamma      - Seasonal smoothing (0-1)
 * @returns {{ fitted: number[], forecast: number[], level: number[], trend: number[], seasonal: number[] }}
 */
export function holtWinters(data, seasonLen = 30, forecastH = 90, alpha = 0.3, beta = 0.05, gamma = 0.15) {
  const n = data.length;
  if (n < seasonLen * 2) {
    // Fallback to simple exponential smoothing if not enough data for seasonal
    return simpleExponentialSmoothing(data, forecastH, alpha);
  }

  // Initialize level and trend using first two seasons
  let level = 0;
  for (let i = 0; i < seasonLen; i++) level += data[i];
  level /= seasonLen;

  let trend = 0;
  for (let i = 0; i < seasonLen; i++) {
    trend += (data[i + seasonLen] - data[i]) / seasonLen;
  }
  trend /= seasonLen;

  // Initialize seasonal components
  const seasonal = new Array(n + forecastH).fill(0);
  for (let i = 0; i < seasonLen; i++) {
    seasonal[i] = data[i] - level;
  }

  const fitted = new Array(n).fill(0);
  const levels = [level];
  const trends = [trend];

  // Fit the model
  for (let t = 0; t < n; t++) {
    const prevLevel = level;
    const prevTrend = trend;
    const sIdx = t % seasonLen;

    if (t >= seasonLen) {
      level = alpha * (data[t] - seasonal[t - seasonLen]) + (1 - alpha) * (prevLevel + prevTrend);
      trend = beta * (level - prevLevel) + (1 - beta) * prevTrend;
      seasonal[t] = gamma * (data[t] - level) + (1 - gamma) * seasonal[t - seasonLen];
    } else {
      level = alpha * (data[t] - seasonal[sIdx]) + (1 - alpha) * (prevLevel + prevTrend);
      trend = beta * (level - prevLevel) + (1 - beta) * prevTrend;
    }

    fitted[t] = level + trend + (t >= seasonLen ? seasonal[t - seasonLen] : seasonal[sIdx]);
    levels.push(level);
    trends.push(trend);
  }

  // Generate forecast
  const forecast = [];
  for (let h = 1; h <= forecastH; h++) {
    const sIdx = (n - seasonLen + ((h - 1) % seasonLen)) % seasonLen;
    const fval = level + trend * h + seasonal[n - seasonLen + ((h - 1) % seasonLen)] || 0;
    forecast.push(Math.max(0, Math.round(fval)));
  }

  return { fitted, forecast, level: levels, trend: trends, seasonal };
}


/**
 * Simple Exponential Smoothing fallback
 */
function simpleExponentialSmoothing(data, forecastH, alpha = 0.3) {
  const n = data.length;
  const fitted = [data[0]];

  for (let t = 1; t < n; t++) {
    fitted.push(alpha * data[t] + (1 - alpha) * fitted[t - 1]);
  }

  const lastValue = fitted[n - 1];
  const forecast = new Array(forecastH).fill(Math.round(lastValue));

  return { fitted, forecast, level: [], trend: [], seasonal: [] };
}


// ================================================================
//  WEIGHTED MOVING AVERAGE
// ================================================================

/**
 * Weighted Moving Average with configurable window.
 * More recent observations get higher weights.
 */
export function weightedMovingAverage(data, window = 14) {
  const n = data.length;
  const wma = [];

  for (let i = 0; i < n; i++) {
    if (i < window - 1) {
      wma.push(data[i]);
      continue;
    }

    let weightSum = 0;
    let valueSum = 0;
    for (let j = 0; j < window; j++) {
      const weight = j + 1; // Linear weights: 1, 2, 3, ..., window
      valueSum += data[i - window + 1 + j] * weight;
      weightSum += weight;
    }
    wma.push(Math.round(valueSum / weightSum));
  }

  return wma;
}

/**
 * Simple Moving Average
 */
export function simpleMovingAverage(data, window = 7) {
  const sma = [];
  for (let i = 0; i < data.length; i++) {
    if (i < window - 1) {
      sma.push(data[i]);
      continue;
    }
    let sum = 0;
    for (let j = 0; j < window; j++) sum += data[i - j];
    sma.push(Math.round(sum / window));
  }
  return sma;
}


// ================================================================
//  CONFIDENCE INTERVALS
// ================================================================

/**
 * Calculate prediction intervals based on historical forecast errors.
 * @param {number[]} forecast  - Point forecast values
 * @param {number[]} residuals - Historical residuals (actual - fitted)
 * @param {number}   ci80      - Z-score for 80% CI (1.28)
 * @param {number}   ci95      - Z-score for 95% CI (1.96)
 */
export function calculateConfidenceIntervals(forecast, residuals, ci80 = 1.28, ci95 = 1.96) {
  const stddev = standardDeviation(residuals);

  return forecast.map((val, h) => {
    // Widen bands as horizon increases
    const horizonFactor = 1 + (h * 0.008); // 0.8% widening per period
    const adjustedStd = stddev * horizonFactor;

    return {
      point: val,
      upper95: Math.round(val + ci95 * adjustedStd),
      lower95: Math.round(Math.max(0, val - ci95 * adjustedStd)),
      upper80: Math.round(val + ci80 * adjustedStd),
      lower80: Math.round(Math.max(0, val - ci80 * adjustedStd)),
    };
  });
}

/**
 * Calculate residuals between actual and fitted values
 */
export function calculateResiduals(actual, fitted) {
  const minLen = Math.min(actual.length, fitted.length);
  const residuals = [];
  for (let i = 0; i < minLen; i++) {
    residuals.push(actual[i] - fitted[i]);
  }
  return residuals;
}


// ================================================================
//  SEASONAL DECOMPOSITION
// ================================================================

/**
 * Decompose time series into trend, seasonal, and residual components.
 * Uses classical additive decomposition.
 */
export function seasonalDecomposition(data, seasonLen = 30) {
  const n = data.length;

  // 1. Trend: centered moving average
  const trend = centeredMovingAverage(data, seasonLen);

  // 2. Detrended: subtract trend
  const detrended = data.map((val, i) => trend[i] !== null ? val - trend[i] : 0);

  // 3. Seasonal: average detrended values for each position in season
  const seasonalAvg = new Array(seasonLen).fill(0);
  const seasonalCount = new Array(seasonLen).fill(0);

  for (let i = 0; i < n; i++) {
    if (trend[i] !== null) {
      const sIdx = i % seasonLen;
      seasonalAvg[sIdx] += detrended[i];
      seasonalCount[sIdx]++;
    }
  }

  for (let i = 0; i < seasonLen; i++) {
    seasonalAvg[i] = seasonalCount[i] > 0 ? seasonalAvg[i] / seasonalCount[i] : 0;
  }

  const seasonal = data.map((_, i) => Math.round(seasonalAvg[i % seasonLen]));

  // 4. Residual
  const residual = data.map((val, i) =>
    trend[i] !== null ? Math.round(val - trend[i] - seasonal[i]) : 0
  );

  return { trend, seasonal, residual };
}

function centeredMovingAverage(data, window) {
  const halfWin = Math.floor(window / 2);
  const result = new Array(data.length).fill(null);

  for (let i = halfWin; i < data.length - halfWin; i++) {
    let sum = 0;
    for (let j = -halfWin; j <= halfWin; j++) sum += data[i + j];
    result[i] = Math.round(sum / (window + 1));
  }

  return result;
}


// ================================================================
//  FORECAST ACCURACY METRICS
// ================================================================

/**
 * Mean Absolute Percentage Error
 */
export function mape(actual, predicted) {
  let sum = 0;
  let count = 0;
  for (let i = 0; i < actual.length; i++) {
    if (actual[i] !== 0) {
      sum += Math.abs((actual[i] - predicted[i]) / actual[i]);
      count++;
    }
  }
  return count > 0 ? (sum / count) * 100 : 0;
}

/**
 * Root Mean Square Error
 */
export function rmse(actual, predicted) {
  let sum = 0;
  for (let i = 0; i < actual.length; i++) {
    sum += (actual[i] - predicted[i]) ** 2;
  }
  return Math.sqrt(sum / actual.length);
}

/**
 * Mean Absolute Error
 */
export function mae(actual, predicted) {
  let sum = 0;
  for (let i = 0; i < actual.length; i++) {
    sum += Math.abs(actual[i] - predicted[i]);
  }
  return sum / actual.length;
}


// ================================================================
//  FULL FORECAST PIPELINE
// ================================================================

/**
 * Run the complete forecast pipeline for a vessel class.
 * @param {Array<{rate: number}>} rateData - Historical rate data
 * @param {number} forecastDays - Number of days to forecast
 * @returns {Object} Full forecast results with confidence intervals
 */
export function runForecast(rateData, forecastDays = 90) {
  const rates = rateData.map(r => r.rate);
  const dates = rateData.map(r => r.date);

  // Run Holt-Winters
  const hw = holtWinters(rates, 30, forecastDays, 0.3, 0.05, 0.15);

  // Calculate residuals and accuracy
  const residuals = calculateResiduals(rates, hw.fitted);
  const accuracy = {
    mape: Math.round(mape(rates.slice(30), hw.fitted.slice(30)) * 100) / 100,
    rmse: Math.round(rmse(rates.slice(30), hw.fitted.slice(30))),
    mae: Math.round(mae(rates.slice(30), hw.fitted.slice(30))),
  };

  // Confidence intervals for forecast
  const intervals = calculateConfidenceIntervals(hw.forecast, residuals);

  // WMA overlays
  const wma7 = weightedMovingAverage(rates, 7);
  const wma14 = weightedMovingAverage(rates, 14);
  const wma30 = weightedMovingAverage(rates, 30);

  // Seasonal decomposition
  const decomp = seasonalDecomposition(rates, 30);

  // Generate forecast dates
  const lastDate = new Date(dates[dates.length - 1]);
  const forecastDates = [];
  for (let i = 1; i <= forecastDays; i++) {
    const d = new Date(lastDate);
    d.setDate(d.getDate() + i);
    forecastDates.push(d.toISOString().split('T')[0]);
  }

  // Trend direction
  const recentRates = rates.slice(-30);
  const trendDirection = recentRates[recentRates.length - 1] > recentRates[0] ? 'rising' : 'falling';
  const trendMagnitude = ((recentRates[recentRates.length - 1] - recentRates[0]) / recentRates[0]) * 100;

  return {
    historical: { dates, rates, fitted: hw.fitted, wma7, wma14, wma30 },
    forecast: { dates: forecastDates, values: hw.forecast, intervals },
    decomposition: decomp,
    accuracy,
    trend: {
      direction: trendDirection,
      magnitude: Math.round(trendMagnitude * 100) / 100,
      currentRate: rates[rates.length - 1],
      avgRate30d: Math.round(recentRates.reduce((a, b) => a + b, 0) / recentRates.length),
    },
  };
}


// ================================================================
//  Statistical Helpers
// ================================================================

function standardDeviation(arr) {
  const n = arr.length;
  if (n === 0) return 0;
  const mean = arr.reduce((a, b) => a + b, 0) / n;
  const variance = arr.reduce((sum, val) => sum + (val - mean) ** 2, 0) / n;
  return Math.sqrt(variance);
}
