from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
     return "Grocery Shop is running!"

if __name__ == "__main__":
     app.run(debug=True, host="0.0.0.0", port=5000)
