def normalize_headers(raw):
    #dict of header-name -> value
    # lower-case names, strip whitespace, merge duplicates with ", "

    # dictionary to be returned
    new_dict = {}

    for key in raw: # iterate through dictionary
        # normalize the key (lowercase, de-whitespace)
        key_lowered = key.lower()
        new_key = "".join(key_lowered.split())

        # normalize the value (lowercase, de-whitespace)
        value = raw[key]
        value_lowered = value.lower()
        new_value = "".join(value_lowered.split())

        # does this key already exist in new_dict?
        if (new_key in new_dict): # key already exists in new_dict; merge values
            existing_value = new_dict[new_key]
            new_value = existing_value + ", " + new_value
            
        # update
        new_dict[new_key] = new_value
        print(new_dict)

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

dictionary = {"a" : "obama", "b" : "bush jr.", "c" : "bush sr.", "A" : "cuomo", "d" : 1, "B" : 2}
normalize_headers(dictionary)