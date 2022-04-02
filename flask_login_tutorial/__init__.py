"""Initialize app."""
from authlib.integrations.flask_client import OAuth
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
sess = Session()

authlib_oauth_client = OAuth()


def create_app():
    """Construct the core app object."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")

    # Initialize Plugins
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    sess.init_app(app)

    authlib_oauth_client.init_app(app)

    with app.app_context():

        from .assets import compile_static_assets
        from .routes import main
        from .services.iam import routes as iam

        # Register Blueprints
        app.register_blueprint(main.main_bp)
        app.register_blueprint(iam.iam_bp)

        # Create Database Models
        # db.create_all()

        # Compile static assets
        if app.config["FLASK_ENV"] == "development":
            compile_static_assets(app)

        return app
