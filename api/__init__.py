import os
from flask import Flask, request
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from sqlalchemy_utils import create_database, database_exists

from api.config import config

def create_app(test_config=None):
    app = Flask(__name__)

    # check environment variables to see which config to load
    env = os.environ.get("FLASK_ENV", "dev")
    if test_config:
        # ignore environment variable config if config was given
        app.config.from_mapping(**test_config)
    else:
        app.config.from_object(config[env])


    # decide whether to create database
    if env != "prod":
        db_url = app.config["SQLALCHEMY_DATABASE_URI"]
        if not database_exists(db_url):
            create_database(db_url)

    bootstrap = Bootstrap(app)


    # register sqlalchemy to this app
    from api.models import db

    db.init_app(app)
    Migrate(app, db)

    # import and register blueprints
    from api.views import main

    app.register_blueprint(main.main)
    main.login_manager.init_app(app)
    main.login_manager.login_view = 'login'
    
    return app
