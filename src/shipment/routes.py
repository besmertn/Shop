import json

from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required
from wtforms.validators import ValidationError

from src import global_products, global_products_json, db
from src.shipment import bp
from src.shipment.forms import CreateShipmentForm, AddProductForm
from src.entities.product import Product
from src.entities.shipment import Shipment


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateShipmentForm(request.form)
    if form.is_submitted():
        if form.products.data == '[]':
            flash('No products specified')
            return redirect(url_for('shipment.create'))
        result = json.loads(form.products.data.replace("\'", "\""))
        shipment = Shipment(date=form.datetime.data)
        db.session.add(shipment)
        db.session.commit()
        shipment = Shipment.find_last()
        for prod in result:
            product = Product(
                shipment_id=shipment.id,
                name=prod['name'],
                unit=prod['unit'],
                price=prod['price'],
                amount=prod['amount']
            )
            db.session.add(product)
        db.session.commit()
        global_products.clear()
        global_products_json.clear()
        return redirect(url_for('main.index'))

    form.products.data = global_products_json
    return render_template('shipment/create_shipment.html', title='Create Shipment', form=form)


@bp.route('/get', methods=['GET'])
@login_required
def get():
    shipments = Shipment.query.all()
    return render_template('shipment/list_of_shipments.html', title='List of Shipments', shipments=shipments)


@bp.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = AddProductForm(request.form)
    if form.validate_on_submit():
        global_products.append(form.name.data)
        global_products_json.append(form.to_dict())
        return redirect(url_for('shipment.create'))
    return render_template('shipment/add_product.html', title='Add a Product', form=form)
