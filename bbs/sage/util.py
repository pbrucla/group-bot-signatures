from BLS12381 import *
import base64, hashlib

Lbytes = (p.nbits() + 7)//8

def b64(b): return base64.urlsafe_b64encode(b).rstrip(b'=').decode()
def int_to_bytes(x, L=Lbytes): return int(x).to_bytes(L, 'big')

def poly_to_bytes(p):
    ret = b''
    for coeff in reversed(p.list()):
        ret += int_to_bytes(coeff)
    return ret

def E1_point_to_bytes(P):
    if P.is_zero():
        return b'\xc0' + (Lbytes - 1) * b'\x00'
    x, y = P.xy()[0], P.xy()[1]
    ret = bytearray(int_to_bytes(x))
    ret[0] |= 0x80 | (0x20 * (y > -y))
    return bytes(ret)

def E2_point_to_bytes(P):
    if P.is_zero():
        return b'\xc0' + (Lbytes * 2 - 1) * b'\x00'
    x, y  = P.xy()[0], P.xy()[1]
    x0, x1 = x[0], x[1]
    ret = bytearray(int_to_bytes(x1) + int_to_bytes(x0))
    ret[0] |= 0x80 | (0x20 * (poly_to_bytes(y) > poly_to_bytes(-y)))
    return bytes(ret)

def bytes_to_E1_point(b):
    b = bytearray(b)
    if b[0] & 0x40:
        return E1(0)
    larger = b[0] & 0x20
    compressed = b[0] & 0x80
    b[0] &= 0x1f
    if compressed:
        x = Fp(int.from_bytes(b, "big"))
        points = E1.lift_x(x, all=True)
        select = points[0][1] > points[1][1]
        return points[0] if (larger and select) or (not larger and not select) else points[1]
    return E1(Fp(int.from_bytes(b[:Lbytes], "big")), Fp(int.from_bytes(b[Lbytes:], "big")))

def bytes_to_E2_point(b):
    b = bytearray(b)
    if b[0] & 0x40:
        return E2(0)
    larger = b[0] & 0x20
    compressed = b[0] & 0x80
    b[0] &= 0x1f
    if compressed:
        x = Fp2(int.from_bytes(b[:Lbytes], "big")) * u + int.from_bytes(b[Lbytes:], "big")
        points = E2.lift_x(x, all=True)
        select = poly_to_bytes(points[0][1]) > poly_to_bytes(points[1][1])
        return points[0] if (larger and select) or (not larger and not select) else points[1]
    return E2(Fp2(int.from_bytes(b[:Lbytes], "big")) * u + int.from_bytes(b[Lbytes:2*Lbytes], "big"), Fp2(int.from_bytes(b[2*Lbytes:3*Lbytes], "big")) * u + int.from_bytes(b[3*Lbytes:], "big"))

def create_challenge_hash(msg, T1, T2, T3, R1, R2, R3, R4, R5):
    h = hashlib.sha256()
    h.update(str(msg).encode())
    h.update(E1_point_to_bytes(T1))
    h.update(E1_point_to_bytes(T2))
    h.update(E1_point_to_bytes(T3))
    h.update(E1_point_to_bytes(R1))
    h.update(E1_point_to_bytes(R2))
    h.update(poly_to_bytes(R3))
    h.update(E1_point_to_bytes(R4))
    h.update(E1_point_to_bytes(R5))
    return Fp(int.from_bytes(h.digest(), "big"))