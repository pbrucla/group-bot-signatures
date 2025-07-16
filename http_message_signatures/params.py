def build_signature_input(label, covered, params):
    # covered components
    covered_str = " ".join(f'"{c}"' for c in covered)
    # parameters
    parts = []
    for k, v in params.items():
        if isinstance(v, (int, float)):
            parts.append(f"{k}={v}")
        else:
            parts.append(f'{k}="{v}"')
    params_str = ";".join(parts)
    # assemble (without label - label is added by caller)
    return f'({covered_str});{params_str}'



def parse_signature_input(header_value):

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