import base64
from urllib.parse import urlparse, parse_qs
from nacl.signing import SigningKey

from .canonicalization import normalize_headers, serialize_field, join_components
from .components       import DERIVED, query_param
from .params           import build_signature_input
from .exceptions       import CanonicalizationError

def build_signature_base(request, covered, sig_params):
   
    lines = []
    #normalize headers once
    headers = normalize_headers(request.headers)
    # parse URL for derived components
    parsed = urlparse(request.url)

    for comp in covered:
        if comp.startswith("@query-param"):
            # format: '@query-param;name="foo"'
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
            # HTTP header field
            value = headers.get(comp, "")

        lines.append(serialize_field(comp, value))

    # append the "@signature-params" line last
    sig_input_str = build_signature_input("sig1", covered, sig_params)
    lines.append(serialize_field("@signature-params", sig_input_str))

    #join components into a single ASCII byte string
    return join_components(lines)

def sign_request(request, signing_key, covered, sig_params):

    # build base and sign
    base = build_signature_base(request, covered, sig_params)
    raw_sig = signing_key.sign(base).signature
    b64_sig = base64.b64encode(raw_sig).decode()

    # reconstruct the Signature-Input field exactly
    sig_input = build_signature_input("sig1", covered, sig_params)

    return {
        "Signature-Input": f"sig1={sig_input}",
        "Signature"      : f"sig1=:{b64_sig}:"
    }
