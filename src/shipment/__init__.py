from flask import Blueprint

bp = Blueprint('shipment', __name__)

from src.shipment import routes, forms
