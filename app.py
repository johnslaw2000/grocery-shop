import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load the .env file so os.environ can see DATABASE_URL etc.
load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]

# Connect SQLAlchemy to the app
db = SQLAlchemy(app)


# A Product is one row in the 'product' table
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)


@app.route("/")
def home():
    count = Product.query.count()
    return f"Grocery Shop is running! Products in database: {count}"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # creates tables that don't exist yet
    app.run(debug=True, host="0.0.0.0", port=5000)
