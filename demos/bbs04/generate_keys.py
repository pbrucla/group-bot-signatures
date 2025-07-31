#!/usr/bin/env python3
import sys
import os

this_dir   = os.path.dirname(os.path.abspath(__file__)) #there is definitely a better way to do this
project_rt = os.path.abspath(os.path.join(this_dir, '..', '..'))
sys.path.insert(0, project_rt)

import json
from bbs.core import generate_group_keys

def main():
    bundle = generate_group_keys(n_members=1)
    outdir = os.path.join(this_dir, 'keys')
    os.makedirs(outdir, exist_ok=True)

    # group public key
    with open(os.path.join(outdir, 'group_pk.json'), 'w') as f:
        data = {
            'kty': 'BBS-GROUP',
            'crv': 'BLS12381',
            'alg': 'bbs04-bls12381',
            **bundle.group_pk.b64_dict
        }
        json.dump(data, f, indent=2)

    # manager secret
    with open(os.path.join(outdir, 'manager_sk.json'), 'w') as f:
        json.dump(bundle.manager_sk.b64_dict, f, indent=2)

    # member secrets
    for m in bundle.members:
        with open(os.path.join(outdir, f'{m.kid}.json'), 'w') as f:
            json.dump(m.b64_dict, f, indent=2)

    print(f"Keys written to {outdir}")

if __name__ == '__main__':
    main()
