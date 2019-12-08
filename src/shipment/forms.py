from datetime import datetime

from flask import jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField, DateTimeField, HiddenField, FloatField
from wtforms.validators import ValidationError, DataRequired, NumberRange

from src.entities.product import Product, UnitEnum
from src import global_products


class CreateShipmentForm(FlaskForm):
    datetime = DateTimeField('Shipment date time', default=datetime.utcnow())
    products = HiddenField()
    submit = SubmitField('Create Sipment')


class AddProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    unit = SelectField('Unit', choices=[(e.name, e.value) for e in UnitEnum])
    price = FloatField(
        label='Price',
        validators=[NumberRange(min=0.01, message='Price may not be less than 0.1')],
        default=0.1
    )
    amount = IntegerField(
        label='Amount',
        validators=[NumberRange(min=1, message='You may not add less than one product')],
        default=1
    )
    submit = SubmitField('Add')

    def validate_name(self, name):
        if name.data in global_products:
            raise ValidationError('Such product already added')

    def to_dict(self):
        return {
            "name": self.name.data,
            "unit": self.unit.data,
            "price": self.price.data,
            "amount": self.amount.data
        }
