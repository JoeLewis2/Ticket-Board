from flask import Flask
from dotenv import load_dotenv
from config import Config
from extensions import db, login_manager
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # make sure an instance folder exists for the datebase
    os.makedirs(os.path.join(Config.BASE_DIR, 'instance'), exist_ok=True)

    # initialise extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'

    from auth import auth_bp
    from tickets import tickets_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(tickets_bp)

    # create database tables if they don't exist yet
    with app.app_context():
        from models import User, Ticket, TicketHistory
        db.create_all()

        # seed the database on first run
        if User.query.count() == 0:
            from seed import seed_database
            seed_database(app)

    return app


# flask-login load user code
@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
