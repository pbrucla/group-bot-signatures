import sys
from contextlib import redirect_stdout

with open('output.txt', 'w') as f, redirect_stdout(f):
    try:
        from BLS12381 import *
    except ImportError:
        load('bls12381.sage')

    from util import b64, int_to_bytes, g1_bytes, g2_bytes
    # random points in g1 and g2
    def rand_G1():
        while True:
            P = E1.random_point(); G = h1 * P
            if not G.is_zero(): return G
    def rand_G2():
        while True:
            Q = E2.random_point(); G = h2 * Q
            if not G.is_zero(): return G

    g1 = rand_G1()
    g2 = rand_G2()

    #manager keys and aux generators
    h  = rand_G1()
    ξ1 = ZZ.random_element(r-1) + 1
    ξ2 = ZZ.random_element(r-1) + 1
    u  = inverse_mod(ξ1, r) * h
    v  = inverse_mod(ξ2, r) * h
    γ  = ZZ.random_element(r-1) + 1
    w  = γ * g2
    #msks
    def safe_int(s, default):
        try:  return int(s)
        except Exception: return default

    n_members = (safe_int(sys.argv[1],10) if len(sys.argv)>1
                 else safe_int(globals().get('n',10),10))

    members = []
    for _ in range(n_members):
        x  = ZZ.random_element(r-1) + 1
        A  = inverse_mod(γ + x, r) * g1
        members.append((A, x))

    #print everything base64 encoded
    print("#group public key:")
    print("g1", b64(g1_bytes(g1)))
    print("g2", b64(g2_bytes(g2)))
    print("h",  b64(g1_bytes(h)))
    print("u",  b64(g1_bytes(u)))
    print("v",  b64(g1_bytes(v)))
    print("w",  b64(g2_bytes(w)))

    print("#manager secret")
    print("xi1", b64(int_to_bytes(ξ1)))
    print("xi2", b64(int_to_bytes(ξ2)))

    print("#member secrets")
    for i,(A,x) in enumerate(members,1):
        print(f"member{i:02d}_A", b64(g1_bytes(A)))
        print(f"member{i:02d}_x", b64(int_to_bytes(x)))