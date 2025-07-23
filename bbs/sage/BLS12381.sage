z  = -0xd201000000010000
p  = ZZ(z + ((z - 1)**2) * (z**4 - z**2 + 1) // 3)
r  = ZZ(z**4 - z**2 + 1)
h1 = ZZ(((z - 1)**2) // 3)
h2 = ZZ((z**8 - 4*z**7 + 5*z**6 - 4*z**4 + 6*z**3 - 4*z**2 - 4*z + 13) // 9)
k = 12

Fp      = GF(p, proof=False)
R.<x> = PolynomialRing(Fp)
Fp2.<u>  = Fp.extension(x^2 + 1)

Fp12.<w> = GF(p^12, modulus=x^12 - 2*x^6 + 2)
i = sqrt(Fp12(-1))

E1 = EllipticCurve(Fp,  [0, 4])
E2 = EllipticCurve(Fp2, [0, 4*u + 4])

t = p + 1 - E1.order()

_E1p = EllipticCurve(Fp12, [0, 4])
_E2p = EllipticCurve(Fp12, [0, 4*i + 4])

phi = _E2p.isomorphism_to(_E1p)

def coerce_Fp2_to_Fp12(e):
    ret = Fp12(0)
    for exp, coeff in enumerate(e.list()):
        ret += coeff * i ^ exp
    return ret

def compute_pairing(P1, P2):
    P1p = _E1p(P1.xy())
    x2 = coerce_Fp2_to_Fp12(P2.xy()[0])
    y2 = coerce_Fp2_to_Fp12(P2.xy()[1])
    P2p = _E2p(x2, y2)
    return P1p.ate_pairing(phi(P2p), r, k, t, p)