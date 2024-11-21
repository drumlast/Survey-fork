from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf import CSRFProtect

from app.models import Admin, db
from app.blueprints.admin import admin_bp
from app.blueprints.survey import survey_bp

migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['REPORTS_FOLDER'] = 'reports'

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = 'admin.login'
    login_manager.login_message_category = 'info'

    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(survey_bp, url_prefix='/')

    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(int(user_id))

    return app
