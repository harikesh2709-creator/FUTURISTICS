"""
fec.py
Convolutional encoder and hard-decision Viterbi decoder.
Default: constraint length K=7, rate 1/2, generators (171, 133) octal --
the standard NASA/CCSDS short convolutional code, a common default to
try first per the problem statement's "short-constrained convolution
codes with Viterbi decoding" requirement.

Extension points: Reed-Solomon (use a GF(2^m) library), concatenated
RS+conv (chain rs_decode -> conv_decode), and LDPC (belief propagation
over a known parity-check matrix) are not implemented here but the
pipeline is structured so they can be dropped in as alternate `decode`
functions.
"""

import numpy as np


def _poly_taps(value, K):
    """
    Convert a generator polynomial to a tap bitmask of length K.
    `value` is an int whose binary representation is the tap pattern --
    pass Python octal literals like 0o171 directly (0o171 == 0b1111001),
    not a string/decimal restatement of the octal digits.
    """
    bits = [(value >> i) & 1 for i in range(K - 1, -1, -1)]
    return np.array(bits, dtype=np.uint8)


class ConvCode:
    def __init__(self, K=7, generators=(0o171, 0o133)):
        self.K = K
        self.n_states = 2 ** (K - 1)
        self.taps = [_poly_taps(g, K) for g in generators]
        self.rate = 1.0 / len(generators)
        self._build_trellis()

    def _output_for(self, state, bit):
        reg = ((state << 1) | bit) & (2 ** self.K - 1)
        reg_bits = np.array([(reg >> i) & 1 for i in range(self.K - 1, -1, -1)], dtype=np.uint8)
        outs = [int(np.bitwise_xor.reduce(reg_bits * t)) for t in self.taps]
        next_state = reg & (self.n_states - 1)
        return next_state, outs

    def _build_trellis(self):
        self.next_state = np.zeros((self.n_states, 2), dtype=np.int32)
        self.output = np.zeros((self.n_states, 2, len(self.taps)), dtype=np.uint8)
        self.pred_state_0 = np.zeros(self.n_states, dtype=np.int32)
        self.pred_bit_0 = np.zeros(self.n_states, dtype=np.uint8)
        self.pred_state_1 = np.zeros(self.n_states, dtype=np.int32)
        self.pred_bit_1 = np.zeros(self.n_states, dtype=np.uint8)

        pred_counts = np.zeros(self.n_states, dtype=int)
        for s in range(self.n_states):
            for b in (0, 1):
                ns, outs = self._output_for(s, b)
                self.next_state[s, b] = ns
                self.output[s, b] = outs
                if pred_counts[ns] == 0:
                    self.pred_state_0[ns] = s
                    self.pred_bit_0[ns] = b
                    pred_counts[ns] += 1
                else:
                    self.pred_state_1[ns] = s
                    self.pred_bit_1[ns] = b

    def encode(self, bits):
        state = 0
        coded = []
        for b in bits:
            ns = self.next_state[state, b]
            outs = self.output[state, b]
            coded.extend(outs.tolist())
            state = ns
        return np.array(coded, dtype=np.uint8)

    def decode(self, coded_bits):
        """Hard-decision Viterbi decoding with vectorized trellis updates."""
        n_out = len(self.taps)
        n_symbols = len(coded_bits) // n_out
        received = coded_bits[: n_symbols * n_out].reshape(n_symbols, n_out)

        INF = 1e9
        path_metric = np.full(self.n_states, INF, dtype=np.float64)
        path_metric[0] = 0.0
        traceback = np.zeros((n_symbols, self.n_states), dtype=np.int32)
        bit_history = np.zeros((n_symbols, self.n_states), dtype=np.uint8)

        # Vectorized Viterbi trellis traversal
        for t in range(n_symbols):
            bm = np.sum(self.output != received[t], axis=-1)  # shape (n_states, 2)

            cand0 = path_metric[self.pred_state_0] + bm[self.pred_state_0, self.pred_bit_0]
            cand1 = path_metric[self.pred_state_1] + bm[self.pred_state_1, self.pred_bit_1]

            choose1 = cand1 < cand0
            path_metric = np.where(choose1, cand1, cand0)
            traceback[t] = np.where(choose1, self.pred_state_1, self.pred_state_0)
            bit_history[t] = np.where(choose1, self.pred_bit_1, self.pred_bit_0)

        state = int(np.argmin(path_metric))
        decoded = np.zeros(n_symbols, dtype=np.uint8)
        for t in range(n_symbols - 1, -1, -1):
            decoded[t] = bit_history[t, state]
            state = traceback[t, state]

        return decoded, {"final_path_metric": float(np.min(path_metric)), "n_symbols": n_symbols}


def bit_error_rate(a, b):
    n = min(len(a), len(b))
    if n == 0:
        return 1.0
    return float(np.mean(a[:n] != b[:n]))
