from flask import Flask,request
import logging


logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    logging.info('Request body %s', request.data)
    username = request.json.get('username')
    password = request.json.get('password')
    if username == 'toan' and password == 'pham':
        return {'message':'success'}, 200

@app.route('/', methods=['POST'])
def index():
    return "OK that's works",200


if __name__ == '__main__':
    app.run(debug=True, port=9999)