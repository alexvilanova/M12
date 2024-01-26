from flask import Blueprint

api_bp = Blueprint('api', __name__)

from . import users, statuses, orders, auth, tokens
