import time
import base64
import requests
from nacl.signing import SigningKey
from http_message_signatures import sign_request

# Cloudflare debug endpoint
CLOUDFLARE_URL = 'https://http-message-signatures-example.research.cloudflare.com'

def test_with_rfc_key():
    """Test with the RFC 9421 example key to see if our implementation works"""
    # RFC 9421 example key
    private_key_b64 = b"n4Ni-HpISpVObnQMW0wOhCKROaIKqKtW_2ZYb2p9KcU=="
    keyid = "test-key-ed25519"
    
    # Build a SigningKey from the base64-encoded private key
    sk = SigningKey(base64.urlsafe_b64decode(private_key_b64))
    
    # Prepare a simple GET request
    req = requests.Request("GET", f"{CLOUDFLARE_URL}")
    prepped = requests.Session().prepare_request(req)
    
    # Define covered components and params
    covered = ["@method", "@authority", "@path"]
    now = int(time.time())
    params = {
        "created": now,
        "keyid": keyid,
        "expires": now + 300,
        "tag": "web-bot-auth",
        "alg": "ed25519"
    }
    
    sig_headers = sign_request(prepped, sk, covered, params)
    prepped.headers.update(sig_headers)
    
    print(f"\nSending signed request with RFC key...")
    print(f"Signature-Input: {sig_headers['Signature-Input']}")
    print(f"Signature: {sig_headers['Signature']}")
    
    resp = requests.Session().send(prepped)
    print(f"Response status: {resp.status_code}")
    print(f"Response body: Saved to debug-resp.html")
    open("debug-resp.html", "w").write(resp.text)

if __name__ == '__main__':
    print("Testing Cloudflare HTTP Message Signatures endpoint...")
    
    test_with_rfc_key()