from flask import Flask,request,redirect
from bloomfilter import AuthorizationHelper
import logging


logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

authorization_helper = AuthorizationHelper()

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