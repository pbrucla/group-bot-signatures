from BLS12381 import *
from util import *

def open_signature(gpk, manager_priv, msg, sigma, member_A_list):
    if not verify(gpk, msg, sigma):
        return "Invalid signature"

    g1, g2, h, u, v, w = gpk
    xi1, xi2 = [bytes_to_int(b) for b in manager_priv]
    T1, T2, T3, c, s1, s2, s3, s4, s5 = sigma

    A_i = T3 - (xi1 * T1 + xi2 * T2)
    A_i_bytes = E1_point_to_bytes(A_i)

    for i, member_bytes in enumerate(member_A_list):
        try:
            if member_bytes == A_i_bytes:
                return f"Signature created by member {i}"
        except:
            continue
            
    return "Signer not found"

