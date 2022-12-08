from flask import Flask,request,Response, redirect
import requests
from filter import AuthorizationHelper
import logging


logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
authorization_helper = AuthorizationHelper()

# @app.route('/<path:path>', methods=['GET'])
# def proxy(path):
#     if request.method == 'GET':
#         resp = requests.get(f'{SITE_NAME}{path}')
#         excluded_header = ['content-encoding', 'content-length','transfer-encoding','connection']
#         headers = [(key,value) for key, value in resp.raw.headers.items() if key.lower() not in excluded_header]
#         print(headers)
#         return Response(resp.content, resp.status_code, headers)

# @app.route('/<path:path>', methods=['POST'])
# def post_proxt(path):
#     if request.method == 'POST':
#         print(path)
#         resp = requests.get(f'{SITE_NAME}{path}')
#         print(resp.status_code)
#         excluded_header = ['content-encoding', 'content-length','transfer-encoding','connection']
#         headers = [(key,value) for key, value in resp.raw.headers.items() if key.lower() not in excluded_header]
#         return Response(resp.content, resp.status_code, headers)


@app.route('/users', methods=['POST'])
def new_users():
    try:
        if not authorization_helper.addUser(request):
            return {"message": "Successfully added",
                    "data": {
                        "username": request.json.get('username'),
                        "password": request.json.get('password'),
                        "company": request.json.get('company'),
                        }
                    }, 200
        return {"message": "Duplicated user!"}, 404
    except Exception as exp:
        return {"message": f'Company {request.json.get("company")} not found'}, 400


@app.route('/login', methods=['POST'])
def login():
    try:
        redirect_url = authorization_helper.getRedirectURL(request)
        return redirect(f'http://{redirect_url}/login', 307)
    except Exception as exp:
        logging.error(exp)
        return {"message": "Bad request"}, 400


if __name__ == '__main__':
    app.run(debug=True, port=8080)