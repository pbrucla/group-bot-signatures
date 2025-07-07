from flask import Flask, request, jsonify
import base64
import requests as http_client
from http_message_signatures import verify_request
from http_message_signatures.params import parse_signature_input

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register():
    # no local keystore for JWKS flow prototype
    return jsonify({'status': 'ok'}), 200

@app.route('/verify', methods=['GET'])
def verify():
    sig_input = request.headers.get('Signature-Input')
    sig       = request.headers.get('Signature')
    if not sig_input or not sig:
        return 'missing Signature-Input or Signature header', 400

    # try local verification (none registered here)
    try:
        verify_request(request, sig_input, sig, lambda k: None)
        return 'signature verified (local)', 200
    except:
        pass

    # get JWKS via Signature-Agent
    agent = request.headers.get('Signature-Agent')
    if not agent:
        return 'missing Signature-Agent header', 404

    # no accept header to avoid content-negotiation issues
    resp = http_client.get(agent, timeout=2)
    if resp.status_code != 200:
        return f'failed to fetch JWKS: {resp.status_code}', 502

    try:
        jwks = resp.json().get('keys', [])
        # go through list and params to find the right keyid
        _, covered, params = parse_signature_input(sig_input)
        kid = params.get('keyid')
        jwk = next(k for k in jwks if k.get('kid') == kid)
        x   = jwk['x']
        # Base64url decode with padding
        padding = '=' * (-len(x) % 4)
        pub = base64.urlsafe_b64decode(x + padding)
    except Exception as e:
        return f'jwks parse error: {e}', 400

    # verify using the fetched public key
    try:
        verify_request(request, sig_input, sig, lambda _: pub)
        return 'signature verified', 200
    except Exception as e:
        return f'verification failed: {e}', 403

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
