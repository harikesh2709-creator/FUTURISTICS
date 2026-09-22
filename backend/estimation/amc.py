"""
Automatic Modulation Classification (AMC) — Uses Higher-Order Cumulants
(C20, C21, C40, C41, C42) and spectral moment features to classify
modulation type among: BPSK, QPSK, 8-PSK, 16-QAM, 64-QAM, 2-FSK, 4-FSK.

Reference: A. Swami & B.M. Sadler, "Hierarchical Digital Modulation
Classification Using Cumulants," IEEE Trans. Comm., 2000.
"""

import numpy as np
from scipy.signal import welch


def compute_cumulants(samples: np.ndarray, max_samples: int = 100000) -> dict:
    """
    Compute normalized higher-order cumulants C20, C21, C40, C41, C42
    from complex baseband signal samples (unit-power normalized).
    """
    x = samples[:max_samples].copy()
    x = x - np.mean(x)
    power = np.mean(np.abs(x) ** 2)
    if power < 1e-12:
        return {"C20": 0, "C21": 0, "C40": 0, "C41": 0, "C42": 0}
    x = x / np.sqrt(power)

    # 2nd-order moments
    M20 = np.mean(x ** 2)           # E[x^2]
    M21 = np.mean(np.abs(x) ** 2)   # E[|x|^2] -> ~1

    # 4th-order moments
    M40 = np.mean(x ** 4)
    M41 = np.mean(x ** 3 * np.conj(x))
    M42 = np.mean(np.abs(x) ** 4)

    # 4th-order cumulants
    C20 = M20
    C21 = M21
    C40 = M40 - 3 * M20 ** 2
    C41 = M41 - 3 * M20 * M21
    C42 = M42 - np.abs(M20) ** 2 - 2 * M21 ** 2

    return {
        "C20": complex(C20),
        "C21": complex(C21),
        "C40": complex(C40),
        "C41": complex(C41),
        "C42": complex(C42),
    }


def _abs_c(val) -> float:
    if isinstance(val, complex):
        return float(abs(val))
    return abs(float(val))


def detect_fsk(
    samples: np.ndarray,
    sample_rate: float,
    max_samples: int = 50000,
) -> dict:
    """
    Detect genuine FSK modulation by analyzing discrete tone clustering.
    Requires high peak-to-noise ratio in instantaneous frequency histogram.
    """
    sig = samples[:max_samples]
    prod = sig[1:] * np.conj(sig[:-1])
    inst_freq = np.angle(prod) / (2 * np.pi) * sample_rate

    p5, p95 = np.percentile(inst_freq, [5, 95])
    mask = (inst_freq >= p5) & (inst_freq <= p95)
    freq_clean = inst_freq[mask]

    if len(freq_clean) < 500:
        return {"is_fsk": False, "fsk_order": 0, "freqs": []}

    n_bins = 128
    hist, edges = np.histogram(freq_clean, bins=n_bins)
    centers = (edges[:-1] + edges[1:]) / 2

    hist_smooth = np.convolve(hist, np.ones(5) / 5, mode="same")
    max_h = np.max(hist_smooth)
    med_h = np.median(hist_smooth) + 1e-6

    # Real FSK has very high peak-to-median ratio (> 8.0)
    if max_h / med_h < 8.0:
        return {"is_fsk": False, "fsk_order": 0, "freqs": []}

    peaks = []
    total_counts = np.sum(hist)
    for i in range(2, len(hist_smooth) - 2):
        if (hist_smooth[i] > hist_smooth[i - 1] and
            hist_smooth[i] > hist_smooth[i + 1] and
            hist_smooth[i] > max_h * 0.4):
            # Must have substantial mass (> 10% of samples)
            if hist_smooth[i] * 5 / total_counts > 0.10:
                peaks.append(centers[i])

    if len(peaks) >= 4:
        return {"is_fsk": True, "fsk_order": 4, "freqs": [float(f) for f in peaks[:4]]}
    elif len(peaks) == 2:
        return {"is_fsk": True, "fsk_order": 2, "freqs": [float(f) for f in peaks[:2]]}
    else:
        return {"is_fsk": False, "fsk_order": 0, "freqs": []}


# Theoretical cumulant signatures for unit-power constellations
_THEORETICAL_CUMS = {
    "BPSK":   {"C40": 2.0,  "C42": 2.0,  "C42_real": -2.0},
    "QPSK":   {"C40": 1.0,  "C42": 1.0,  "C42_real": -1.0},
    "8-PSK":  {"C40": 0.0,  "C42": 1.0,  "C42_real": -1.0},
    "16-QAM": {"C40": 0.68, "C42": 0.68, "C42_real": -0.68},
    "64-QAM": {"C40": 0.62, "C42": 0.62, "C42_real": -0.619},
}


def classify_modulation(
    samples: np.ndarray,
    sample_rate: float,
    max_samples: int = 100000,
) -> dict:
    """
    Automatically classify modulation of a complex baseband signal
    using carrier-corrected symbol-synchronous cumulants and FSK discriminator.
    """
    sig = samples[:max_samples]

    # Check for genuine FSK first
    fsk_info = detect_fsk(sig, sample_rate)
    if fsk_info["is_fsk"]:
        mod_type = f"{fsk_info['fsk_order']}-FSK"
        return {
            "modulation": mod_type,
            "confidence": 0.92,
            "cumulants": {},
            "fsk_info": fsk_info,
            "features": {"|C40|": 0.0, "|C42|": 0.0},
            "all_scores": {mod_type: 1.0, "QPSK": 0.0, "BPSK": 0.0, "16-QAM": 0.0},
        }

    # Step 2: Coarse frequency offset correction to prevent cumulant spinning
    # Raising to 4th power collapses PSK/QAM modulation
    raised = sig ** 4
    spec = np.abs(np.fft.fft(raised))
    freqs = np.fft.fftfreq(len(raised), d=1.0 / sample_rate)
    p_idx = np.argmax(spec)
    offset_hz = float(freqs[p_idx] / 4.0)
    n = np.arange(len(sig))
    corrected = sig * np.exp(-1j * 2 * np.pi * offset_hz * n / sample_rate)

    # Step 3: Symbol-synchronous extraction for cumulant evaluation
    mag_sq = np.abs(corrected) ** 2 - np.mean(np.abs(corrected) ** 2)
    s_spec = np.abs(np.fft.fft(mag_sq))
    s_freqs = np.fft.fftfreq(len(mag_sq), d=1.0 / sample_rate)
    pos_mask = (s_freqs > sample_rate * 0.005) & (s_freqs < sample_rate * 0.49)
    if np.any(pos_mask):
        c_f = s_freqs[pos_mask]
        c_s = s_spec[pos_mask]
        sr_est = abs(c_f[np.argmax(c_s)])
        sps = max(2, int(round(sample_rate / sr_est)))
    else:
        sps = 4

    # Subsample at optimal sampling phase
    best_phase = 0
    best_eng = -1
    for phi in range(sps):
        sub = corrected[phi::sps]
        eng = float(np.mean(np.abs(sub) ** 4))
        if eng > best_eng:
            best_eng = eng
            best_phase = phi

    syms = corrected[best_phase::sps]

    # Step 4: Costas tracking on symbols if needed to unspin constellation
    try:
        from sigint_pipeline.demod import costas_loop
        tracked = costas_loop(syms, order=4)
    except Exception:
        tracked = syms

    # Compute higher order cumulants on symbol stream
    cums = compute_cumulants(tracked)
    C40_abs = _abs_c(cums["C40"])
    C42_abs = _abs_c(cums["C42"])
    C42_real = float(cums["C42"].real)

    # Score distance against standard theoretical signatures
    scores = {}
    for mod_name, sig_vals in _THEORETICAL_CUMS.items():
        d = (
            abs(C40_abs - sig_vals["C40"]) * 1.5
            + abs(C42_abs - sig_vals["C42"]) * 2.0
            + abs(C42_real - sig_vals["C42_real"]) * 1.0
        )
        scores[mod_name] = 1.0 / (1.0 + d)

    total = sum(scores.values()) + 1e-9
    normalized_scores = {k: round(float(v / total), 4) for k, v in scores.items()}
    best_mod = max(normalized_scores, key=normalized_scores.get)
    confidence = normalized_scores[best_mod]

    return {
        "modulation": best_mod,
        "confidence": float(confidence),
        "cumulants": cums,
        "features": {
            "|C40|": round(C40_abs, 4),
            "|C42|": round(C42_abs, 4),
            "C42_real": round(C42_real, 4),
        },
        "all_scores": normalized_scores,
        "fsk_info": fsk_info,
    }
