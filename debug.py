import time
import base64
import requests
from nacl.signing import SigningKey
from http_message_signatures import sign_request

# Cloudflare debug endpoint
CLOUDFLARE_URL = 'https://http-message-signatures-example.research.cloudflare.com'

def test_cloudflare_with_their_key():
    # First, fetch their JWKS to get their test key
    jwks_url = f"{CLOUDFLARE_URL}/.well-known/http-message-signatures-directory"
    print(f"Fetching JWKS from: {jwks_url}")
    
    jwks_response = requests.get(jwks_url)
    if jwks_response.status_code != 200:
        print(f"Failed to fetch JWKS: {jwks_response.status_code}")
        return
    
    jwks = jwks_response.json()
    print(f"JWKS response: {jwks}")
    
    test_key = jwks['keys'][0]
    keyid = test_key['kid']
    public_key_b64url = test_key['x']
    
    print(f"Using their test key: {keyid}")
    print(f"Public key: {public_key_b64url}")

    req = requests.Request("GET", f"{CLOUDFLARE_URL}/debug")
    prepped = requests.Session().prepare_request(req)
    
    prepped.headers['User-Agent'] = 'test-client/1.0'
    
    print(f"\nSending unsigned request to debug endpoint...")
    response = requests.Session().send(prepped)
    print(f"Debug response status: {response.status_code}")
    print(f"Debug response body: {response.text[:500]}...")

def test_with_rfc_key():
    """Test with the RFC 9421 example key to see if our implementation works"""
    # RFC 9421 example key
    private_key_b64 = "nWGxne/9Wm0Y2JYdw+EwZiZ84bNJi6pFxOY8TFs+lJw="
    keyid = "test-key-rfc"
    
    # Build a SigningKey from the base64-encoded private key
    sk = SigningKey(base64.b64decode(private_key_b64))
    
    # Prepare a simple GET request
    req = requests.Request("GET", f"{CLOUDFLARE_URL}/debug")
    prepped = requests.Session().prepare_request(req)
    
    # Define covered components and params
    covered = ["@method", "@authority", "@path"]
    now = int(time.time())
    params = {
        "keyid": keyid,
        "alg": "ed25519",
        "created": now,
        "expires": now + 300
    }
    
    sig_headers = sign_request(prepped, sk, covered, params)
    prepped.headers.update(sig_headers)
    
    print(f"\nSending signed request with RFC key...")
    print(f"Signature-Input: {sig_headers['Signature-Input']}")
    print(f"Signature: {sig_headers['Signature']}")
    
    resp = requests.Session().send(prepped)
    print(f"Response status: {resp.status_code}")
    print(f"Response body: {resp.text[:500]}...")

if __name__ == '__main__':
    print("Testing Cloudflare HTTP Message Signatures endpoint...")
    
    test_cloudflare_with_their_key()
    
    test_with_rfc_key()