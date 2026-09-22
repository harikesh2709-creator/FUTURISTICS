"""
Concatenated Code Pipeline — Inner Viterbi + De-interleaver + Outer
Reed-Solomon decoder, following the CCSDS / ESA standard concatenated
coding scheme.
"""

import numpy as np

from .viterbi import viterbi_decode, convolutional_encode
from .reed_solomon import rs_decode, rs_encode


def concatenated_decode(
    received_bits: np.ndarray,
    inner_K: int = 7,
    inner_hard: bool = True,
    interleaver_depth: int = 5,
    outer_nsym: int = 32,
    outer_fcr: int = 1,
) -> dict:
    """
    Concatenated code decoder:
      1. Inner Viterbi decoder (convolutional code)
      2. De-interleaver (symbol-level block de-interleaving)
      3. Outer Reed-Solomon decoder

    Parameters
    ----------
    received_bits : received encoded bit stream
    inner_K : inner convolutional code constraint length
    inner_hard : True for hard-decision Viterbi
    interleaver_depth : block interleaver depth (number of RS codewords interleaved)
    outer_nsym : RS parity symbol count (2t)
    outer_fcr : RS first consecutive root

    Returns dict:
        decoded_data  : final decoded data bytes
        inner_result  : Viterbi decoder output details
        outer_results : list of RS decoder results per codeword
        success       : overall success flag
    """
    # --- Step 1: Inner Viterbi Decoding ---
    inner_result = viterbi_decode(
        received_bits,
        constraint_length=inner_K,
        hard_decision=inner_hard,
    )
    viterbi_bits = inner_result["decoded_bits"]

    # --- Step 2: Bits → Bytes (8 bits per RS symbol) ---
    n_bytes = len(viterbi_bits) // 8
    viterbi_bits = viterbi_bits[:n_bytes * 8]
    symbols = np.packbits(viterbi_bits)

    # --- Step 3: Symbol-level De-interleaving ---
    # The interleaver writes I codewords row-wise into a matrix of
    # I rows × N columns, then reads column-wise.
    # De-interleaver reverses: write column-wise, read row-wise.
    rs_n = 255  # RS codeword length for CCSDS
    if outer_nsym == 16:
        rs_n = 204  # DVB shortened code

    I = interleaver_depth
    total_symbols = I * rs_n

    if len(symbols) < total_symbols:
        symbols = np.concatenate([
            symbols,
            np.zeros(total_symbols - len(symbols), dtype=np.uint8)
        ])

    # Process as many complete interleaved blocks as possible
    n_blocks = len(symbols) // total_symbols
    if n_blocks < 1:
        n_blocks = 1
        symbols = symbols[:total_symbols]

    all_decoded = []
    all_rs_results = []
    overall_success = True

    for blk in range(n_blocks):
        block_syms = symbols[blk * total_symbols : (blk + 1) * total_symbols]

        # De-interleave: reshape as (rs_n, I) column-major → read rows
        if len(block_syms) == total_symbols:
            matrix = block_syms.reshape(rs_n, I).T  # I × rs_n
        else:
            matrix = block_syms.reshape(-1, 1).T

        # --- Step 4: Outer RS Decoding per codeword ---
        for row in range(matrix.shape[0]):
            codeword = matrix[row]
            if len(codeword) < rs_n:
                codeword = np.concatenate([
                    codeword,
                    np.zeros(rs_n - len(codeword), dtype=np.uint8)
                ])

            rs_result = rs_decode(codeword[:rs_n], nsym=outer_nsym, fcr=outer_fcr)
            all_rs_results.append({
                "success": rs_result["success"],
                "errors_corrected": rs_result["errors_corrected"],
            })
            if rs_result["success"]:
                all_decoded.append(rs_result["data"])
            else:
                all_decoded.append(codeword[:rs_n - outer_nsym])
                overall_success = False

    decoded_data = np.concatenate(all_decoded) if all_decoded else np.array([], dtype=np.uint8)

    return {
        "decoded_data": decoded_data,
        "inner_result": {
            "num_decoded": inner_result["num_decoded"],
            "path_metric": inner_result["path_metric"],
            "ber_estimate": inner_result["ber_estimate"],
        },
        "outer_results": all_rs_results,
        "success": overall_success,
        "total_errors_corrected": sum(r["errors_corrected"] for r in all_rs_results),
    }


def concatenated_encode(
    data: np.ndarray,
    inner_K: int = 7,
    interleaver_depth: int = 5,
    outer_nsym: int = 32,
    outer_fcr: int = 1,
) -> np.ndarray:
    """
    Concatenated code encoder:
      1. Outer RS encoding (per data block)
      2. Symbol-level block interleaving
      3. Inner convolutional encoding

    Returns encoded bit stream.
    """
    rs_k = 255 - outer_nsym  # Data symbols per RS codeword
    I = interleaver_depth

    # Pad data to fill I complete RS data blocks
    total_data = I * rs_k
    if len(data) < total_data:
        data = np.concatenate([data, np.zeros(total_data - len(data), dtype=np.uint8)])
    else:
        data = data[:total_data]

    # --- Step 1: Outer RS encoding ---
    codewords = []
    for i in range(I):
        block = data[i * rs_k : (i + 1) * rs_k]
        cw = rs_encode(block, nsym=outer_nsym, fcr=outer_fcr)
        codewords.append(cw)

    # --- Step 2: Symbol-level block interleaving ---
    # Stack codewords as rows, read columns
    matrix = np.array(codewords)  # I × 255
    interleaved = matrix.T.flatten()  # Read column-wise

    # --- Step 3: Inner convolutional encoding ---
    # Convert symbols to bits
    bits = np.unpackbits(interleaved)
    encoded = convolutional_encode(bits, constraint_length=inner_K)

    return encoded
