from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import current_user, login_required
from app.models import Product, db

shop = Blueprint('shop', __name__, template_folder = 'shoptemplates')

# A route that shows a list of all available products
@shop.route('/allproducts')
def allProducts():
    products = Product.query.all()
    return render_template('products.html', products=products)

# a route which shows a single product (with the information of the product you just clicked)
@shop.route('/product/<int:product_id>')
@login_required
def singleProduct(product_id):
    product = Product.query.get(product_id)
    return render_template('singleproduct.html', product=product)

# A route (cart) that shows a list of products you’ve added into your cart as well as the total of all the items in your cart
@shop.route('/add/<int:product_id>')
@login_required
def addToCart(product_id):
    product = Product.query.get(product_id)
    if current_user.cart.all():
        current_user.cart.add(product)
    else:
        flash('Added to cart', 'success')
    return redirect(url_for('cart.html'))

# Add a route that, when clicked handles functionality that removes all items from your cart one time. Also create a button that, when pressed, it removes that specific product object from the cart.
@shop.route('/remove/<int:product_id>')
@login_required
def removeFromCart(product_id):
    product = Product.query.get(product_id)
    if current_user.cart.all():
        current_user.cart.remove(product)
    else:
        flash('Removed from cart', 'danger')
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

####################### API ROUTES #######################
@shop.route('/api/products', methods=['POST', 'GET'])
def getAllProductsAPI():
    # args = request.args
    # pin = args.get('pin')
    # print(pin, type(pin))
    # if pin == '1234':

        products = Product.query.all() #list of posts

        my_products = [p.to_dict() for p in products]
        print(my_products)
        return {'status': 'ok', 'total_results': len(products), 'products': my_products}
    # else:
    #     return {
    #         'status': 'not ok',
    #         'code': 'Invalid pin',
    #         'message': 'The pin number was incorrect, please try again'
    #     }