from . import api
from flask import jsonify, request


@api.route('/users/', methods=['GET'])
def get_users():
    return jsonify({'user':'Remyoooo'})

