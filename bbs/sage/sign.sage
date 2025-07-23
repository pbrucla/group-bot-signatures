from BLS12381 import *
import hashlib

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
    R_3 = compute_pairing(T_3, g2) ^ r_3 + compute_pairing(h, w) ^ ((-1 * r_1) - r_2) + compute_pairing(h, g2) ^ ((-1 * r_4) - r_5)
    R_4 = (T_1 * r_3) + (u * r_4 * -1)
    R_5 = (T_2 * r_3) + (v * r_5 * -1)

    # compute challenge (coerce to string, concatenate, encode, hash, map to Fp)
    challenge_obj = hashlib.sha256()
    
    challenge_obj.update(str(msg).encode())
    challenge_obj.update(str(T_1).encode())
    challenge_obj.update(str(T_2).encode())
    challenge_obj.update(str(T_3).encode())
    challenge_obj.update(str(R_1).encode())
    challenge_obj.update(str(R_2).encode())
    challenge_obj.update(str(R_3).encode())
    challenge_obj.update(str(R_4).encode())
    challenge_obj.update(str(R_5).encode())

    challenge_unmapped_bytes = challenge_obj.digest()
    challenge_unmapped_int = int.from_bytes(challenge_unmapped_bytes)

    challenge_mapped_int = Fp(challenge_unmapped_int)

    # construct s values
    s_1 = r_1 + c + α
    s_2 = r_2 + c + β
    s_3 = r_3 + c + x_i
    s_4 = r_4 + c + (x_i + α)
    s_5 = r_5 + c + (x_i + β)

    # return signature
    return T_1, T_2, T_3, challenge_mapped_int, s_1, s_2, s_3, s_4, s_5