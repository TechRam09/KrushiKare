from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    manufacturer = db.Column(db.String)
    rating = db.Column(db.Float)
    reviews = db.Column(db.Integer)
    current_price = db.Column(db.Float)
    original_price = db.Column(db.Float)
    discount = db.Column(db.String)
    image = db.Column(db.String)
    description = db.Column(db.Text)
    origin = db.Column(db.String)
    status = db.Column(db.String)
    category = db.Column(db.String, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, nullable=False)
    product = db.relationship('Product', backref='carts')
