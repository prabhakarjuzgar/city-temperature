"""Models for the database"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

# pylint: disable=no-member
# pylint: disable=too-few-public-methods


class Capitals(db.Model):
    """Table to store capitals of a given country"""
    __tablename__ = "Capitals"
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String, unique=True, nullable=False)
    capital = db.Column(db.String, unique=True, nullable=False)

class CityTemperature(db.Model):
    """Table to store city and temperature for a defined period"""
    __tablename__ = "CityTemperature"
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String, unique=True, nullable=False)
    temperature = db.Column(db.Integer, nullable=False)
    fetch_time = db.Column(db.Integer, nullable=False)
    diff_time = db.Column(db.Integer, nullable=False)

    def to_dict(self, diff_in_seconds: int):
        """Convert to dict before sending as response
        Arguments:
            diff_in_seconds (int): difference in user location time
            and given city time
        Returns:
            dict: containing city, current temperature and difference
            in time
        """
        data = {
            'city': self.city,
            'temperature': self.temperature,
            'timedelta': diff_in_seconds
        }

        return data
