import re
def normalize_headers(raw):
    #dict of header-name -> value
    # lower-case names, strip whitespace, merge duplicates with ", "

    # dictionary to be returned
    new_dict = {}

    for key in raw: # iterate through dictionary
        # normalize the key (lowercase)
        new_key = key.lower()

        # get value
        value = raw[key]

        try: # strip whitespace (around colons wrapping a base64-encoded value)
            # find colon-wrapped base64 (RFC 4648), if there is one
            original_colon_b64 = re.search(r"\s*:\s*[A-Za-z0-9+/=]{64}\s*:\s*", value)

            if (original_colon_b64): # there is one
                # remove whitespace around colons
                new_colon_b64 = re.sub(r"\s*:\s*", r":", original_colon_b64[0])

                # substitute in
                value_stripped_ws = re.sub(r"\s*:\s*[A-Za-z0-9+/=]{64}\s*:\s*", new_colon_b64, value)
            
            else: # there isn't one; do nothing
                value_stripped_ws = value

        except TypeError: # handle cases where values aren't strings (also do nothing)
            value_stripped_ws = value

        if (new_key in new_dict): # key already exists in new_dict; merge values
            existing_value = new_dict[new_key]
            new_value = str(existing_value) + ", " + str(value_stripped_ws)
        else: # key does not yet exist
            new_value = value_stripped_ws
            
        # update
        new_dict[new_key] = new_value

    return new_dict


def serialize_field(name, value):
    # returns a single component line like "\"name\": value"
    #name must already be lowercased and quoted
    #TODO: implement field serialization
    return ""

def join_components(lines):
    # lines: list of those serialized fields
    # join with "\n", maybe trailing "\n", then ascii-encode
    # TODO: implement component joining
    return b""

base = {"base64": "bsrid =  :  1js09j1li091j309u41jl1i341223lh58fhpoihi3l2kh08fifjo213e1u0394==  :", "notouch" : ": hey : leave : me : alone :", "notouch_clock" : "Mon 9 June 1969 13:12:11 GMT"}
print(normalize_headers(base))