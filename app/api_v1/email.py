from flask import request
from ..decorators import json
from . import api
from ..save_email import help


@api.route('/support/', methods=['POST'])
@json
def new_support():
    email = help(request.json['names'], request.json['email'],
                 request.json['title'], request.json['message'])
    if email:
        return {}, 200
    return {}, 404
