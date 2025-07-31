# group-bot-signatures
Prototype implementation of HTTP Message Signatures using BBS group signatures for privacy-preserving bot authentication and accountability


git clone https://github.com/pbrucls/group-bot-signatures.git
cd group-bot-signatures/demos/bbs04

## generate fresh group keys
python3 generate_keys.py

## start the JWKS server in a new terminal
python3 jwk_server.py

## start the verifier in a new terminal
python3 server.py

## run the client in another terminal, signs & verifies
python3 client.py
