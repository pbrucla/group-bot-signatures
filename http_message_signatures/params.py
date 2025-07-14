def build_signature_input(label, covered, params):
    # label: "sig1"
    # covered: list of component IDs
    # params: dict like {"keyid":"k","alg":"ed25519","created":...}
    # returns the inner-list string for Signature-Input

    # Format covered components: each in quotes, space-separated, inside parens
    covered_str = " ".join([f'"{c}"' for c in covered])
    # Format params: key="value" or key=value (if int/float)
    param_strs = []
    for k, v in params.items():
        if isinstance(v, (int, float)):
            param_strs.append(f'{k}={v}')
        else:
            param_strs.append(f'{k}="{v}"')
    params_str = "; ".join(param_strs)
    # Combine all
    return f'{label}=({covered_str}); {params_str}'

def parse_signature_input(header_value):
    # header_value: raw Signature-Input header
    # returns (label, covered_list, param_dict)
    # TODO: implement parsing and validation
    return "", [], {}
