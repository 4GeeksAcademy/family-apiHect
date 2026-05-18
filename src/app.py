"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Inicializamos la clase limpia con sus 3 miembros nativos (John, Jane, Tommy)
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


# =========================================================================
# 📍 ENDPOINTS CORREGIDOS (TODOS EN PLURAL '/members')
# =========================================================================

# 1) OBTENER TODOS LOS MIEMBROS (GET /members)
@app.route('/members', methods=['GET'])
def get_all_family_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200


# 2) OBTENER UN SOLO MIEMBRO (GET /members/<int:member_id>)
@app.route('/members/<int:member_id>', methods=['GET'])
def get_single_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    return jsonify({"msg": "Member not found"}), 400


# 3) AÑADIR UN NUEVO MIEMBRO (POST /members)
@app.route('/members', methods=['POST'])
def add_new_member():
    request_data = request.get_json()
    if not request_data:
        return jsonify({"msg": "Body empty"}), 400

    new_member = jackson_family.add_member(request_data)
    return jsonify(new_member), 200


# 4) ELIMINAR UN MIEMBRO (DELETE /members/<int:member_id>)
@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_single_member(member_id):
    success = jackson_family.delete_member(member_id)
    if success:
        return jsonify({"done": True}), 200
    return jsonify({"msg": "Member not found to delete"}), 400

# =========================================================================

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)