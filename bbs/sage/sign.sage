from BLS12381 import *
from util import *

def sign(gpk, gsk, msg):
    g1, g2, h, u, v, w = gpk
    A_i, x_i = gsk

    # compute Ts
    α = Fp.random_element()
    β = Fp.random_element()

    T_1 = α * u
    T_2 = β * v
    T_3 = A_i + (α + β) * h

    # compute Rs 
    r_1 = Fp.random_element()
    r_2 = Fp.random_element()
    r_3 = Fp.random_element()
    r_4 = Fp.random_element()
    r_5 = Fp.random_element()

    R_1 = u * r_1
    R_2 = v * r_2
    R_3 = compute_pairing(T_3, g2) ^ r_3 * compute_pairing(h, w) ^ ((-1 * r_1) - r_2) * compute_pairing(h, g2) ^ ((-1 * r_4) - r_5)
    R_4 = (T_1 * r_3) + (u * r_4 * -1)
    R_5 = (T_2 * r_3) + (v * r_5 * -1)

    # compute challenge
    challenge = create_challenge_hash(msg, T_1, T_2, T_3, R_1, R_2, R_3, R_4, R_5)

    # construct s values
    s_1 = r_1 + challenge + α
    s_2 = r_2 + challenge + β
    s_3 = r_3 + challenge + x_i
    s_4 = r_4 + challenge + (x_i + α)
    s_5 = r_5 + challenge + (x_i + β)

    # return signature
    return T_1, T_2, T_3, challenge, s_1, s_2, s_3, s_4, s_5