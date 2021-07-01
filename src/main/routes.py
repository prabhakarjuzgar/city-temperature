"""This model implements rest end-points to get temparature of a city"""
import os
from typing import Dict, Tuple
import time
import requests
from sqlalchemy.exc import SQLAlchemyError
from flask import request, jsonify, make_response, abort
from werkzeug.http import HTTP_STATUS_CODES
from src.main import bp
from src.models import CityTemperature, Capitals, db
from src.app import logger

# pylint: disable=no-member

# Lets return same temparature for 10 minutes
SECONDS = 60 * 10

def error_response(status_code, message=None):
    """Return error response"""
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response = make_response(response)
    return response

def bad_response(message: str, code: int):
    """Invoke error_response"""
    return error_response(code, message)

@bp.route('/')
def hello_world():
    """Base end-point"""
    return "Hello World"

@bp.before_app_request
def before_request():
    """Method executed before handling every request"""
    if os.environ.get('APPID') is None:
        return abort(503, description="APP KEY ID for openweathermap is not set")
    return None

def get_temperature_info(city: str) -> Tuple[int, int]:
    """Invoke openweathermap api to get temparature info
    Arguments:
        city (str): Name of the city
    """
    temp_info = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={os.environ["APPID"]}')
    if temp_info.status_code != 200:
        raise Exception(temp_info.json())

    return temp_info.json()["main"]["temp"], int(temp_info.json()["dt"])

def calculate_temparature(city: str, user_time: int) -> Dict:
    """Get city temparature
    Arguments:
        city (st): Name of the city
        user_time (str): User local time
    """
    row = CityTemperature.query.filter(CityTemperature.city == city).first()
    now_seconds = int(time.time())
    if not row:
        temperature, city_time = get_temperature_info(city)
        diff_time = city_time - now_seconds
        store_info = CityTemperature(city=city, temperature=temperature, fetch_time=now_seconds, diff_time=diff_time)
        db.session.add(store_info)
        db.session.commit()
        ret_data = store_info.to_dict(user_time - city_time)
    else:
        if now_seconds - row.fetch_time > SECONDS:
            temperature, city_time = get_temperature_info(city)
            diff_time = city_time - now_seconds
            store_info = CityTemperature(city, temperature, now_seconds, diff_time)
            db.session.add(store_info)
            db.session.commit()
            ret_data = store_info.to_dict(user_time - city_time)
        else:
            ret_data = row.to_dict(user_time - (now_seconds + row.diff_time))

    return ret_data

@bp.route("/city", methods=['REPORT'])
def city_temparature():
    """Get city temparature"""
    try:
        if not request.is_json:
            return bad_response('Invalid input', 400)

        data = request.get_json()
        city = data["city"]
        user_time = int(data["local_time"])
        ret_data = calculate_temparature(city, user_time)

    except Exception as err:
        return bad_response(f"{str(err)}", 500)

    return jsonify(ret_data)

@bp.route("/country", methods=['REPORT'])
def capital_city_temparature():
    """Get capital city temparature given country name"""
    if not request.is_json:
        return bad_response('Invalid input', 400)

    ret_data = {}
    data = request.get_json()
    country = data["country"]
    user_time = int(data["local_time"])
    city = None
    try:
        row = Capitals.query.filter(Capitals.country == country).first()
        if not row:
            # Get the capital city of the country in request
            country_info = requests.get(f'https://restcountries.eu/rest/v2/alpha/{country}')
            if country_info.status_code != 200:
                return bad_response(
                    f'Invalid Request {country_info.json()}', country_info.status_code)
            city = country_info.json()['capital']
            capital = Capitals(country, city)
            try:
                db.session.add(capital)
                db.session.commit()
            except SQLAlchemyError as err:
                logger.error(str(err))
                return bad_response("Server is busy, please try again", 500)

        else:
            city = row.capital
    except Exception as err:
        return bad_response(f'Invalid input {str(err)}', 500)

    ret_data = calculate_temparature(city, user_time)

    return jsonify(ret_data)
