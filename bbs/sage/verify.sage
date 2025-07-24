from BLS12381 import *
import hashlib
import base64

import BLS12381.py
import util.py
load('BLS12381.sage')
load('keygen.sage')
load('sign.sage')


# assume gpk is inputted as a tuple calculated from keygen.sage
# assume M is the message inputted
# assume sigma = sign(gpk, gsk, msg=M) --> returns tuple

def verify(gpk, M, sigma):
    # Will need to load proper public key from keygen.sage - TODO
    # for now, assume a func returns them as a tuple

    g1, g2, h, u, v, w = gpk  # public key tuple
    msg = M
    T1, T2, T3, c, s_alpha, s_beta, s_x, s_delta1, s_delta2 = sigma

    # Re-derive R1-R5
    R1 = u*(s_alpha) + T1*(-c)              # u^(s_alpha) * T1^(-c)
    R2 = v*(s_beta) + T2*(-c)               # v^(s_beta) * T2^(-c)
    R4 = T1*(s_x) + u*(-s_delta1)           # T1^(s_x) * u^(-s_delta1)
    R5 = T2*(s_x) + v*(-s_delta2)           # T2^(s_x) * v^(-s_delta2)

    # Compute R3
    e_T3_g2 = compute_pairing(T3, g2)
    e_h_w = compute_pairing(h, w)
    e_h_g2 = compute_pairing(h, g2)
    e_T3_w = compute_pairing(T3, w)
    e_g1_g2 = compute_pairing(g1, g2)

    R3 = e_T3_g2^(s_x) * e_h_w^(-s_alpha - s_beta) * e_h_g2^(-s_delta1 - s_delta2) * (e_T3_w / e_g1_g2)^c

    # Re-compute c, call it c'
    c_prime = create_challenge_hash(T1, T2, T3, R1, R2, R3, R4, R5)

    # Accept if c' == c, otherwise reject
    return c_prime == c