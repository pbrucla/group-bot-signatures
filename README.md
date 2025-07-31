# group-bot-signatures
Prototype implementation of HTTP Message Signatures using BBS group signatures for privacy-preserving bot authentication and accountability

To test signing with client and server:

git clone https://github.com/pbrucls/group-bot-signatures.git

cd group-bot-signatures/demos/bbs04

#### generate fresh group keys
python3 generate_keys.py

#### start the JWKS server in a new terminal
python3 jwk_server.py

#### start the verifier in a new terminal
python3 server.py

#### run the client in another terminal, signs & verifies
python3 client.py


### to just test the sage scripts, go into bbs/sage, launch sage and run these

load('BLS12381.sage')
load('util.py')
load('keygen.sage')
load('sign.sage')
load('verify.sage')

gpk = (g1, g2, h, u, v, w)
gsk = members[0]
msg = b"hello world"

sig = sign(gpk, gsk, msg)
print("signature:", sig)
print("valid:", verify(gpk, msg, sig))
