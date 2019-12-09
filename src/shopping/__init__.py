from flask import Blueprint

bp = Blueprint('shopping', __name__)

from src.shopping import routes, forms
