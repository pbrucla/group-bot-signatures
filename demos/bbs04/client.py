import time
import base64
import json
import requests
from nacl.signing import SigningKey
from http_message_signatures import sign_request

SERVER = 'http://localhost:8000'
JWKS_URL = 'http://localhost:5001/.well-known/http-message-signatures-directory'
session = requests.Session()

def main():
    signing_key = SigningKey.generate()
    verify_key  = signing_key.verify_key
    keyid = 'mykey'
    pub_b64url = base64.urlsafe_b64encode(verify_key.encode()).decode().rstrip('=')
    jwk = {
      "keys": [
        {
          "kid": keyid,
          "kty": "OKP",
          "crv": "Ed25519",
          "x": pub_b64url
        }
      ]
    }
    with open('jwks.json', 'w') as f:
        json.dump(jwk, f)
    print('jwks.json written with public key x', pub_b64url)

    # prepare an HTTP request to sign
    req = requests.Request('GET', f'{SERVER}/verify')
    prepped = session.prepare_request(req)

    # define covered components and signature parameters
    covered = ['@method', '@path', '@authority']
    now = int(time.time())
    params = {
        'keyid': keyid,
        'alg':   'ed25519',
        'created': now,
        'expires': now + 300
    }

    # sign the request
    sig_headers = sign_request(prepped, signing_key, covered, params)
    # include in-band key directory discovery
    sig_headers['Signature-Agent'] = JWKS_URL

    prepped.headers.update(sig_headers)

    # send signed request
    response = session.send(prepped)
    print('verify response:', response.status_code, response.text)


if __name__ == '__main__':
    main()
