from flask import Flask, render_template

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
        'image': 'https://cdn.shopify.com/s/files/1/0722/2059/products/4_bd3ad653-2283-4098-aa9f-1d13b22b22b8.webp',  # Full URL
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
    app.run(debug=True)
