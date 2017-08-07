from . import user
from flask import jsonify, request


@user.route('/', methods=['GET'])
def get_users():
    return jsonify({'user':'Remy'})