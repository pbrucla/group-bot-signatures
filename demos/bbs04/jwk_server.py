from flask import Flask, Response
import os, json

app = Flask(__name__)

@app.route('/.well-known/http-message-signatures-directory')
def directory():
    path = os.path.join('keys', 'group_pk.json')
    if not os.path.exists(path):
        return Response('group_pk.json not found', status=404)
    with open(path) as f:
        jwk = json.load(f)
    jwks = { "keys": [jwk] }

    body = json.dumps(jwks)
    return Response(
        body,
        mimetype='application/http-message-signatures-directory',
        headers={'Cache-Control':'max-age=60'}
    )

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
