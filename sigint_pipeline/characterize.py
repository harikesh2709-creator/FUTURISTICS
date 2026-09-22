"""
characterize.py
Blind signal characterization: PSD/waterfall, occupied bandwidth,
symbol-rate estimation (delay-and-multiply cyclostationary method),
and modulation family classification via higher-order cumulants.
"""

import numpy as np
from scipy import signal as sp_signal


def power_spectral_density(iq, fs, nperseg=1024):
    freqs, psd = sp_signal.welch(iq, fs=fs, nperseg=nperseg, return_onesided=False)
    order = np.argsort(freqs)
    return freqs[order], 10 * np.log10(psd[order] + 1e-12)


def waterfall(iq, fs, nperseg=256, noverlap=128):
    f, t, Sxx = sp_signal.spectrogram(
        iq, fs=fs, nperseg=nperseg, noverlap=noverlap, return_onesided=False
    )
    order = np.argsort(f)
    return f[order], t, 10 * np.log10(Sxx[order, :] + 1e-12)


def occupied_bandwidth(iq, fs, threshold_db=-10, nperseg=2048):
    """Bandwidth containing power within threshold_db of the peak."""
    freqs, psd_db = power_spectral_density(iq, fs, nperseg=nperseg)
    peak = np.max(psd_db)
    above = freqs[psd_db >= peak + threshold_db]
    if above.size == 0:
        return 0.0, 0.0
    return float(above.max() - above.min()), float(freqs[np.argmax(psd_db)])


def estimate_symbol_rate(iq, fs, min_rate=1.0, max_rate=None):
    """
    Delay-and-multiply cyclostationary estimator: for many linearly
    modulated signals, |x(t)|^2 (or x(t)^M for M-PSK) contains a spectral
    line at the symbol rate due to pulse-shaping-induced cyclostationarity.
    We search the spectrum of |x|^2 for its strongest non-DC peak.
    """
    if max_rate is None:
        max_rate = fs / 2

    mag_sq = np.abs(iq) ** 2
    mag_sq = mag_sq - np.mean(mag_sq)
    spectrum = np.abs(np.fft.fft(mag_sq))
    freqs = np.fft.fftfreq(len(mag_sq), d=1 / fs)

    mask = (np.abs(freqs) >= min_rate) & (np.abs(freqs) <= max_rate)
    if not np.any(mask):
        return None

    idx = np.argmax(spectrum[mask])
    candidate_freqs = freqs[mask]
    candidate_spec = spectrum[mask]
    peak_freq = abs(candidate_freqs[idx])
    confidence = float(candidate_spec[idx] / (np.mean(candidate_spec) + 1e-9))
    return {"symbol_rate_hz": float(peak_freq), "confidence": confidence}


# ---- Modulation classification via higher-order cumulants ----
#
# Reference statistic: normalized |C42| = |cum(x,x,x*,x*)| / (E[|x|^2])^2
# after removing carrier offset by working on magnitude/phase-invariant
# combinations. This is a coarse, explainable classifier (not ML) that
# separates constant-envelope PSK from multi-amplitude QAM, and uses a
# secondary statistic to split PSK orders.

def _moment(x, n_unconjugated, n_conjugated):
    """M_pq = E[ x^(n_unconjugated) * (x*)^(n_conjugated) ], total order p = n_unconjugated + n_conjugated."""
    return np.mean((x ** n_unconjugated) * (np.conj(x) ** n_conjugated))


def cumulants(x):
    """
    Standard complex-signal higher-order cumulants (Swami & Sadler
    convention), computed on unit-power-normalized samples. M_pq notation:
    total order p, q of which are conjugated.
    """
    x = x / np.sqrt(np.mean(np.abs(x) ** 2) + 1e-12)  # normalize power

    m20 = _moment(x, 2, 0)  # E[x^2]
    m21 = _moment(x, 1, 1)  # E[|x|^2]
    m40 = _moment(x, 4, 0)  # E[x^4]
    m41 = _moment(x, 3, 1)  # E[x^3 x*]
    m42 = _moment(x, 2, 2)  # E[|x|^4]

    c20 = m20
    c21 = m21
    c40 = m40 - 3 * m20 ** 2
    c41 = m41 - 3 * m20 * m21
    c42 = m42 - np.abs(m20) ** 2 - 2 * m21 ** 2

    return {"C20": c20, "C21": c21, "C40": c40, "C41": c41, "C42": c42}


def classify_modulation(iq, candidates=("BPSK", "QPSK", "8PSK", "16QAM")):
    """
    Nearest-neighbor match against the standard theoretical (C40, C42)
    cumulant pairs for unit-power constellations (Swami & Sadler, 2000).
    Distance in (C40, C42) space -> inverse-distance pseudo-confidence.
    """
    c = cumulants(iq)
    c40, c42 = c["C40"], c["C42"]

    # theoretical (C40, C42) for unit average power, phase-averaged:
    reference = {
        "BPSK": (-2.0, -2.0),
        "QPSK": (1.0, -1.0),
        "8PSK": (0.0, -1.0),
        "16QAM": (-0.68, -0.68),
    }

    scores = {}
    for mod in candidates:
        t40, t42 = reference.get(mod, (0.0, 0.0))
        # BPSK's C40 phase depends on unknown carrier phase (magnitude
        # only is reliable); compare magnitudes for C40, real part for C42
        # which is phase-invariant by construction.
        dist = abs(abs(c40) - abs(t40)) + abs(c42.real - t42)
        scores[mod] = 1.0 / (1.0 + dist)

    total = sum(scores.values()) + 1e-9
    ranked = sorted(
        ((mod, s / total) for mod, s in scores.items()),
        key=lambda kv: kv[1],
        reverse=True,
    )
    return ranked, {"C40": complex(c40), "C42": complex(c42)}
