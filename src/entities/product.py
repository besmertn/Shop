from random import randint
from datetime import datetime
import enum

from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import Schema, fields, post_load

from src import db


class UnitEnum(enum.Enum):
    gram = 'gram'
    piece = 'piece'
    litre = 'litre'


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    shipment_id = db.Column(db.Integer, db.ForeignKey('shipments.id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    unit = db.Column(db.Enum(UnitEnum), nullable=False)
    price = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    code = db.Column(db.String, nullable=False, unique=True)

    def __init__(self, shipment_id, name, unit, price, amount):
        self.shipment_id = shipment_id
        self.name = name
        self.unit = unit
        self.price = price
        self.amount = amount
        self.code = self.generate_product_code()

    def generate_product_code(self):
        numbers = [randint(0, 9) for i in range(12)]
        control_digit_sum = sum([numbers[i] * 3 for i in range(12) if i % 2 == 1])
        control_digit = ((control_digit_sum // 10) + 1) * 10 - control_digit_sum
        barcode = ''.join([str(x) for x in numbers]) + str(control_digit)

        if self.query.filter_by(code=barcode).first() is not None:
            barcode = self.generate_product_code()

        return barcode


class ProductSchema(Schema):
    id = fields.Number()
    shipment_id = fields.Number()
    name = fields.Str()
    unit = fields.Str()
    price = fields.Float()
    amount = fields.Number()
    code = fields.Str()
