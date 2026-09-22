"""
Blind Interleaver Detector — Estimates interleaver type and parameters
(depth, span) from received bitstream using autocorrelation analysis
and rank-matrix methods.
"""

import numpy as np


def detect_interleaver_params(
    bits: np.ndarray,
    max_depth: int = 64,
    max_span: int = 64,
) -> dict:
    """
    Attempt to blindly detect interleaving parameters by analyzing
    bit-level autocorrelation periodicity.

    For block interleavers: periodic peaks in autocorrelation at
    multiples of the interleaver depth.

    Returns dict:
        detected     : bool — whether interleaving was detected
        type_guess   : str — "block", "convolutional", or "none"
        depth        : int — estimated interleaver depth
        span         : int — estimated interleaver span (columns)
        confidence   : float — detection confidence 0..1
        acf_peaks    : list of (lag, correlation) peak pairs
    """
    if len(bits) < 200:
        return {
            "detected": False, "type_guess": "none",
            "depth": 0, "span": 0, "confidence": 0,
            "acf_peaks": [],
        }

    # Convert to ±1 for correlation
    x = bits.astype(np.float64) * 2 - 1
    N = min(len(x), 10000)
    x = x[:N]

    # Compute normalized autocorrelation
    max_lag = min(max_depth * max_span, N // 2)
    acf = np.zeros(max_lag)
    x_norm = x - np.mean(x)
    var = np.var(x_norm)
    if var < 1e-12:
        return {
            "detected": False, "type_guess": "none",
            "depth": 0, "span": 0, "confidence": 0,
            "acf_peaks": [],
        }

    for lag in range(1, max_lag):
        acf[lag] = np.mean(x_norm[:N - lag] * x_norm[lag:N]) / var

    # Find peaks in autocorrelation
    peaks = []
    threshold = 0.05  # Minimum correlation to consider a peak
    for i in range(2, len(acf) - 1):
        if acf[i] > acf[i - 1] and acf[i] > acf[i + 1] and acf[i] > threshold:
            peaks.append((i, float(acf[i])))

    if not peaks:
        return {
            "detected": False, "type_guess": "none",
            "depth": 0, "span": 0, "confidence": 0,
            "acf_peaks": [],
        }

    # Sort by correlation strength
    peaks.sort(key=lambda p: p[1], reverse=True)

    # Check for periodic peaks (indicates block interleaving)
    if len(peaks) >= 2:
        primary_lag = peaks[0][0]
        # Check if other peaks are at multiples
        harmonics = 0
        for lag, corr in peaks[1:]:
            ratio = lag / primary_lag
            if abs(ratio - round(ratio)) < 0.15 and round(ratio) > 0:
                harmonics += 1

        if harmonics >= 1:
            # Block interleaver detected
            depth = primary_lag
            # Estimate span from secondary peak spacing
            span = max_span  # Default
            if len(peaks) >= 3:
                diffs = [peaks[i + 1][0] - peaks[i][0] for i in range(min(5, len(peaks) - 1))]
                if diffs:
                    span = int(np.median(diffs))
                    if span < 2:
                        span = max_span

            confidence = min(0.95, peaks[0][1] * 2 + harmonics * 0.1)
            return {
                "detected": True,
                "type_guess": "block",
                "depth": depth,
                "span": span,
                "confidence": round(confidence, 3),
                "acf_peaks": peaks[:10],
            }

    # Check for linearly increasing delays (convolutional)
    lags = [p[0] for p in peaks[:8]]
    if len(lags) >= 3:
        diffs = np.diff(lags)
        if len(diffs) >= 2 and np.std(diffs) / (np.mean(diffs) + 1e-10) < 0.3:
            # Roughly evenly spaced → convolutional
            depth = int(np.mean(diffs))
            span = len(lags)
            confidence = min(0.85, peaks[0][1] * 1.5)
            return {
                "detected": True,
                "type_guess": "convolutional",
                "depth": depth,
                "span": span,
                "confidence": round(confidence, 3),
                "acf_peaks": peaks[:10],
            }

    # Weak or ambiguous detection
    return {
        "detected": True,
        "type_guess": "unknown",
        "depth": peaks[0][0],
        "span": 0,
        "confidence": round(peaks[0][1], 3),
        "acf_peaks": peaks[:10],
    }
