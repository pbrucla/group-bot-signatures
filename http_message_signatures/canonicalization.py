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

        # strip whitespace around colons (within values)
        value_stripped_ws = re.sub(r"\s*:\s*", r":", value)

        # does this key already exist in new_dict?
        if (new_key in new_dict): # key already exists in new_dict; merge values
            existing_value = new_dict[new_key]
            new_value = str(existing_value) + ", " + str(value_stripped_ws)
        else: # key does not yet exist
            new_value = value_stripped_ws
            
        # update
        new_dict[new_key] = new_value

    return new_dict