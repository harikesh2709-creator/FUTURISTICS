"""
Viterbi Decoder — Convolutional code encoder and soft/hard-decision
Viterbi decoder for constraint lengths K=5, 7, 9.

Includes the NASA standard K=7 R=1/2 code:
  G1 = 171₈ (0b1111001 = 0x79)
  G2 = 133₈ (0b1011011 = 0x5B)
"""

import numpy as np


# ---------------------------------------------------------------------------
# Standard convolutional code generator polynomials
# ---------------------------------------------------------------------------
_CODES = {
    5: {"generators": [0o35, 0o23], "rate": 0.5, "name": "K=5 R=1/2"},
    7: {"generators": [0o171, 0o133], "rate": 0.5, "name": "NASA K=7 R=1/2"},
    9: {"generators": [0o753, 0o561], "rate": 0.5, "name": "K=9 R=1/2"},
}


# ---------------------------------------------------------------------------
# Convolutional Encoder
# ---------------------------------------------------------------------------
def convolutional_encode(
    bits: np.ndarray,
    constraint_length: int = 7,
) -> np.ndarray:
    """
    Rate-1/2 convolutional encoder.

    Parameters
    ----------
    bits : input data bits (uint8, values 0 or 1)
    constraint_length : K (5, 7, or 9)

    Returns encoded bits (twice the length of input).
    """
    if constraint_length not in _CODES:
        raise ValueError(f"Unsupported constraint length K={constraint_length}. Use 5, 7, or 9.")

    gens = _CODES[constraint_length]["generators"]
    K = constraint_length
    state = 0
    mask = (1 << K) - 1  # K-bit mask
    output = []

    for b in bits:
        state = ((state << 1) | int(b)) & mask
        for g in gens:
            parity = bin(state & g).count("1") % 2
            output.append(parity)

    return np.array(output, dtype=np.uint8)


# ---------------------------------------------------------------------------
# Viterbi Decoder
# ---------------------------------------------------------------------------
def viterbi_decode(
    received: np.ndarray,
    constraint_length: int = 7,
    hard_decision: bool = True,
    traceback_depth: int = 0,
) -> dict:
    """
    Viterbi decoder for rate-1/2 convolutional codes.

    Parameters
    ----------
    received : received bits or soft values
               For hard_decision=True: uint8 bits (0 or 1), taken in pairs.
               For hard_decision=False: float soft values, taken in pairs.
    constraint_length : K (5, 7, or 9)
    hard_decision : if True, uses Hamming distance; else Euclidean distance
    traceback_depth : depth for traceback (0 = 5*K default)

    Returns dict:
        decoded_bits : np.ndarray uint8 — decoded data bits
        path_metric  : final best path metric
        ber_estimate : estimated BER from path metric
    """
    if constraint_length not in _CODES:
        raise ValueError(f"Unsupported K={constraint_length}")

    gens = _CODES[constraint_length]["generators"]
    K = constraint_length
    n_states = 1 << (K - 1)
    n_outputs = len(gens)  # 2 for rate 1/2

    if traceback_depth <= 0:
        traceback_depth = 5 * K

    # Pre-compute branch outputs for each state and input bit
    branch_outputs = np.zeros((n_states, 2, n_outputs), dtype=np.uint8)
    for state in range(n_states):
        for inp in range(2):
            full_state = ((state << 1) | inp) & ((1 << K) - 1)
            for g_idx, g in enumerate(gens):
                branch_outputs[state, inp, g_idx] = bin(full_state & g).count("1") % 2

    # Number of trellis steps
    if len(received) % n_outputs != 0:
        # Pad
        pad_len = n_outputs - (len(received) % n_outputs)
        received = np.concatenate([received, np.zeros(pad_len, dtype=received.dtype)])

    n_steps = len(received) // n_outputs

    # Path metrics
    INF = 1e9
    path_metrics = np.full(n_states, INF)
    path_metrics[0] = 0  # Start in state 0

    # Traceback memory
    survivors = np.zeros((n_steps, n_states), dtype=int)  # Previous state
    decisions = np.zeros((n_steps, n_states), dtype=np.uint8)  # Input bit

    for step in range(n_steps):
        rx = received[step * n_outputs: (step + 1) * n_outputs]
        new_metrics = np.full(n_states, INF)

        for state in range(n_states):
            if path_metrics[state] >= INF:
                continue

            for inp in range(2):
                # Next state
                next_state = ((state << 1) | inp) & (n_states - 1)

                # Branch metric
                expected = branch_outputs[state, inp]
                if hard_decision:
                    bm = np.sum(np.abs(rx.astype(int) - expected.astype(int)))
                else:
                    # Soft: Euclidean distance (rx expected to be ±1 or 0..1)
                    expected_soft = expected.astype(float) * 2 - 1  # Map 0,1 → -1,+1
                    bm = np.sum((rx - expected_soft) ** 2)

                total = path_metrics[state] + bm

                if total < new_metrics[next_state]:
                    new_metrics[next_state] = total
                    survivors[step, next_state] = state
                    decisions[step, next_state] = inp

        path_metrics = new_metrics

        # Normalize to prevent overflow
        min_metric = np.min(path_metrics)
        if min_metric > 1000:
            path_metrics -= min_metric

    # Traceback from best final state
    best_state = np.argmin(path_metrics)
    best_metric = path_metrics[best_state]

    decoded = np.zeros(n_steps, dtype=np.uint8)
    state = best_state
    for step in range(n_steps - 1, -1, -1):
        decoded[step] = decisions[step, state]
        state = survivors[step, state]

    # BER estimate from path metric
    if hard_decision:
        ber_est = float(best_metric) / (n_steps * n_outputs)
    else:
        ber_est = 0.0  # Not meaningful for soft

    return {
        "decoded_bits": decoded,
        "path_metric": float(best_metric),
        "ber_estimate": round(ber_est, 6),
        "num_decoded": len(decoded),
        "constraint_length": K,
        "code_name": _CODES[K]["name"],
    }
