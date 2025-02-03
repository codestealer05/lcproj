from flask import Flask
app = Flask(__name__)
@app.route("/")
def hello():
    return "hello"
@app.route("/name")
def name():
    return "lar"
    
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=6006, debug=False)
