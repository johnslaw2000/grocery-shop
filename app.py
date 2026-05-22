import os
from flask import Flask, render_template, request, redirect, url_for
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
    products = Product.query.all()
    return render_template("products.html", products=products)


@app.route("/add", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        product = Product(
            name=request.form["name"],
            price=float(request.form["price"]),
            stock=int(request.form["stock"]),
        )
        db.session.add(product)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("form.html", product=None)


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_product(id):
    product = Product.query.get_or_404(id)
    if request.method == "POST":
        product.name = request.form["name"]
        product.price = float(request.form["price"])
        product.stock = int(request.form["stock"])
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("form.html", product=product)


@app.route("/delete/<int:id>")
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=5000)
