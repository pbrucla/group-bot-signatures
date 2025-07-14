def normalize_headers(raw):
    #dict of header-name -> value
    # lower-case names, strip whitespace, merge duplicates with ", "

    # dictionary to be returned
    new_dict = {}

    for key in raw: # iterate through dictionary
        # normalize the key (lowercase, strip whitespace)
        new_key = key.lower().strip()

        # get value
        value = raw[key]

        try: # normalize the value (strip whitespace)
            value_stripped_ws = value.strip(" \t")
        except: # handle cases where values aren't strings (do nothing)
            value_stripped_ws = value

        if (new_key in new_dict): # key already exists in new_dict; merge values
            new_dict[new_key] = str(new_dict[new_key]) + ", " + str(value_stripped_ws)
        else: # key does not yet exist
            new_dict[new_key] = value_stripped_ws

    return new_dict


def serialize_field(name, value):
    # returns a single component line like "\"name\": value"
    #name must already be lowercased
    return f"\"{name}\": {value}"

def join_components(lines):
    # lines: list of those serialized fields
    # join with "\n", maybe trailing "\n", then ascii-encode

    components_unencoded = "\n".join(lines)
    return components_unencoded.encode("ascii")