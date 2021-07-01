import os
import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(os.path.abspath(os.path.dirname(__file__))).parent))

from src.app import create_app
from src.models import db, CityTemperature, Capitals


@pytest.fixture
def app():
    os.environ["FLASK_CONFIG"] = "config.TestingConfig"
    app = create_app()

    return app

@pytest.fixture
def database(app):
    with app.app_context():
        db.drop_all()
        db.create_all()

    yield db
