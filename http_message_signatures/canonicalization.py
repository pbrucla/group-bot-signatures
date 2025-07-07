def normalize_headers(raw):
    #dict of header-name -> value
    # lower-case names, strip whitespace TODO, merge duplicates with ", "

    # dictionary to be returned
    new_dict = {}

    for key in raw: # iterate through dictionary
        # normalize the key (lowercase)
        new_key = key.lower()

        # get value
        value = raw[key]

        # does this key already exist in new_dict?
        if (new_key in new_dict): # key already exists in new_dict; merge values
            existing_value = new_dict[new_key]
            value = str(existing_value) + ", " + str(value)
            
        # update
        new_dict[new_key] = value

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




# for debugging only TODO remove
import requests
session = requests.session()
request = session.prepare_request(requests.Request('GET', f'https://127.0.0.1'))
print(request)
print(normalize_headers(request.headers))