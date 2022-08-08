from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import current_user, login_required
from app.models import Product, db

shop = Blueprint('shop', __name__, template_folder = 'shoptemplates')

# A route that shows a list of all available products
@shop.route('/allproducts')
def allProducts():
    products = Product.query.all()
    return render_template('feed.html', products=products)

# a route which shows a single product (with the information of the product you just clicked)
@shop.route('/product')
@login_required
def singleProduct(product_id):
    product = Product.query.get(product_id)
    return render_template('singleproduct.html', product=product)

# A route (cart) that shows a list of products you’ve added into your cart as well as the total of all the items in your cart
@shop.route('/add/<string:product_name>')
@login_required
def addToCart(product_name):
    product = Product.query.filter_by(name=product_name).first()
    if current_user.cart.all():
        current_user.cart.append(product)
        current_user.save()
    else:
        flash('Added to cart', 'success')
    return redirect(url_for('cart.html'))

# Add a route that, when clicked handles functionality that removes all items from your cart one time. Also create a button that, when pressed, it removes that specific product object from the cart.
@shop.route('/remove/<string:product_name>')
@login_required
def removeFromCart(product_id):
    product = Product.query.filter(product_id == product_id).first()
    current_user.cart.remove(product)
    flash('Successfully removed!', 'success')
    return redirect(url_for('cart.html'))

# @shop.route('/removeall')
# @login_required
# def removeAllProducts():
#     if current_user.is_authenticated:
#         product = current_user.cart()
#     else:
#         db.session.clear()
#         current_user.save()

#         return render_template('cart.html', product=product)


#     current_user.cart.clear(product)
#     current_user.save()
#     return render_template('cart.html')