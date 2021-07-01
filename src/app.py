"""Factory method to create flask application"""
import logging
from logging.config import fileConfig
import os
from pathlib import Path
from flask import Flask

LOG_FILE_CONF_PATH = os.path.join(Path(os.path.realpath(__file__)).parent, 'logging.cfg')
fileConfig(LOG_FILE_CONF_PATH, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

# pylint: disable=import-outside-toplevel
# pylint: disable=wrong-import-position

def create_app():
    """Factory method to create Flask app"""
    application = Flask(__name__)
    application.config.from_object(os.environ['FLASK_CONFIG'])

    from src.main import bp as main_bp
    application.register_blueprint(main_bp)

    from src.models import db, migrate
    db.init_app(application)
    migrate.init_app(application, db)

    return application

app = create_app()

from src.main import routes
