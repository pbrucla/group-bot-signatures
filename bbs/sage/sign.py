from BLS12381 import compute_pairing, Fr
from util import create_challenge_hash, E1_point_to_bytes, int_to_bytes, Rbytes
from verify import BBS04PublicKey

class BBS04SigningKey:
    def __init__(self, gpk, sk):
        self.gpk = BBS04PublicKey(gpk)
        self.A, self.x = sk
        # precompute
        self.e_A_g2 = compute_pairing(self.A, self.gpk.g2)

    def sign(self, msg):
        T1, T2, T3, c, s1, s2, s3, s4, s5 = self._sign(msg)
        sign_bytes = b''
        for point in (T1, T2, T3):
            sign_bytes += E1_point_to_bytes(point)
        for scalar in (c, s1, s2, s3, s4, s5):
            sign_bytes += int_to_bytes(scalar, L=Rbytes)
        return sign_bytes


    def _sign(self, msg):
        _, _, h, u, v, _ = self.gpk.public_key()
        # compute Ts
        alpha = Fr.random_element()
        beta = Fr.random_element()

        T_1 = alpha * u
        T_2 = beta * v
        T_3 = self.A + (alpha + beta) * h

        # compute Rs 
        r_1 = Fr.random_element()
        r_2 = Fr.random_element()
        r_3 = Fr.random_element()
        r_4 = Fr.random_element()
        r_5 = Fr.random_element()

        R_1 = u * r_1
        R_2 = v * r_2
        R_3 = ((self.e_A_g2 * self.gpk.e_h_g2 ** (alpha + beta)) ** r_3 * self.gpk.e_h_w  ** (-(r_1 + r_2)) * self.gpk.e_h_g2 ** (-(r_4 + r_5)))
        R_4 = (T_1 * r_3) + (u * r_4 * -1)
        R_5 = (T_2 * r_3) + (v * r_5 * -1)

        # compute challenge
        challenge = create_challenge_hash(msg, T_1, T_2, T_3, R_1, R_2, R_3, R_4, R_5)

        # construct s values
        s_1 = r_1 + challenge * alpha
        s_2 = r_2 + challenge * beta
        s_3 = r_3 + challenge * self.x
        s_4 = r_4 + challenge * (self.x * alpha)
        s_5 = r_5 + challenge * (self.x * beta)
        # return signature
        return T_1, T_2, T_3, challenge, s_1, s_2, s_3, s_4, s_5