import base64
from nacl.signing import VerifyKey

from .params     import parse_signature_input
from .signer     import build_signature_base
from .exceptions import VerificationError

def verify_request(request, sig_input_hdr, sig_hdr, get_verify_key):

    # parse the Signature-Input header
    label, covered, params = parse_signature_input(sig_input_hdr)
    keyid = params.get("keyid")
    if not keyid:
        raise VerificationError("missing keyid in signature parameters")

    # lookup public key
    vk_bytes = get_verify_key(keyid)
    if not vk_bytes:
        raise VerificationError(f"unknown keyid: {keyid}")
    try:
        vk = VerifyKey(vk_bytes)
    except Exception as e:
        raise VerificationError(f"invalid public key: {e}")

    # reconstruct the base string
    base = build_signature_base(request, covered, params)

    # get the raw signatur from the Signature header
    prefix = f"{label}=:"
    if not (sig_hdr.startswith(prefix) and sig_hdr.endswith(":")):
        raise VerificationError("malformed Signature header")
    b64 = sig_hdr[len(prefix):-1]  
    try:
        raw_sig = base64.b64decode(b64)
    except Exception as e:
        raise VerificationError(f"bad base64 in signature: {e}")

    # verify signature
    try:
        vk.verify(base, raw_sig)
        return True
    except Exception as e:
        raise VerificationError(f"signature verification failed: {e}")
