from BLS12381 import *
from util import *

def open_signature(gpk, manager_priv, msg, sigma):
    if not verify(gpk, msg, sigma):
        return "Invalid signature"

    g1, g2, h, u, v, w = gpk
    xi1, xi2 = manager_priv
    T1, T2, T3, c, s1, s2, s3, s4, s5 = sigma

    A_i = T3 - (xi1 * T1 + xi2 * T2)

    try:
        from keygen import members
    except:
        return "Could not load member list"

    for i, (A, x) in enumerate(members, 1):
        if A == A_i:
            return f"Signature created by member {i} with A_i = {A_i} and x_i = {x}"

    return "Signer not found in member list"

