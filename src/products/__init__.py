from flask import Blueprint

bp = Blueprint('products', __name__)

from src.products import routes
