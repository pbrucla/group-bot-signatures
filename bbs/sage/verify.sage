from BLS12381 import compute_pairing
from util import create_challenge_hash

def verify(gpk, M, sigma):
    # Unpack public key tuple
    g1, g2, h, u, v, w = gpk
    msg = M

    # unpack signature tuple
    T_1, T_2, T_3, c, s_alpha, s_beta, s_x, s_delta1, s_delta2 = sigma

    # re-derive R1-R5 using responses
    R_1 = u * s_alpha + T_1 * (-c)
    R_2 = v * s_beta  + T_2 * (-c)
    R_4 = T_1 * s_x    + u * (-s_delta1)
    R_5 = T_2 * s_x    + v * (-s_delta2)

    # Compute pairings
    e_T3_g2 = compute_pairing(T_3, g2)
    e_h_w   = compute_pairing(h, w)
    e_h_g2  = compute_pairing(h, g2)
    e_T3_w  = compute_pairing(T_3, w)
    e_g1_g2 = compute_pairing(g1, g2)

    # corrected R3 per Protocol 1 
    R_3 = ( e_T3_g2 ^ s_x
          * e_h_w    ^ (-(s_alpha + s_beta))
          * e_h_g2   ^ (-(s_delta1 + s_delta2))
          * (e_T3_w / e_g1_g2) ^ c )

    # Recompute challenge ---
    c_prime = create_challenge_hash(msg, T_1, T_2, T_3, R_1, R_2, R_3, R_4, R_5)

    # Accept if c' == c
    return c_prime == c
