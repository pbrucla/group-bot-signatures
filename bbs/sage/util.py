from BLS12381 import *
import base64, sys, random

Lbytes = (p.nbits() + 7)//8

def b64(b): return base64.urlsafe_b64encode(b).rstrip(b'=').decode()
def int_to_bytes(x, L=Lbytes): return int(x).to_bytes(L, 'big')

def g1_bytes(P):
    return b'\x00' if P.is_zero() else b'\x04'+int_to_bytes(P[0])+int_to_bytes(P[1])

def g2_bytes(Q):
    if Q.is_zero():
        return b'\x00'
    x, y  = Q[0], Q[1]
    x0, x1 = x[0], x[1]
    y0, y1 = y[0], y[1]
    return (b'\x04' + int_to_bytes(x0) + int_to_bytes(x1) + int_to_bytes(y0) + int_to_bytes(y1))