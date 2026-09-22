"""
De-interleaver Engine — Implements Block, Convolutional (Forney/Ramsey),
Diagonal, and Pseudo-Random de-interleaving algorithms.
"""

import numpy as np


# ---------------------------------------------------------------------------
# Block De-interleaver
# ---------------------------------------------------------------------------
def block_deinterleave(
    data: np.ndarray,
    rows: int,
    cols: int,
) -> np.ndarray:
    """
    Block de-interleaver: inverse of writing row-wise, reading column-wise.
    Processes all blocks across the entire data stream.
    """
    block_size = rows * cols
    if block_size <= 0:
        return data

    n_blocks = max(1, len(data) // block_size)
    total = n_blocks * block_size
    if len(data) < total:
        padded = np.pad(data, (0, total - len(data)))
    else:
        padded = data[:total]

    out_blocks = []
    for b in range(n_blocks):
        blk = padded[b * block_size : (b + 1) * block_size]
        matrix = blk.reshape(cols, rows).T
        out_blocks.append(matrix.flatten())

    return np.concatenate(out_blocks)


def block_interleave(
    data: np.ndarray,
    rows: int,
    cols: int,
) -> np.ndarray:
    """Block interleaver: write rows, read columns across all blocks."""
    block_size = rows * cols
    if block_size <= 0:
        return data

    n_blocks = max(1, len(data) // block_size)
    total = n_blocks * block_size
    if len(data) < total:
        padded = np.pad(data, (0, total - len(data)))
    else:
        padded = data[:total]

    out_blocks = []
    for b in range(n_blocks):
        blk = padded[b * block_size : (b + 1) * block_size]
        matrix = blk.reshape(rows, cols)
        out_blocks.append(matrix.T.flatten())

    return np.concatenate(out_blocks)


# ---------------------------------------------------------------------------
# Convolutional De-interleaver (Forney / Ramsey)
# ---------------------------------------------------------------------------
def convolutional_deinterleave(
    data: np.ndarray,
    branches: int,
    delay_per_branch: int,
) -> np.ndarray:
    """
    Convolutional (Forney) de-interleaver.

    The interleaver uses B branches with delays 0, M, 2M, ..., (B-1)*M.
    The de-interleaver uses inverse delays: (B-1)*M, (B-2)*M, ..., M, 0.

    Parameters
    ----------
    data : interleaved data
    branches : number of branches (B)
    delay_per_branch : delay increment per branch (M)
    """
    B = branches
    M = delay_per_branch
    N = len(data)

    # Create shift register banks
    max_delay = (B - 1) * M
    output = np.zeros(N, dtype=data.dtype)

    # Initialize shift registers for each branch
    shift_regs = [np.zeros(delay, dtype=data.dtype) if delay > 0 else None
                  for delay in range((B - 1) * M, -1, -M)]
    # shift_regs[b] has delay = (B-1-b)*M

    for i in range(N):
        branch = i % B
        sr = shift_regs[branch]
        if sr is not None and len(sr) > 0:
            output[i] = sr[0]
            sr[:-1] = sr[1:]
            sr[-1] = data[i]
        else:
            output[i] = data[i]

    return output


def convolutional_interleave(
    data: np.ndarray,
    branches: int,
    delay_per_branch: int,
) -> np.ndarray:
    """Convolutional interleaver (forward direction)."""
    B = branches
    M = delay_per_branch
    N = len(data)
    output = np.zeros(N, dtype=data.dtype)

    shift_regs = [np.zeros(b * M, dtype=data.dtype) if b * M > 0 else None
                  for b in range(B)]

    for i in range(N):
        branch = i % B
        sr = shift_regs[branch]
        if sr is not None and len(sr) > 0:
            output[i] = sr[0]
            sr[:-1] = sr[1:]
            sr[-1] = data[i]
        else:
            output[i] = data[i]

    return output


# ---------------------------------------------------------------------------
# Diagonal De-interleaver
# ---------------------------------------------------------------------------
def diagonal_deinterleave(
    data: np.ndarray,
    rows: int,
    cols: int,
) -> np.ndarray:
    """
    Diagonal (helical scan) de-interleaver.

    Interleaver writes column-by-column, reads along diagonals.
    De-interleaver reverses this permutation.

    Parameters
    ----------
    data : interleaved data
    rows : matrix height
    cols : matrix width
    """
    total = rows * cols
    n = len(data)
    if n < total:
        data = np.concatenate([data, np.zeros(total - n, dtype=data.dtype)])
    else:
        data = data[:total]

    # Build the interleaver permutation (diagonal read order)
    perm = []
    for d in range(rows + cols - 1):
        for r in range(rows):
            c = d - r
            if 0 <= c < cols:
                perm.append(r * cols + c)

    # Inverse permutation
    inv_perm = np.zeros(total, dtype=int)
    for i, p in enumerate(perm[:total]):
        if i < total and p < total:
            inv_perm[p] = i

    output = np.zeros(total, dtype=data.dtype)
    for i in range(total):
        if inv_perm[i] < len(data):
            output[i] = data[inv_perm[i]]

    return output


# ---------------------------------------------------------------------------
# Pseudo-Random De-interleaver
# ---------------------------------------------------------------------------
def _generate_pr_permutation(size: int, seed: int = 42) -> np.ndarray:
    """Generate a deterministic pseudo-random permutation using an LFSR-like seed."""
    rng = np.random.default_rng(seed)
    perm = rng.permutation(size)
    return perm


def pseudorandom_deinterleave(
    data: np.ndarray,
    block_size: int = 0,
    seed: int = 42,
) -> np.ndarray:
    """
    Pseudo-random de-interleaver using a deterministic permutation
    generated from a seed value.

    Parameters
    ----------
    data : interleaved data
    block_size : permutation block size (0 = use full data length)
    seed : LFSR / PRNG seed for permutation generation
    """
    if block_size <= 0:
        block_size = len(data)

    N = len(data)
    output = np.zeros(N, dtype=data.dtype)

    # Process in blocks
    for start in range(0, N, block_size):
        end = min(start + block_size, N)
        blen = end - start
        perm = _generate_pr_permutation(blen, seed)

        # Inverse permutation
        inv_perm = np.argsort(perm)
        output[start:end] = data[start:end][inv_perm[:blen]]

    return output


# ---------------------------------------------------------------------------
# Unified interface
# ---------------------------------------------------------------------------
def deinterleave(
    data: np.ndarray,
    method: str = "block",
    rows: int = 16,
    cols: int = 16,
    branches: int = 8,
    delay_per_branch: int = 17,
    seed: int = 42,
) -> dict:
    """
    Apply de-interleaving with the specified method.

    Parameters
    ----------
    data : input data array (bits or soft values)
    method : "block", "convolutional", "diagonal", "pseudorandom"
    rows, cols : matrix dimensions for block/diagonal
    branches, delay_per_branch : for convolutional
    seed : for pseudo-random

    Returns dict:
        output : de-interleaved data
        method : method used
        params : parameters used
    """
    method = method.lower().replace("-", "").replace("_", "").replace(" ", "")

    if method in ("block", "blk"):
        result = block_deinterleave(data, rows, cols)
        params = {"rows": rows, "cols": cols}
    elif method in ("convolutional", "conv", "forney", "ramsey"):
        result = convolutional_deinterleave(data, branches, delay_per_branch)
        params = {"branches": branches, "delay_per_branch": delay_per_branch}
    elif method in ("diagonal", "diag", "helical"):
        result = diagonal_deinterleave(data, rows, cols)
        params = {"rows": rows, "cols": cols}
    elif method in ("pseudorandom", "pr", "random", "lfsr"):
        result = pseudorandom_deinterleave(data, rows * cols, seed)
        params = {"block_size": rows * cols, "seed": seed}
    else:
        raise ValueError(f"Unknown de-interleaving method: {method}")

    return {
        "output": result,
        "method": method,
        "params": params,
    }
