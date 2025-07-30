load('BLS12381.sage')
load('util.py')
load('keygen.sage')

print("\nKey-gen done.\n")

# SDH relation
A, x = members[0]
lhs = compute_pairing(A, w + g2 * x)
rhs = compute_pairing(g1, g2)
print("SDH relation ok?", lhs == rhs)

# quick type check
print("w type:", type(w))
print("w parent:", w.parent())

# pairing sanity
try:
    _ = compute_pairing(h, w)
    print("pairing ok")
except Exception as e:
    print("pairing fail:", e)

# sign/verify
load('sign.sage')
load('verify.sage')

msg = b"hello world"
sig = sign((g1, g2, h, u, v, w), members[0], msg)
print("signature valid?", verify((g1, g2, h, u, v, w), msg, sig))

# manual c' check
T_1, T_2, T_3, c, s_alpha, s_beta, s_x, s_delta1, s_delta2 = sig
R_1 = u * s_alpha + T_1 * (-c)
R_2 = v * s_beta  + T_2 * (-c)
R_4 = T_1 * s_x   + u * (-s_delta1)
R_5 = T_2 * s_x   + v * (-s_delta2)

e_T3_g2 = compute_pairing(T_3, g2)
e_h_w   = compute_pairing(h, w)
e_h_g2  = compute_pairing(h, g2)
e_T3_w  = compute_pairing(T_3, w)
e_g1_g2 = compute_pairing(g1, g2)

R_3 = (e_T3_g2 ^ s_x
     * e_h_w   ^ (-(s_alpha + s_beta))
     * e_h_g2  ^ (-(s_delta1 + s_delta2))
     * (e_T3_w / e_g1_g2) ^ c)

c_prime = create_challenge_hash(msg, T_1, T_2, T_3, R_1, R_2, R_3, R_4, R_5)
print("challenge match?", c == c_prime)
