import os
from flask import Flask
from flask_restplus import Api
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS

PKG_NAME = os.path.dirname(os.path.realpath(__file__)).split("/")[-1]

migrate = Migrate()


def create_app(app_name=PKG_NAME, **kwargs):
    from api import api as apiNamespace

    application = Flask(app_name)
    application.url_map.strict_slashes = False
    CORS(application)
    api = Api(
        application,
        version='0.1',
        title='Audio API',
        description='Simulates the behavior of an audio file server.'
    )

    from db import db, db_config
    application.config['RESTPLUS_MASK_SWAGGER'] = False
    application.config.update(db_config)
    db.init_app(application)
    application.db = db

    migrate.init_app(application, db=db)
    application.cli.add_command(MigrateCommand, name="db")

    api.add_namespace(apiNamespace)

    return application
