import json

from flask import render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required

from src import global_products, global_products_json, db
from src.shipment import bp
from src.shipment.forms import CreateShipmentForm, AddProductForm
from src.entities.product import Product
from src.entities.shipment import Shipment
from src.barcode_manager import generate_barcode


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
                amount=prod['amount'],
                expiration_period=prod['expiration_period']
            )
            generate_barcode(product, current_app.config['BARCODE_PATH'])
            db.session.add(product)
        db.session.commit()
        global_products.clear()
        global_products_json.clear()
        return redirect(url_for('main.index'))

    form.products.data = global_products_json
    return render_template('shipment/create_shipment.html', title='Create Shipment', form=form)


@bp.route('/cancel', methods=['GET', 'POST'])
@login_required
def cancel():
    global_products.clear()
    global_products_json.clear()
    return redirect(url_for('main.index'))


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
