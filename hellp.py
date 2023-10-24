from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "hello world"

@app.route('/greeting')
def greet():
    return "ALX is awesome"

if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0')

