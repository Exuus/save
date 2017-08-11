import os

from app import create_app, db
from app.models import User
from flask import jsonify
config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)


@app.route('/user/')
def new_user():
    u = User(username='rmuhire')
    u.set_password('18061992')
    db.session.add(u)
    db.session.commit()
    return jsonify(True)

if __name__ == '__main__':
    with app.app_context():
        # create a development user
        if User.query.get(1) is None:
            u = User(username='rmuhire')
            u.set_password('18061992')
            db.session.add(u)
            db.session.commit()
    app.run()