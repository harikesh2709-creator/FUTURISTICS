"""
interleave.py
Block interleaver/deinterleaver (write-by-row, read-by-column), plus a
depth-search routine for the receiver side, since the depth is not
known a priori. Convolutional/diagonal/pseudo-random interleavers follow
the same "parametrized transform + verify by downstream decode success"
pattern; block is implemented fully here as the reference case and the
search harness (`search_deinterleave_depth`) is written generically
enough to be reused once those transforms are added.
"""

import numpy as np


def block_interleave(bits, depth):
    n = len(bits)
    cols = n // depth
    usable = depth * cols
    matrix = bits[:usable].reshape(depth, cols)
    interleaved = matrix.T.flatten()  # write by row, read by column
    return interleaved, bits[usable:]  # return leftover tail bits too


def block_deinterleave(bits, depth):
    n = len(bits)
    blk_size = depth * depth
    if blk_size > 0 and n >= blk_size:
        n_blocks = n // blk_size
        total = n_blocks * blk_size
        out = []
        for b in range(n_blocks):
            blk = bits[b * blk_size : (b + 1) * blk_size]
            matrix = blk.reshape(depth, depth).T
            out.append(matrix.flatten())
        if total < n:
            out.append(bits[total:])
        return np.concatenate(out)

    cols = n // depth
    usable = depth * cols
    matrix = bits[:usable].reshape(cols, depth)
    deinterleaved = matrix.T.flatten()
    return deinterleaved


def search_deinterleave_depth(bits, candidate_depths, score_fn):
    """
    Try each candidate depth, deinterleave, run score_fn(deinterleaved_bits)
    which should return a lower-is-better score (e.g. post-FEC-decode
    residual bit-error rate from re-encoding). Returns the best depth,
    its deinterleaved bits, and the score table for transparency in the UI.
    """
    results = []
    best = None
    for d in candidate_depths:
        if d <= 0 or d > len(bits):
            continue
        try:
            deint = block_deinterleave(bits, d)
            score = score_fn(deint)
        except Exception:
            score = float("inf")
            deint = None
        results.append({"depth": d, "score": score})
        if deint is not None and (best is None or score < best[2]):
            best = (d, deint, score)

    results.sort(key=lambda r: r["score"])
    if best is None:
        return None, None, results
    return best[0], best[1], results
