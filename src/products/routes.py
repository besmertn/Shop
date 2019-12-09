import json
from datetime import timedelta, datetime

from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required
from wtforms.validators import ValidationError

from src import global_products, global_products_json, db
from src.products import bp
from src.entities.product import Product
from src.entities.shipment import Shipment


@bp.route('/', methods=['GET'])
@login_required
def index():
    products = Product.query.all()
    products_list = []
    for p in products:
        d = {
            "name": p.name,
            "unit": p.unit,
            "price": p.price,
            "amount": p.amount,
            "code": p.code,
            "expiration_date": p.shipment.date.date() + timedelta(days=p.expiration_period),
            "shelflife_zone": "common"
        }
        rest = datetime.today().date() - p.shipment.date.date()
        total = d['expiration_date'] - p.shipment.date.date()
        if d['expiration_date'] <= datetime.today().date():
            d['shelflife_zone'] = "overdue"
        elif (rest / total) * 100 > 90 or (d['expiration_date'] - p.shipment.date.date()).days <= 2:
            d['shelflife_zone'] = "risky"
        products_list.append(d)
    return render_template('products/products.html', title='Products managment', products=products_list)
