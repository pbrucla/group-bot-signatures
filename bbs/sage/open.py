from BLS12381 import Fr
from util import *
from verify import BBS04PublicKey

class BBS04GroupManagerKey:
    def __init__(self, gpk, gmsk, gmlut):
        self.xi1, self.xi2 = gmsk
        self.gpk = BBS04PublicKey(gpk)
        self.member_lookup = gmlut

    def open(self, msg, signature):
        sigma = [signature[i:i+Lbytes] for i in range(0, Lbytes*3, Lbytes)] + [signature[i:i+Rbytes] for i in range(Lbytes*3, len(signature), Rbytes)]
        for i in range(3):
            sigma[i] = bytes_to_E1_point(sigma[i])
        for i in range(3, len(sigma)):
            sigma[i] = Fr(int.from_bytes(sigma[i], "big"))
        return self._open(msg, sigma)

    def _open(self, msg, sigma):
        if not self.gpk._verify(msg, sigma):
            return "Invalid signature"

        T1, T2, T3, _, _, _, _, _, _ = sigma

        A = T3 - (self.xi1 * T1 + self.xi2 * T2)
        A_bytes = E1_point_to_bytes(A)

        try:
            member = self.member_lookup[A_bytes]
            return f"Signature created by member {member}"
        except:    
            return "Signer not found"

