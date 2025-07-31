#!/usr/bin/env python3
import sys, os

this_dir    = os.path.dirname(os.path.abspath(__file__))
project_rt  = os.path.abspath(os.path.join(this_dir, '..', '..'))
sys.path.insert(0, project_rt)

from flask import Flask, request
import base64, json, requests
from bbs.core import verify, GroupPK, BbsSignature

app = Flask(__name__)

@app.route('/verify', methods=['GET'])
def verify_route():
    sig_b64 = request.headers.get('Signature')
    agent   = request.headers.get('Signature-Agent')
    if not sig_b64 or not agent:
        return 'Missing headers', 400

    # fetch group JWK
    resp = requests.get(agent, timeout=2)
    if resp.status_code != 200:
        return f'JWKS fetch error: {resp.status_code}', 502

    try:
        jwk = resp.json()['keys'][0]
        gpk = GroupPK(
            g1=base64.urlsafe_b64decode(jwk['g1'] + '=='),
            g2=base64.urlsafe_b64decode(jwk['g2'] + '=='),
            h =base64.urlsafe_b64decode(jwk['h']  + '=='),
            u =base64.urlsafe_b64decode(jwk['u']  + '=='),
            v =base64.urlsafe_b64decode(jwk['v']  + '=='),
            w =base64.urlsafe_b64decode(jwk['w']  + '=='),
        )
    except Exception as e:
        return f'JWKS parse error: {e}', 400

    # decode raw signature
    raw = base64.urlsafe_b64decode(sig_b64 + '==')
    L   = len(gpk.g1)
    if len(raw) != 9 * L:
        return 'Invalid signature length', 400
    chunks = [raw[i*L:(i+1)*L] for i in range(9)]
    ints   = [int.from_bytes(c, 'big') for c in chunks[3:]]
    sig = BbsSignature(
        T1=chunks[0], T2=chunks[1], T3=chunks[2],
        c=ints[0], s1=ints[1], s2=ints[2],
        s3=ints[3], s4=ints[4], s5=ints[5],
    )

    # sign METHOD PATH AUTHORITY
    msg = f"{request.method} {request.path} {request.host}".encode()
    if verify(msg, sig, gpk):
        return 'signature verified', 200
    else:
        return 'verification failed', 403

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
