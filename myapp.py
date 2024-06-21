from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Flask 웹사이트!'

app.run()