import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)


jackson_family = FamilyStructure("Jackson")


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    response_body = members
    if members == None:
        return jsonify({"message": "Ha ocurrido un error"}), 400

    return jsonify(response_body), 200


@app.route('/member/<int:member_id>', methods=['GET'])
def get_member_by_id(member_id):
    response_body = jackson_family.get_member(member_id)
    if response_body == None:
        return jsonify({"message": "Ha ocurrido un error"}), 400

    return jsonify(response_body), 200


@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    response_body = {"done": jackson_family.delete_member(member_id)}
    if response_body == None:
        return jsonify({"message": "Ha ocurrido un error"}), 400

    return jsonify(response_body), 200



@app.route('/member', methods=['POST'])
def add_member():
    request_body = request.json
    member = {'id': request_body['id'] or jackson_family._generateId(), 
              'first_name': request_body['first_name'],
              'age': request_body['age'],
              'lucky_numbers': request_body['lucky_numbers']}
    if member == None:
        return jsonify({"message": "Ha ocurrido un error"}), 400

    response_body = jackson_family.add_member(member)
    return jsonify(response_body), 200


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
