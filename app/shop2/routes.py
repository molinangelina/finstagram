from flask import Blueprint, request
from ..apiauthhelper import token_required
from app.models import User, Product2, cart2

shop2 = Blueprint('shop2', __name__)

@shop2.route('/api/products2')
def getAllProducts2():
    products = Product2.query.all() # getting all products w/ no order # bc we have a list of objects, we need a list of dictionaries # if sending in HTTp, it needs to be in a dictionary
    return {
        'status':'ok',
        'products': [p.to_dict() for p in products] # a list of products
    }

@shop2.route('/api/products2/<int:product_id>')
def getOneProduct(product_id):
    product = Product2.query.get(product_id)
    return {
        'status':'ok',
        'product': product.to_dict()
    }

@shop2.route('/api/cart', methods=["GET"])
@token_required #whos cart are you getting?
def getCart(user):
    return {
        'status': 'ok',
        'cart': [p.to_dict() for p in user.getCart()] # getting list of all of the cart items 
    }

@shop2.route('/api/cart/add', methods=["POST"]) #what kind of item we're adding
@token_required #whos cart to add it to 
def addToCart(user):
    data = request.json
    product_id = data['productId'] # productId is coming from JS(react)
    product = Product2.query.get(product_id)
    user.addToCart(product)
    return {'status':'ok','message':'Successfully added to cart.'}

@shop2.route('/api/cart/remove', methods=["POST"]) #what kind of item we're adding
@token_required #whos logged in
def removeFromCart(user):
    data = request.json
    product_id = data['productId']
    product = Product2.query.get(product_id)
    user.removeFromCart(product)
    return {'status':'ok','message':'Successfully removed from cart.'}