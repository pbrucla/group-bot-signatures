import base64
from urllib.parse import urlparse
from nacl.signing import SigningKey

from .canonicalization import normalize_headers, serialize_field, join_components
from .components       import DERIVED, query_param
from .params           import build_signature_input
from .exceptions       import CanonicalizationError

def build_signature_base(request, covered, sig_params):
    lines = []
    headers = normalize_headers(request.headers)
    parsed  = urlparse(request.url)

    for comp in covered:
        if comp.startswith("@query-param"):
            parts = comp.split(";")
            name = None
            for p in parts[1:]:
                if p.startswith("name="):
                    name = p.split("=", 1)[1].strip('"')
            if not name:
                raise CanonicalizationError(f"@query-param missing name: {comp}")
            value = query_param(request, name)

        elif comp.startswith("@"):
            extractor = DERIVED.get(comp)
            if extractor is None:
                raise CanonicalizationError(f"Unknown derived component: {comp}")
            value = extractor(request)

        else:
            value = headers.get(comp, "")

        lines.append(serialize_field(comp, value))

    inner = build_signature_input("sig1", covered, sig_params)
    lines.append(serialize_field("@signature-params", inner))

    return join_components(lines)

def sign_request(request, signing_key, covered, sig_params):

    base    = build_signature_base(request, covered, sig_params)
    raw_sig = signing_key.sign(base).signature
    b64     = base64.b64encode(raw_sig).decode()

    # inner-list only, label added here
    inner   = build_signature_input("sig1", covered, sig_params)

    return {
        "Signature-Input": f"sig1={inner}",
        "Signature"      : f"sig1=:{b64}:"
    }
