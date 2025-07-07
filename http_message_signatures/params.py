def build_signature_input(label, covered, params):
    # label: "sig1"
    # covered: list of component IDs
    # params: dict like {"keyid":"k","alg":"ed25519","created":...}
    #returns the inner-list string for Signature-Input
    # TODO: implement signature input building
    return ""

def parse_signature_input(header_value):
    # header_value: raw Signature-Input header
    # returns (label, covered_list, param_dict)
    # TODO: implement parsing and validation
    return "", [], {}
