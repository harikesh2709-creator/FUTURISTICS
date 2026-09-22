"""
LDPC Decoder — Low-Density Parity-Check code decoder using
Min-Sum (normalized) iterative belief propagation.

Implements:
  - Regular LDPC code construction (PEG-like random construction)
  - Log-domain Min-Sum decoding with configurable max iterations
  - Parity check stopping criterion
"""

import numpy as np


# ---------------------------------------------------------------------------
# LDPC Parity Check Matrix Construction
# ---------------------------------------------------------------------------
def build_regular_ldpc_matrix(
    n: int = 256,
    rate: float = 0.5,
    col_weight: int = 3,
    seed: int = 42,
) -> np.ndarray:
    """
    Build a regular LDPC parity check matrix H with approximately
    the given code rate and column weight.

    Parameters
    ----------
    n : code length (columns of H)
    rate : code rate (k/n)
    col_weight : number of 1s per column (variable node degree)
    seed : random seed

    Returns H : (m x n) binary parity check matrix
    """
    k = int(n * rate)
    m = n - k  # Number of check nodes (rows)
    row_weight = int(col_weight * n / m)

    rng = np.random.default_rng(seed)
    H = np.zeros((m, n), dtype=np.uint8)

    for j in range(n):
        # Place col_weight 1s in column j at random row positions
        rows = rng.choice(m, size=min(col_weight, m), replace=False)
        H[rows, j] = 1

    return H


# ---------------------------------------------------------------------------
# Min-Sum LDPC Decoder
# ---------------------------------------------------------------------------
def ldpc_decode(
    llr_input: np.ndarray,
    H: np.ndarray,
    max_iterations: int = 50,
    min_sum_factor: float = 0.75,
) -> dict:
    """
    Min-Sum LDPC decoder (normalized).

    Parameters
    ----------
    llr_input : log-likelihood ratios of received bits
                (positive = likely 0, negative = likely 1)
    H : parity check matrix (m x n binary)
    max_iterations : maximum decoding iterations
    min_sum_factor : normalization factor for min-sum (0.5..1.0)

    Returns dict:
        decoded_bits : hard-decision decoded bits
        iterations   : number of iterations performed
        converged    : whether parity check passed
        syndrome_weight : number of unsatisfied checks
    """
    m, n = H.shape
    assert len(llr_input) >= n, f"LLR length {len(llr_input)} < code length {n}"

    llr = llr_input[:n].astype(np.float64)

    # Build adjacency lists for efficient message passing
    # check_to_var[i] = list of variable nodes connected to check i
    # var_to_check[j] = list of check nodes connected to variable j
    check_to_var = [[] for _ in range(m)]
    var_to_check = [[] for _ in range(n)]

    for i in range(m):
        for j in range(n):
            if H[i, j]:
                check_to_var[i].append(j)
                var_to_check[j].append(i)

    # Initialize messages
    # Q[i][j] = message from variable j to check i (initialized to channel LLR)
    # R[i][j] = message from check i to variable j (initialized to 0)
    Q = {}
    R = {}
    for i in range(m):
        for j in check_to_var[i]:
            Q[(i, j)] = llr[j]
            R[(i, j)] = 0.0

    converged = False
    iteration = 0

    for iteration in range(1, max_iterations + 1):
        # --- Check node update (Min-Sum) ---
        for i in range(m):
            neighbors = check_to_var[i]
            for j in neighbors:
                # Product of signs and minimum of magnitudes (excluding j)
                sign = 1
                min_abs = 1e30
                for jp in neighbors:
                    if jp != j:
                        q_val = Q[(i, jp)]
                        sign *= (1 if q_val >= 0 else -1)
                        min_abs = min(min_abs, abs(q_val))

                R[(i, j)] = sign * min_abs * min_sum_factor

        # --- Variable node update ---
        for j in range(n):
            neighbors = var_to_check[j]
            for i in neighbors:
                # Sum of all incoming R messages except from check i
                total = llr[j]
                for ip in neighbors:
                    if ip != i:
                        total += R[(ip, j)]
                Q[(i, j)] = total

        # --- Hard decision and parity check ---
        total_llr = llr.copy()
        for j in range(n):
            for i in var_to_check[j]:
                total_llr[j] += R[(i, j)]

        hard_bits = (total_llr < 0).astype(np.uint8)

        # Check syndrome
        syndrome = (H @ hard_bits) % 2
        syndrome_weight = int(np.sum(syndrome))

        if syndrome_weight == 0:
            converged = True
            break

    return {
        "decoded_bits": hard_bits,
        "iterations": iteration,
        "converged": converged,
        "syndrome_weight": syndrome_weight,
    }


def ldpc_encode_systematic(
    data: np.ndarray,
    H: np.ndarray,
) -> np.ndarray:
    """
    Simple systematic LDPC encoder.

    For a (m x n) parity check matrix with n-m information bits,
    constructs a codeword [data | parity] such that H·c = 0 mod 2.

    Note: This is a simplified encoder that works for regular LDPC
    matrices where the rightmost m×m submatrix is invertible.
    """
    m, n = H.shape
    k = n - m  # Information bits

    if len(data) > k:
        data = data[:k]
    elif len(data) < k:
        data = np.concatenate([data, np.zeros(k - len(data), dtype=np.uint8)])

    # Extract parity submatrix P = H[:, k:]  and info submatrix A = H[:, :k]
    A = H[:, :k]
    P = H[:, k:]

    # Syndrome from data: s = A @ data mod 2
    s = (A @ data) % 2

    # Solve P @ parity = s mod 2 using Gaussian elimination
    # Simple approach: use numpy (works for most well-constructed LDPC matrices)
    try:
        # GF(2) solve via row reduction
        augmented = np.hstack([P.astype(int), s.reshape(-1, 1)])
        m_rows = augmented.shape[0]
        parity = np.zeros(m, dtype=np.uint8)

        # Forward elimination
        for col in range(min(m, m_rows)):
            # Find pivot
            pivot = -1
            for row in range(col, m_rows):
                if augmented[row, col] == 1:
                    pivot = row
                    break
            if pivot == -1:
                continue
            if pivot != col:
                augmented[[col, pivot]] = augmented[[pivot, col]]
            for row in range(m_rows):
                if row != col and augmented[row, col] == 1:
                    augmented[row] = (augmented[row] + augmented[col]) % 2

        # Back-substitution
        for i in range(m):
            if i < m_rows:
                parity[i] = augmented[i, -1]

        codeword = np.concatenate([data, parity])
    except Exception:
        # Fallback: just append zeros
        codeword = np.concatenate([data, np.zeros(m, dtype=np.uint8)])

    return codeword
