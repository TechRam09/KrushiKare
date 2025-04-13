from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash,check_password_hash  # Import for hashing passwords

app = Flask(__name__)

# Sample product data
products = {
    1: {
        'name': 'Sempra Herbicide',
        'manufacturer': 'Dhanuka',
        'rating': '4.9',
        'reviews': '33 reviews',
        'current_price': '₹222',
        'original_price': '₹281',
        'discount': '21% OFF',
        'image': 'https://cdn.shopify.com/s/files/1/0722/2059/products/4_bd3ad653-2283-4098-aa9f-1d13b22b22b8.webp',
        'description': [
            'Sempra Herbicide is the first herbicide introduced in India by Dhanuka Agritech Ltd for effective control of Cyperus rotundus.',
            'It is a selective, systemic, post-emergence herbicide with WDG formulation for effective control of Cyperus rotundus from nuts in Sugarcane and Maize crop.',
            'Sempra Herbicide has strong systemic action i.e. moves in both ways through Xylem & Phloem.'
        ],
        'origin': 'India',
        'status': 'In stock, Ready to Ship'
    },
    2: {
        'name': 'Roundup Weed Killer',
        'manufacturer': 'Bayer',
        'rating': '4.7',
        'reviews': '28 reviews',
        'current_price': '₹350',
        'original_price': '₹450',
        'discount': '22% OFF',
        'image': 'https://cdn.shopify.com/s/files/1/0722/2059/products/4_bd3ad653-2283-4098-aa9f-1d13b22b22b8.webp',
        'description': [
            'Roundup Weed Killer is the most effective product to manage weeds in a variety of crops.',
            'It offers post-emergence weed control with strong systemic action.',
            'Best suited for use in non-crop areas, vineyards, and more.'
        ],
        'origin': 'Germany',
        'status': 'Limited Stock, Ships within 3 days'
    },
    # Add more products as needed...
}

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Model creation
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(128), nullable=False)  # Increased length for hashed passwords

    def __repr__(self):
        return f"{self.username}"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        try:
            new_user = User(
                username=username,
                email=email,
                password=generate_password_hash(password)  # Hashing the password
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            print(f"Error occurred: {e}")  # Log the error
            return "There was an issue with your registration", 500

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()  # Query the user by username
        if user and check_password_hash(user.password, password):  # Check hashed password
            return redirect(url_for('index'))  # Redirect to index page on successful login
        else:
            return "Username or password is incorrect", 401  # Handle invalid login

    return render_template('login.html')  # Render login page on GET request


# Route for the index page with product listings
@app.route('/')
def index():
    return render_template('index.html', products=products)

# Route for the product details page
@app.route('/details/<int:product_id>')
def product_details(product_id):
    product = products.get(product_id)
    if product:
        return render_template('details.html', product=product)
    else:
        return "Product not found", 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
