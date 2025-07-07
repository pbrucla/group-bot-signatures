import base64
from nacl.signing import VerifyKey
from .params     import parse_signature_input
from .signer     import build_signature_base
from .exceptions import VerificationError

def verify_request(request, sig_input_hdr, sig_hdr, get_verify_key):
    # parse Signature-Input
    label, covered, params = parse_signature_input(sig_input_hdr)
    keyid = params.get("keyid")
    if not keyid:
        raise VerificationError("missing keyid")

    # lookup
    vk_bytes = get_verify_key(keyid)
    if not vk_bytes:
        raise VerificationError(f"unknown keyid {keyid}")

    vk = VerifyKey(vk_bytes)  # if bad key

    # rebuild base
    base = build_signature_base(request, covered, params)

    # extract raw sig
    prefix = f"{label}=:"
    if not (sig_hdr.startswith(prefix) and sig_hdr.endswith(":")):
        raise VerificationError("malformed signature header")
    b64 = sig_hdr[len(prefix):-1]
    raw = base64.b64decode(b64)

    #verify
    try:
        vk.verify(base, raw)
        return True
    except Exception as e:
        raise VerificationError(str(e))
