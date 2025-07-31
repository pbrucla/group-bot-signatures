from BLS12381 import compute_pairing, Fr
from util import bytes_to_E1_point, Lbytes, Rbytes, create_challenge_hash

class BBS04PublicKey:
    def __init__(self, gpk):
        self.g1, self.g2, self.h, self.u, self.v, self.w = gpk
        # precompute
        self.e_h_w = compute_pairing(self.h, self.w)
        self.e_h_g2 = compute_pairing(self.h, self.g2)
        self.e_g1_g2 = compute_pairing(self.g1, self.g2)

    def verify(self, msg, signature):
        sigma = [signature[i:i+Lbytes] for i in range(0, Lbytes*3, Lbytes)] + [signature[i:i+Rbytes] for i in range(Lbytes*3, len(signature), Rbytes)]
        for i in range(3):
            sigma[i] = bytes_to_E1_point(sigma[i])
        for i in range(3, len(sigma)):
            sigma[i] = Fr(int.from_bytes(sigma[i], "big"))
        return self._verify(msg, sigma)

    def _verify(self, msg, sigma):
        T1, T2, T3, c, s_alpha, s_beta, s_x, s_delta1, s_delta2 = sigma

        # Re-derive R1-R5
        R1 = self.u*(s_alpha) + T1*(-c)              # u^(s_alpha) * T1^(-c)
        R2 = self.v*(s_beta) + T2*(-c)               # v^(s_beta) * T2^(-c)
        R4 = T1*(s_x) + self.u*(-s_delta1)           # T1^(s_x) * u^(-s_delta1)
        R5 = T2*(s_x) + self.v*(-s_delta2)           # T2^(s_x) * v^(-s_delta2)
        # Compute R3
        e_T3 = compute_pairing(T3, (c * self.w) + (s_x * self.g2))
        R3 = e_T3 * self.e_h_w**(-s_alpha - s_beta) * self.e_h_g2**(-s_delta1 - s_delta2) * self.e_g1_g2**(-c)

        # Re-compute c, call it c'
        c_prime = create_challenge_hash(msg, T1, T2, T3, R1, R2, R3, R4, R5)

        # Accept if c' == c, otherwise reject
        return c_prime == c
    
    def public_key(self):
        return self.g1, self.g2, self.h, self.u, self.v, self.w