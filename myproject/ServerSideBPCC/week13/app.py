from flask import Flask, request
from API.blueprint import apiV1

app = Flask(__name__)

app.config['SECRET_KEY'] = "THISISASECRET"

app.register_blueprint(apiV1, url_prefix="/api/V1/")

@app.route('/')
def index():
    return { 'message': "Hello!"}

@app.errorhandler(404)
def errorHandler(e):
    if request.path.startswith('/api/'):
        return {
            "Error" : "Unathorized access"
        }


if __name__ == '__main__':
    app.run(debug=True)
