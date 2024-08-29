import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Add initial members
initial_members = [
    {'id': 1, 'first_name': 'John', 'last_name': 'Doe', 'age': 30, 'lucky_numbers': [7, 13, 22]},
    {'id': 2, 'first_name': 'Jane', 'last_name': 'Doe', 'age': 28, 'lucky_numbers': [3, 17, 25]},
    {'id': 3, 'first_name': 'Jim', 'last_name': 'Doe', 'age': 25, 'lucky_numbers': [4, 8, 16]}
]

for member in initial_members:
    jackson_family.add_member(member)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_members():
    try:
        members = jackson_family.get_all_members()
        return jsonify(members), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    try:
        member = jackson_family.get_member(member_id)
        if member:
            return jsonify(member), 200
        return jsonify({'message': 'Miembro no encontrado'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/member', methods=['POST'])
def add_member():
    try:
        data = request.get_json()
        if 'id' not in data or 'first_name' not in data or 'age' not in data or 'lucky_numbers' not in data:
            return jsonify({'message': 'Datos no válidos'}), 400
        member = {
            'id': data['id'],
            'first_name': data['first_name'],
            'age': data['age'],
            'lucky_numbers': data['lucky_numbers'],
            'last_name': jackson_family.last_name
        }
        jackson_family.add_member(member)
        return jsonify(member), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        success = jackson_family.delete_member(member_id)
        if success:
            return jsonify({'done': True}), 200
        return jsonify({'message': 'Miembros no encontrados'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
