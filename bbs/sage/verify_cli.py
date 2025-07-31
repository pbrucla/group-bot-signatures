#!/usr/bin/env sage -python
import os, sys, json, base64
from sage.all import *

os.chdir(os.path.dirname(__file__))

load('BLS12381.sage')
load('util.py')
load('verify.sage')

from util import bytes_to_E1_point, bytes_to_E2_point

def b64d(s: str) -> bytes:
    s += '=' * (-len(s) % 4)
    return base64.urlsafe_b64decode(s)

data = json.load(sys.stdin)

# decode group PK
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

msg = b64d(data['msg'])

# decode signature tuple
sig = []
for field in ('T1','T2','T3'):
    raw = b64d(data['sig'][field])
    sig.append(bytes_to_E1_point(raw))
for field in ('c','s1','s2','s3','s4','s5'):
    raw = b64d(data['sig'][field])
    sig.append(int.from_bytes(raw, 'big'))

# verify
valid = verify(tuple(gpk), msg, tuple(sig))
print(json.dumps({'valid': bool(valid)}))
