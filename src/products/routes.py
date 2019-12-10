import json
from datetime import timedelta, datetime

from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required

from src import global_products, global_products_json, db
from src.products import bp
from src.products.forms import AddDiscountForm
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
        d['shelflife_zone'] = determine_shelflife_zone(d['expiration_date'], p.shipment.date.date())
        products_list.append(d)
    return render_template('products/products.html', title='Products managment', products=products_list)


@bp.route('/add_discount', methods=['GET', 'POST'])
@login_required
def add_discount():
    form = AddDiscountForm(request.form)
    products = Product.query.all()
    products_list = []
    for p in products:
        zone = determine_shelflife_zone(p.shipment.date.date() + timedelta(days=p.expiration_period), p.shipment.date.date())
        if zone == "risky":
            products_list.append((p.code, "{0} [{1}]".format(p.name, p.code)))
    form.product.choices = products_list
    if form.validate_on_submit():
        product = Product.find_by_code(form.product.data)
        discount = 1 - form.discount.data / 100
        product.price *= discount
        db.session.commit()
        return redirect(url_for('products.index'))
    return render_template('products/add_discount.html', title='Add Discount', form=form)


@bp.route('/remove', methods=['GET', 'POST'])
@login_required
def remove():
    products = Product.query.all()
    for p in products:
        zone = determine_shelflife_zone(p.shipment.date.date() + timedelta(days=p.expiration_period), p.shipment.date.date())
        if zone == "overdue":
            db.session.delete(p)
    db.session.commit()
    return redirect(url_for('products.index'))


def determine_shelflife_zone(expiration_date, shipment_date):
    rest = datetime.today().date() - shipment_date
    total = expiration_date - shipment_date
    if expiration_date <= datetime.today().date():
        return "overdue"
    elif (rest / total) * 100 > 90 or (expiration_date - shipment_date).days <= 2:
        return "risky"
    else:
        return "common"
