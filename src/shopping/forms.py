from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, HiddenField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Length, NumberRange

from src import global_shopping
from src.entities.product import Product, UnitEnum


class ShoppingForm(FlaskForm):
    products = HiddenField(validators=[DataRequired()])
    submit = SubmitField('Submit')


class ScanForm(FlaskForm):
    barcode_img = FileField('Select Barcode', validators=[DataRequired()])
    submit = SubmitField('Scan')


class AddProductForm(FlaskForm):
    code = StringField(
        'Product Barcode',
        validators=[DataRequired(), Length(min=13, max=13, message="The barcode should be 13 digits length")]
    )
    amount = IntegerField('Amount', validators=[NumberRange(min=1)], default=1)
    submit = SubmitField('Add Product')

    def validate_code(self, code):
        product = Product.find_by_code(code.data)
        if product is None:
            raise ValidationError('There is no product with such code')

    def validate_amount(self, amount):
        product = Product.find_by_code(self.code.data)
        if product is not None:
            if self.code.data not in global_shopping:
                global_amount = 0
            else:
                global_amount = global_shopping[self.code.data]
            if product.amount < amount.data + global_amount:
                raise ValidationError("There are only " + str(product.amount) + " such products")
