import os
import json

from flask import render_template, current_app, redirect, url_for
from flask_login import login_required

from src import global_products, global_products_json
from src.shipment import bp
from src.shipment.forms import CreateShipmentForm, AddProductForm
from src.entities.product import Product, ProductSchema
from src.entities.shipment import Shipment


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateShipmentForm()
    form.products.data = global_products_json
    if form.validate_on_submit():
        pass
    return render_template('shipment/create_shipment.html', title='Create Shipment', form=form)


@bp.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = AddProductForm()
    if form.validate_on_submit():
        global_products.append(form.name.data)
        global_products_json.append(form.to_dict())
        print(global_products_json)
        return redirect(url_for('shipment.create'))
    return render_template('shipment/add_product.html', title='Add a Product', form=form)
