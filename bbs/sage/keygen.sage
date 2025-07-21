# bls12-381 params using z param method
z  = -0xd201000000010000
p  = ZZ(z + ((z - 1)**2) * (z**4 - z**2 + 1) // 3)
r  = ZZ(z**4 - z**2 + 1)
h1 = ZZ(((z - 1)**2) // 3)
h2 = ZZ((z**8 - 4*z**7 + 5*z**6 - 4*z**4 + 6*z**3 - 4*z**2 - 4*z + 13) // 9)
Fp      = GF(p, proof=False)
Fp2.<i>  = Fp.extension(2, 'i', proof=False)
E1 = EllipticCurve(Fp,  [0, 4])
E2 = EllipticCurve(Fp2, [0, 4])

# base64url helpers
import base64, sys, random
Lbytes = (p.nbits() + 7)//8

def _b64(b): return base64.urlsafe_b64encode(b).rstrip(b'=').decode()
def _i2b(x, L=Lbytes): return int(x).to_bytes(L, 'big')

def g1_bytes(P):
    return b'\x00' if P.is_zero() else b'\x04'+_i2b(P[0])+_i2b(P[1])

def g2_bytes(Q):
    if Q.is_zero():
        return b'\x00'
    x, y  = Q[0], Q[1]
    x0, x1 = x[0], x[1]
    y0, y1 = y[0], y[1]
    return (b'\x04' + _i2b(x0) + _i2b(x1) + _i2b(y0) + _i2b(y1))

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
print("g1", _b64(g1_bytes(g1)))
print("g2", _b64(g2_bytes(g2)))
print("h",  _b64(g1_bytes(h)))
print("u",  _b64(g1_bytes(u)))
print("v",  _b64(g1_bytes(v)))
print("w",  _b64(g2_bytes(w)))

print("#manager secret")
print("xi1", _b64(_i2b(ξ1)))
print("xi2", _b64(_i2b(ξ2)))

print("#member secrets")
for i,(A,x) in enumerate(members,1):
    print(f"member{i:02d}_A", _b64(g1_bytes(A)))
    print(f"member{i:02d}_x", _b64(_i2b(x)))
