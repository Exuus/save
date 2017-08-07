import os

from app import create_app, db
from app.models import User

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)

if __name__ == '__main__':
    with app.app_context():
        # create a development user
        if User.query.get(1) is None:
            u = User(username='rmuhire')
            u.set_password('18061992')
            db.session.add(u)
            db.session.commit()
    app.run()