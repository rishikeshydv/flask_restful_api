from enum import unique
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

#initialise app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

#database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#initialise database and marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

#Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True) 
    name = db.Column(db.String(100), unique = True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty

#Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'qty')

#init schema        
product_schema = ProductSchema()
products_schema = ProductSchema(many = True)

#create a product
@app.route('/product', methods = ['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product(name, description, price, qty)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

#get all products
@app.route('/product', methods = ['GET'])
def get_products():
    all_products = Product.query.all()
    results = products_schema.dump(all_products)
    return jsonify(results)

#get a product
@app.route('/product/<id>', methods = ['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

#update a product
@app.route('/product/<id>', methods = ['PUT'])
def update_product(id):

    up_product = Product.query.get(id)
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    up_product.name = name
    up_product.description = description
    up_product.price = price
    up_product.qty = qty
   
    db.session.commit()

    return product_schema.jsonify(up_product)

#delete a product
@app.route('/product/<id>', methods = ['DELETE'])
def delete_product(id):
    del_product = Product.query.get(id)
    db.session.delete(del_product)
    db.session.commit()
    return product_schema.jsonify(del_product)

#run server
if __name__ == '__main__':
    app.run(debug = True)

