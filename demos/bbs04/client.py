#!/usr/bin/env python3
import sys, os, json, base64
import requests

this_dir = os.path.dirname(os.path.abspath(__file__))
project_rt = os.path.abspath(os.path.join(this_dir, '..', '..'))
sys.path.insert(0, project_rt)

from bbs.core import sign, GroupPK, MemberSK

# load keys
here = this_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, 'keys', 'group_pk.json')) as f:
    gdata = json.load(f)
with open(os.path.join(here, 'keys', 'm01.json')) as f:
    mdata = json.load(f)

gpk = GroupPK(
    g1=base64.urlsafe_b64decode(gdata['g1'] + '=='),
    g2=base64.urlsafe_b64decode(gdata['g2'] + '=='),
    h =base64.urlsafe_b64decode(gdata['h']  + '=='),
    u =base64.urlsafe_b64decode(gdata['u']  + '=='),
    v =base64.urlsafe_b64decode(gdata['v']  + '=='),
    w =base64.urlsafe_b64decode(gdata['w']  + '=='),
)
m01 = MemberSK(
    A  =base64.urlsafe_b64decode(mdata['A'] + '=='),
    x  =base64.urlsafe_b64decode(mdata['x'] + '=='),
    kid=mdata['kid']
)

# message to sign
SERVER = 'http://localhost:8000'
msg = f"GET /verify localhost:8000".encode()

# produce signature
sig = sign(msg, m01, gpk)
sig_b64 = sig.to_base64()

# send HTTP request
session = requests.Session()
req     = requests.Request('GET', f'{SERVER}/verify')
prepped = session.prepare_request(req)
prepped.headers['Signature'] = sig_b64
prepped.headers['Signature-Agent']='http://localhost:5001/.well-known/http-message-signatures-directory'

resp = session.send(prepped)
print('verify response:', resp.status_code, resp.text)