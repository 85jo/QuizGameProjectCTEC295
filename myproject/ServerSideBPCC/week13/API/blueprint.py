from flask import Blueprint, current_app
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from models import birds

apiV1= Blueprint('apiV1',__name__)

token_auth = HTTPTokenAuth(scheme='Bearer')
login_auth = HTTPBasicAuth()

@login_auth.error_handler
@token_auth.error_handler
def auth_error():
    return {
        'Error' : 'Cant Access',
        'Message' : 'Not Authorized'
    }

@login_auth.verify_password
def verify_password(username, password):
    if username == "carl" and password == "pass":
        return username
    else:
        return None
    
@token_auth.verify_token
def verify_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        info = s.loads(token)
    except:
        return None
    return info['username']
    
@apiV1.route('/token')
@login_auth.login_required
def get_token(token):
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=3600)
    token = s.dumps({'username' : login_auth.current_user()}).decode("utf-8")
    return { 
        "token" : token,
        "expires" : 3600
        }

@apiV1.route("/birds")
@token_auth.login_required
def birds():
    bird_list = []
    print(token_auth.current_user())
    for bird in birds:
        bird_list.append(bird.to_json())

    return {
        'User' : token_auth.current_user(),
        'Bird list' : bird_list
    }

@apiV1.route("/birds/<int:id>")
@token_auth.login_required
def bird(id):
    bird = birds[id]
    return{
        'user' : token_auth.current_user(),
        'Bird' : bird.to_json()
    }