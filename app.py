from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Welcome to Donde</h1><p>A calmer way to choose where to go out.</p>"

if __name__ == "__main__":
    app.run(debug=True)
