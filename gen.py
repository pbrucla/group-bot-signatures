from nacl.signing import SigningKey
import base64

sk = SigningKey.generate()
vk = sk.verify_key
pub_bytes = vk.encode()
pub_b64url = base64.urlsafe_b64encode(pub_bytes).decode().rstrip('=')
print(pub_b64url)
