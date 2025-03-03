# routes/__init__.py
from flask import Blueprint

bp = Blueprint('main', __name__)

from routes import auth, story, main
