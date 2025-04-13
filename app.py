from flask import Flask, render_template, request, redirect, url_for, flash,session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from models.models import db, User, Product, Cart
from sqlalchemy import func  # Import func for SQL functions

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db.init_app(app)
migrate = Migrate(app, db)

# Route to add products (admin)
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        new_product = Product(
            name=request.form['name'],
            manufacturer=request.form['manufacturer'],
            rating=float(request.form['rating']),
            reviews=int(request.form['reviews']),
            current_price=float(request.form['current_price']),
            original_price=float(request.form['original_price']),
            discount=request.form['discount'],
            image=request.form['image'],
            description=request.form['description'],
            origin=request.form['origin'],
            status=request.form['status'],
            category=request.form['category'].title(),  # Ensure category is capitalized
            stock=int(request.form['stock'])
        )
        db.session.add(new_product)
        db.session.commit()
        flash('Product added successfully!')
        return redirect(url_for('index'))
    return render_template('add_product.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id  # Store user ID in session to track login state
            session['username'] = user.username  # Store username in session for display
            return redirect(url_for('index'))
        else:
            flash('Incorrect username or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user ID from session
    session.pop('username', None)  # Remove username from session
    return redirect(url_for('index'))


@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')  # Get the search query from the form

    # Perform a case-insensitive search for a product by name
    product = Product.query.filter(Product.name.ilike(f'%{query}%')).first()

    # If a product is found, redirect to the product details page
    if product:
        return redirect(url_for('detail', product_id=product.id))
    
    # If no product is found, return an error message or handle it accordingly
    return "Product not found", 404

@app.route('/product/<int:product_id>')
def detail(product_id):
    is_logged_in = 'user_id' in session
    product = Product.query.get_or_404(product_id)
    return render_template('details.html', product=product,is_logged_in=is_logged_in,
                           username=session.get('username'))


@app.route('/')
def index():
    # Check if the user is logged in by inspecting session
    is_logged_in = 'user_id' in session

    # Fetch products and categories
    all_products = Product.query.all()
    todays_offers = Product.query.filter(func.trim(Product.category) == 'Offers').limit(4).all()
    best_selling = Product.query.filter(func.trim(Product.category) == 'Best Selling').limit(4).all()
    growth_promoters = Product.query.filter(func.trim(Product.category) == 'Growth-Promoters').limit(4).all()
    sprayers = Product.query.filter(func.trim(Product.category) == 'Sprayers').limit(4).all()

    return render_template('index.html',
                           products=all_products,
                           todays_offers=todays_offers,
                           best_selling=best_selling,
                           growth_promoters=growth_promoters,
                           sprayers=sprayers,
                           is_logged_in=is_logged_in,
                           username=session.get('username'))

@app.route('/category/<string:category_name>')
def category(category_name):
    # Fetch products that belong to the specified category
    is_logged_in = 'user_id' in session
    products = Product.query.filter(func.trim(Product.category) == category_name.title()).all()
    return render_template('category.html', products=products, category_name=category_name,is_logged_in=is_logged_in,
                           username=session.get('username'))

@app.route('/product/<int:product_id>', methods=['GET', 'POST'])
def product_details(product_id):
    is_logged_in = 'user_id' in session
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        quantity = int(request.form.get('quantity', 1))
        if product.stock >= quantity:
            product.stock -= quantity
            cart_item = Cart.query.filter_by(product_id=product_id).first()
            if cart_item:
                cart_item.quantity += quantity
            else:
                cart_item = Cart(product_id=product_id, quantity=quantity)
                db.session.add(cart_item)
            db.session.commit()
            flash('Product added to cart!')
        else:
            flash('Not enough stock available')
        return redirect(url_for('index'))
    return render_template('details.html', product=product,is_logged_in=is_logged_in,
                           username=session.get('username'))

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    
    quantity = int(request.form.get('quantity', 1))
    product = Product.query.get_or_404(product_id)
    
    # Check if the product is already in the cart
    cart_item = Cart.query.filter_by(product_id=product.id).first()

    if cart_item:
        # If the item is already in the cart, update the quantity
        cart_item.quantity += quantity
    else:
        # Otherwise, add a new entry to the cart
        new_cart_item = Cart(product_id=product.id, quantity=quantity,product=product)
        db.session.add(new_cart_item)

    db.session.commit()  # Commit the changes to the database
    return redirect(url_for('cart'),)

@app.route('/buy_now/<int:product_id>', methods=['POST'])
def buy_now(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get('quantity', 1))  # Get quantity from the form

    # Check if sufficient stock is available
    if product.stock >= quantity:
        # Add to cart or perform buy now logic
        new_cart_item = Cart(product_id=product.id, quantity=quantity)
        db.session.add(new_cart_item)

        # Reduce stock
        product.stock -= quantity
        db.session.commit()  # Commit the changes to the database

        return redirect(url_for('index'))  # Redirect to index or confirmation page
    else:
        return "Insufficient stock available", 400  # Handle insufficient stock case
    
    
@app.route('/delete_cart_item/<int:item_id>', methods=['POST'])
def delete_cart_item(item_id):
    cart_item = Cart.query.get_or_404(item_id)  # Get the cart item
    db.session.delete(cart_item)  # Delete the item from the database
    db.session.commit()  # Commit the changes
    return redirect(url_for('cart'))  # Redirect back to the cart page
 
@app.route('/cart')
def cart():
    is_logged_in = 'user_id' in session
    cart_items = Cart.query.all()  # Fetch all cart items
    
    # Calculate the total price in Python (outside the template)
    total_price = sum(item.product.current_price * item.quantity for item in cart_items)
    
    return render_template('cart.html', cart_items=cart_items, total_price=total_price,is_logged_in=is_logged_in,
                           username=session.get('username'))



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
