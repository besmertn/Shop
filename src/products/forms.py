from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, HiddenField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Length, NumberRange, Required

from src import global_shopping
from src.entities.product import Product, UnitEnum


class AddDiscountForm(FlaskForm):
    product = SelectField('Select a Product')
    discount = IntegerField('Discount (%)', validators=[NumberRange(min=1, max=100)])
    submit = SubmitField('Set Discount')
