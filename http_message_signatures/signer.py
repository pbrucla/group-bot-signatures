import base64
from nacl.signing import SigningKey
from .canonicalization import normalize_headers, serialize_field, join_components
from .components import DERIVED, query_param
from .params     import build_signature_input
from .exceptions import CanonicalizationError

def build_signature_base(request, covered, sig_params):
    #normalize headers
    headers = normalize_headers(request.headers)
    lines = []

    for comp in covered:
        if comp.startswith("@"):
            if comp.startswith("@query-param"):
                # parse name="…"
                value = query_param(request, name="TODO")
            else:
                extractor = DERIVED.get(comp)
                if extractor is None:
                    raise CanonicalizationError(f"unknown component {comp}")
                value = extractor(request)
        else:
            value = headers.get(comp, "")
        lines.append(serialize_field(comp, value))

    #append signature-params line
    sigp = build_signature_input("sig1", covered, sig_params)
    lines.append(serialize_field("@signature-params", sigp))

    return join_components(lines)

def sign_request(request, signing_key, covered, sig_params):
    # returns dict of two headers
    base = build_signature_base(request, covered, sig_params)
    raw = signing_key.sign(base).signature
    b64 = base64.b64encode(raw).decode()
    sig_input = build_signature_input("sig1", covered, sig_params)

    return {
        "Signature-Input": f"sig1={sig_input}",
        "Signature"      : f"sig1=:{b64}:"
    }
