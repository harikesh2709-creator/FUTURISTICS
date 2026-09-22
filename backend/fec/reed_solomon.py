"""
Reed-Solomon Codec — GF(2^8) Reed-Solomon encoder and decoder with
Berlekamp-Massey algorithm, Chien search, and Forney algorithm.

Supports:
  - CCSDS RS(255, 223) with t=16 symbol error correction
  - DVB RS(204, 188) with t=8 (shortened RS(255, 239))
  - Custom RS(n, k) over GF(2^8)

Field generator polynomial: p(x) = x^8 + x^4 + x^3 + x^2 + 1 (0x11D)
"""

import numpy as np


# ---------------------------------------------------------------------------
# Galois Field GF(2^8) arithmetic
# ---------------------------------------------------------------------------
class GF256:
    """Galois Field GF(2^8) with primitive polynomial 0x11D."""

    PRIM_POLY = 0x11D  # x^8 + x^4 + x^3 + x^2 + 1

    def __init__(self):
        self.exp_table = np.zeros(512, dtype=np.int32)
        self.log_table = np.zeros(256, dtype=np.int32)
        self._build_tables()

    def _build_tables(self):
        x = 1
        for i in range(255):
            self.exp_table[i] = x
            self.log_table[x] = i
            x <<= 1
            if x & 0x100:
                x ^= self.PRIM_POLY
        # Extend exp table for easier mod operations
        for i in range(255, 512):
            self.exp_table[i] = self.exp_table[i - 255]

    def mul(self, a: int, b: int) -> int:
        if a == 0 or b == 0:
            return 0
        return int(self.exp_table[self.log_table[a] + self.log_table[b]])

    def div(self, a: int, b: int) -> int:
        if b == 0:
            raise ZeroDivisionError("Division by zero in GF(2^8)")
        if a == 0:
            return 0
        return int(self.exp_table[(self.log_table[a] - self.log_table[b]) % 255])

    def pow(self, a: int, n: int) -> int:
        if a == 0:
            return 0
        return int(self.exp_table[(self.log_table[a] * n) % 255])

    def inv(self, a: int) -> int:
        if a == 0:
            raise ZeroDivisionError("Inverse of zero")
        return int(self.exp_table[255 - self.log_table[a]])

    def poly_eval(self, poly: list, x: int) -> int:
        """Evaluate polynomial at x in GF(2^8). poly[0] = highest degree."""
        result = 0
        for coeff in poly:
            result = self.mul(result, x) ^ coeff
        return result

    def poly_mul(self, p: list, q: list) -> list:
        """Multiply two polynomials in GF(2^8)."""
        result = [0] * (len(p) + len(q) - 1)
        for i, a in enumerate(p):
            for j, b in enumerate(q):
                result[i + j] ^= self.mul(a, b)
        return result

    def alpha(self, i: int) -> int:
        """Return α^i (primitive element raised to i-th power)."""
        return int(self.exp_table[i % 255])


# Singleton GF instance
_gf = GF256()


# ---------------------------------------------------------------------------
# Reed-Solomon Encoder
# ---------------------------------------------------------------------------
def rs_encode(
    data: np.ndarray,
    nsym: int = 32,
    fcr: int = 0,
) -> np.ndarray:
    """
    RS encoder: append nsym parity symbols to data.

    Parameters
    ----------
    data : message symbols (uint8 array, length k)
    nsym : number of parity symbols (2t)
    fcr  : first consecutive root index

    Returns encoded codeword (data + parity), length k + nsym
    """
    # Build generator polynomial g(x) = Π(x - α^i) for i = fcr..fcr+nsym-1
    gen = [1]
    for i in range(fcr, fcr + nsym):
        gen = _gf.poly_mul(gen, [1, _gf.alpha(i)])

    # Polynomial long division: data * x^nsym / g(x)
    msg = list(data.astype(int)) + [0] * nsym
    for i in range(len(data)):
        coeff = msg[i]
        if coeff != 0:
            for j in range(len(gen)):
                msg[i + j] ^= _gf.mul(gen[j], coeff)

    # msg now has remainder in last nsym positions
    codeword = list(data.astype(int)) + msg[len(data):]
    return np.array(codeword, dtype=np.uint8)


# ---------------------------------------------------------------------------
# Reed-Solomon Decoder
# ---------------------------------------------------------------------------
def _compute_syndromes(received: list, nsym: int, fcr: int = 0) -> list:
    """Compute syndromes S_i = R(α^i) for i = fcr..fcr+nsym-1."""
    syndromes = [0] * nsym
    for i in range(nsym):
        syndromes[i] = _gf.poly_eval(received, _gf.alpha(fcr + i))
    return syndromes


def _berlekamp_massey(syndromes: list, nsym: int) -> list:
    """
    Berlekamp-Massey algorithm to find the error locator polynomial Λ(x).
    """
    # Initialize
    C = [1]  # Connection polynomial (error locator)
    B = [1]  # Previous connection polynomial
    L = 0    # Current length of LFSR
    m = 1    # Shift counter
    b = 1    # Previous discrepancy

    for n in range(nsym):
        # Compute discrepancy d
        d = syndromes[n]
        for i in range(1, min(L + 1, len(C))):
            d ^= _gf.mul(C[i], syndromes[n - i])

        if d == 0:
            m += 1
        elif 2 * L <= n:
            T = list(C)
            # C(x) = C(x) - (d/b) * x^m * B(x)
            coeff = _gf.div(d, b)
            pad = [0] * m
            scaled_B = pad + [_gf.mul(coeff, bi) for bi in B]
            # XOR (add in GF)
            while len(C) < len(scaled_B):
                C.append(0)
            for i in range(len(scaled_B)):
                C[i] ^= scaled_B[i]
            L = n + 1 - L
            B = T
            b = d
            m = 1
        else:
            coeff = _gf.div(d, b)
            pad = [0] * m
            scaled_B = pad + [_gf.mul(coeff, bi) for bi in B]
            while len(C) < len(scaled_B):
                C.append(0)
            for i in range(len(scaled_B)):
                C[i] ^= scaled_B[i]
            m += 1

    return C


def _chien_search(error_locator: list, n: int) -> list:
    """
    Chien search: find roots of the error locator polynomial Λ(x)
    by evaluating Λ(α^(-i)) for all i in 0..n-1.

    Returns list of error positions.
    """
    positions = []
    for i in range(n):
        val = _gf.poly_eval(error_locator, _gf.inv(_gf.alpha(i)))
        if val == 0:
            positions.append(i)
    return positions


def _forney_algorithm(
    syndromes: list,
    error_locator: list,
    error_positions: list,
    nsym: int,
    fcr: int = 0,
) -> list:
    """
    Forney algorithm: compute error magnitudes at the identified positions.
    """
    # Compute error evaluator polynomial Ω(x) = S(x) * Λ(x) mod x^nsym
    # where S(x) = S_0 + S_1*x + ... + S_{nsym-1}*x^{nsym-1}
    omega = _gf.poly_mul([1] + syndromes[:nsym], error_locator)
    # Truncate to nsym terms
    omega = omega[:nsym]

    # Formal derivative of Λ(x): Λ'(x) = sum of odd-indexed coefficients
    # In GF(2^m), derivative only keeps odd-power terms
    lambda_prime = [0] * len(error_locator)
    for i in range(1, len(error_locator)):
        if i % 2 == 1:  # Odd indices survive in characteristic 2
            lambda_prime[i] = error_locator[i]
    # Remove leading zeros but keep at least one
    while len(lambda_prime) > 1 and lambda_prime[0] == 0:
        lambda_prime.pop(0)

    magnitudes = []
    for pos in error_positions:
        Xi = _gf.alpha(pos)
        Xi_inv = _gf.inv(Xi)

        # Ω(Xi^-1)
        omega_val = _gf.poly_eval(omega, Xi_inv)

        # Λ'(Xi^-1)
        lambda_p_val = _gf.poly_eval(lambda_prime, Xi_inv)

        if lambda_p_val == 0:
            magnitudes.append(0)
        else:
            # e_i = Xi^(1-fcr) * Ω(Xi^-1) / Λ'(Xi^-1)
            mag = _gf.mul(_gf.pow(Xi, 1 - fcr), _gf.div(omega_val, lambda_p_val))
            magnitudes.append(mag)

    return magnitudes


def rs_decode(
    received: np.ndarray,
    nsym: int = 32,
    fcr: int = 0,
) -> dict:
    """
    Reed-Solomon decoder using Berlekamp-Massey + Chien + Forney.

    Parameters
    ----------
    received : received codeword (uint8 array, may contain errors)
    nsym : number of parity symbols (2t, can correct up to t errors)
    fcr : first consecutive root index

    Returns dict:
        decoded   : corrected codeword (uint8)
        data      : extracted data portion (first n-nsym symbols)
        errors_corrected : number of errors found and corrected
        success   : bool — whether decoding succeeded
    """
    n = len(received)
    r = list(received.astype(int))

    # Step 1: Compute syndromes
    syndromes = _compute_syndromes(r, nsym, fcr)

    # Check if codeword is already valid (all syndromes zero)
    if all(s == 0 for s in syndromes):
        data = np.array(r[:n - nsym], dtype=np.uint8)
        return {
            "decoded": np.array(r, dtype=np.uint8),
            "data": data,
            "errors_corrected": 0,
            "success": True,
        }

    # Step 2: Berlekamp-Massey → error locator polynomial
    error_locator = _berlekamp_massey(syndromes, nsym)

    num_errors = len(error_locator) - 1
    if num_errors > nsym // 2:
        return {
            "decoded": np.array(r, dtype=np.uint8),
            "data": np.array(r[:n - nsym], dtype=np.uint8),
            "errors_corrected": 0,
            "success": False,
        }

    # Step 3: Chien search → error positions
    positions = _chien_search(error_locator, n)

    if len(positions) != num_errors:
        return {
            "decoded": np.array(r, dtype=np.uint8),
            "data": np.array(r[:n - nsym], dtype=np.uint8),
            "errors_corrected": 0,
            "success": False,
        }

    # Step 4: Forney algorithm → error magnitudes
    magnitudes = _forney_algorithm(syndromes, error_locator, positions, nsym, fcr)

    # Apply corrections
    corrected = list(r)
    for pos, mag in zip(positions, magnitudes):
        if pos < n:
            corrected[pos] ^= mag

    data = np.array(corrected[:n - nsym], dtype=np.uint8)

    return {
        "decoded": np.array(corrected, dtype=np.uint8),
        "data": data,
        "errors_corrected": len(positions),
        "success": True,
        "error_positions": positions,
    }


# ---------------------------------------------------------------------------
# Convenience wrappers for standard codes
# ---------------------------------------------------------------------------
def rs_ccsds_encode(data: np.ndarray) -> np.ndarray:
    """CCSDS RS(255, 223) encoder. t=16, nsym=32."""
    if len(data) > 223:
        data = data[:223]
    elif len(data) < 223:
        data = np.concatenate([data, np.zeros(223 - len(data), dtype=np.uint8)])
    return rs_encode(data, nsym=32, fcr=1)


def rs_ccsds_decode(received: np.ndarray) -> dict:
    """CCSDS RS(255, 223) decoder."""
    return rs_decode(received, nsym=32, fcr=1)


def rs_dvb_encode(data: np.ndarray) -> np.ndarray:
    """DVB RS(204, 188) encoder (shortened RS(255, 239)). t=8, nsym=16."""
    if len(data) > 188:
        data = data[:188]
    elif len(data) < 188:
        data = np.concatenate([data, np.zeros(188 - len(data), dtype=np.uint8)])
    # Pad with 51 zeros for shortened code
    padded = np.concatenate([np.zeros(51, dtype=np.uint8), data])
    encoded = rs_encode(padded, nsym=16, fcr=0)
    # Remove the padding
    return np.concatenate([encoded[51:51 + 188], encoded[239:]])


def rs_dvb_decode(received: np.ndarray) -> dict:
    """DVB RS(204, 188) decoder."""
    if len(received) > 204:
        received = received[:204]
    # Pad to RS(255, 239) for decoding
    padded = np.concatenate([np.zeros(51, dtype=np.uint8), received[:188], received[188:]])
    if len(padded) < 255:
        padded = np.concatenate([padded, np.zeros(255 - len(padded), dtype=np.uint8)])
    result = rs_decode(padded[:255], nsym=16, fcr=0)
    if result["success"]:
        result["data"] = result["data"][51:]  # Remove padding
    else:
        result["data"] = received[:188]
    return result
