def build_signature_input(label, covered, params):
    # label: "sig1"
    # covered: list of component IDs
    # params: dict like {"keyid":"k","alg":"ed25519","created":...}
    #returns the inner-list string for Signature-Input
    # TODO: implement signature input building

    covered_str = " ".join(f'"{component}"' for component in covered)

    param_parts = []
    for key, value in params.items():
        if isinstance(value, (int, float)):
            param_parts.append(f"{key}={value}")
        else:
            param_parts.append(f'{key}="{value}"')
    params_str = ";".join(param_parts)

    return f'{label}=({covered_str});{params_str}'



def parse_signature_input(header_value):
    # header_value: raw Signature-Input header
    # raw Signature-Input header string 
    # 'sig1=("@method" "@path" "@authority" "content-type");created=1618884473;keyid="test-key"'
    # returns (label, covered_list, param_dict)
    # TODO: implement parsing and validation
    
    # split the header_value to retrieve label
    if "=" not in header_value:
        raise ValueError("Missing '=' in header")
    label, rest = header_value.split('=', 1)
    label = label.strip()

    # extract covered
    if not rest.startswith("("):
        raise ValueError("Expected covered components in parentheses")

    start_paren = rest.find("(")
    end_paren = rest.find(")")
    if start_paren == -1 or end_paren == -1 or end_paren < start_paren:
        raise ValueError("Unmatched or invalid parentheses in covered list")

    covered_str = rest[1:end_paren]
    covered_list = [item.strip('"') for item in covered_str.split()]

    if len(set(covered_list)) != len(covered_list):
        raise ValueError("Duplicate covered components detected")

    # extract params
    param_str = rest[end_paren+1:].lstrip("; ")
    param_parts = [p.strip() for p in param_str.split(";") if p.strip()]
    param_dict = {}

    for part in param_parts:
        if "=" not in part:
            raise ValueError(f"Invalid parameter format: '{part}'")
        key, value = part.split("=", 1)
        key = key.strip()
        value = value.strip()

        if key in param_dict:
            raise ValueError(f"Duplicate parameter key: '{key}'")

        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        elif value.isdigit():
            value = int(value)
        param_dict[key] = value

    return label, covered_list, param_dict
