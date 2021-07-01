#! /usr/bin/env python
import os
from pathlib import Path
import sys
import time
import inspect
import tempfile
import json
sys.path.insert(0, str(Path(os.path.abspath(os.path.dirname(__file__))).parent))
from flask import url_for
from src.models import CityTemperature, Capitals, db


def test_get_temperature_dublin(app):
    """Get temperature for dublin city"""
    print('Executing - ', inspect.currentframe().f_code.co_name)
    with app.app_context():
        # This is just a hack as pytest fixture for database is not working
        db.drop_all()
        db.create_all()
        response = app.test_client().open(url_for('main.city_temparature', _external=False),
                                    method='REPORT',
                                    json={"city": 'Dublin', 'local_time': int(time.time())},
                                    content_type='application/json')
        assert'Error' not in response.get_data(as_text=True)

def test_get_temperature_ireland(app):
    """Get temparature of the capital city"""
    print('Executing - ', inspect.currentframe().f_code.co_name)
    with app.app_context():
        response = app.test_client().open(url_for('main.capital_city_temparature', _external=False),
                                    method='REPORT',
                                    json={"country": 'Ireland', 'local_time': int(time.time())},
                                    content_type='application/json')
        assert'Error' not in response.get_data(as_text=True)

def test_get_temperature_unknown_city(app):
    """Unknown city"""
    print('Executing - ', inspect.currentframe().f_code.co_name)
    with app.app_context():
        response = app.test_client().open(url_for('main.city_temparature', _external=False),
                                    method='REPORT',
                                    json={"city": 'Unknownd', 'local_time': int(time.time())},
                                    content_type='application/json')
        assert'Error' in response.get_data(as_text=True)

def test_get_temperature_unknown_country(app):
    """Get temparature of the capital city"""
    print('Executing - ', inspect.currentframe().f_code.co_name)
    with app.app_context():
        response = app.test_client().open(url_for('main.capital_city_temparature', _external=False),
                                    method='REPORT',
                                    json={"country": 'Unknown', 'local_time': int(time.time())},
                                    content_type='application/json')
        assert'Error' not in response.get_data(as_text=True)

