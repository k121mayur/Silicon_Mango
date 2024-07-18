from app import db

from sqlalchemy import Column, Integer, String, Float, Date
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager


class studentdatbase(db.model):

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    mobile_number = Column(Integer, unique=True)
    city = Column(String)
    code = Column(String)
    