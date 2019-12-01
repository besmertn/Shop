from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import enum

from src import db


class UnitEnum(enum.Enum):
    GRAM = 'g'
    PIECE = 'pc'
    LITRE = 'l'


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    shipment_id = db.Column(db.Integer, db.ForeignKey('shipment.id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    unit = db.Column(db.Enum(UnitEnum), nullable=False)
    price = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
