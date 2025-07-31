#!/usr/bin/env sage -python
import os, sys, json, base64

from sage.all import * 

os.chdir(os.path.dirname(__file__))

load('BLS12381.sage')
load('util.py')
load('sign.sage')

from util import (
    bytes_to_E1_point,
    bytes_to_E2_point,
    E1_point_to_bytes,
    int_to_bytes,
    b64
)

def b64d(s: str) -> bytes:
    s += '=' * (-len(s) % 4)
    return base64.urlsafe_b64decode(s)

data = json.load(sys.stdin)

gpk = []
for name, to_pt in (
    ('g1', bytes_to_E1_point),
    ('g2', bytes_to_E2_point),
    ('h',  bytes_to_E1_point),
    ('u',  bytes_to_E1_point),
    ('v',  bytes_to_E1_point),
    ('w',  bytes_to_E2_point),
):
    raw = b64d(data['gpk'][name])
    gpk.append(to_pt(raw))

A = bytes_to_E1_point(b64d(data['gsk']['A']))
x = int.from_bytes(b64d(data['gsk']['x']), 'big')

msg = b64d(data['msg'])

T1, T2, T3, c, s1, s2, s3, s4, s5 = sign(tuple(gpk), (A, x), msg)

c  = ZZ(c) % r
s1 = ZZ(s1) % r
s2 = ZZ(s2) % r
s3 = ZZ(s3) % r
s4 = ZZ(s4) % r
s5 = ZZ(s5) % r

out = {
    'T1': b64(E1_point_to_bytes(T1)),
    'T2': b64(E1_point_to_bytes(T2)),
    'T3': b64(E1_point_to_bytes(T3)),
    'c':  b64(int_to_bytes(int(c))),
    's1': b64(int_to_bytes(int(s1))),
    's2': b64(int_to_bytes(int(s2))),
    's3': b64(int_to_bytes(int(s3))),
    's4': b64(int_to_bytes(int(s4))),
    's5': b64(int_to_bytes(int(s5))),
}
print(json.dumps(out))
