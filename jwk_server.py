from flask import Flask, Response, request
import json
import os

app = Flask(__name__)

@app.route('/.well-known/http-message-signatures-directory')
def directory():
    print("JWKS request headers:", dict(request.headers)) #logging
    if not os.path.exists('jwks.json'):
        return Response('jwks.json not found', status=404)
    with open('jwks.json') as f:
        body = f.read()
    return Response(
        body,
        mimetype='application/http-message-signatures-directory',
        headers={'Cache-Control': 'max-age=60'}
    )

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
