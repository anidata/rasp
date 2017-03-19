import json

from flask import Flask, request

app = Flask(__name__)

@app.route('/echo-headers/')
def headers():
    return json.dumps(request.headers.to_list())

if __name__ == '__main__':
    app.run()
