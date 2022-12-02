from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Inventory, inven_schema, invens_schema

api= Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'Truth' :'Jaal and cloud are sexy!'}

@api.route('/stock', methods = ['POST'])
@token_required
def add_item(current_user_token):
    year = request.json['year']
    make = request.json['make']
    model = request.json['model']
    value = request.json['value']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    car = Inventory(year, make, model, value, user_token= user_token)

    db.session.add(car)
    db.session.commit()

    response = inven_schema.dump(car)
    return jsonify(response)

@api.route('/stock', methods= ['GET'])
@token_required
def get_item(current_user_token):
    a_user =  current_user_token.token
    items = Inventory.query.filter_by(user_token = a_user).all()
    response = invens_schema.dump(items)
    return jsonify(response)

#might not work- if not comment out
@api.route('/stock/<id>', methods= ['GET'])
@token_required
def get_single_item(current_user_token, id):
    item = Inventory.query.get(id)
    response = inven_schema.dump(item)
    return jsonify(response)



#update item
@api.route('/item/<id>', methods=['POST', 'PUT'])
@token_required
def update_contact(current_user_token, id):
    item = Inventory.query.get(id)
    item.year = request.json['year']
    item.make = request.json['make']
    item.model = request.json['model']
    item.value = request.json['value']
    item.user_token = current_user_token.token

    db.session.commit()
    response = inven_schema.dump(item)
    return jsonify(response)

#delete contact entry
@api.route('/items/<id>', methods = ['DELETE'])
@token_required
def delete_contact(current_user_token, id):
    item = Inventory.query.get(id)
    db.session.delete(item)
    db.session.commit()
    response = inven_schema.dump(item)
    return jsonify(response)