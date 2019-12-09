import json

from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required

from src import db, global_shopping
from src.shopping import bp
from src.shopping.forms import AddProductForm, ShoppingForm, ScanForm
from src.entities.product import Product


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    products = []
    total_cost = 0
    form = ShoppingForm(request.form)
    if form.is_submitted():
        if form.products.data == '[]':
            flash('No products specified')
            return redirect(url_for('shopping.index'))
        products_json = json.loads(form.products.data.replace("\'", "\""))
        total_cost = sum([prod['total_price'] for prod in products_json])
        for p in products_json:
            product = Product.find_by_code(p['code'])
            product.amount -= p['amount']
            if product.amount <= 0:
                db.session.delete(product)
            db.session.commit()
        global_shopping.clear()
        return render_template('shopping/invoice.html', title='Invoice', products=products_json, total_cost=total_cost)
    for key, value in global_shopping.items():
        product = Product.find_by_code(key)
        products.append({
            'name': product.name,
            'unit': product.unit.value,
            'amount': value,
            'price': product.price,
            'total_price': value * product.price,
            'code': key
        })
        total_cost += value * product.price
    form.products.data = products
    return render_template('shopping/shopping.html', title='Shopping', products=products, total_cost=total_cost, form=form)


@bp.route('/cancel', methods=['GET', 'POST'])
@login_required
def cancel():
    global_shopping.clear()
    return redirect(url_for('main.index'))


@bp.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = AddProductForm(request.form)
    if form.validate_on_submit():
        if form.code.data in global_shopping:
            global_shopping[form.code.data] += form.amount.data
        else:
            global_shopping.update({form.code.data: form.amount.data})
        return redirect(url_for('shopping.index'))
    return render_template('shopping/add_product.html', title='Add a Product', form=form)


@bp.route('/scan_product', methods=['GET', 'POST'])
@login_required
def scan_product():
    form = ScanForm(request.form)
    if form.validate_on_submit():
        if form.barcode_img.data in global_shopping:
            global_shopping[form.code.data] += form.amount.data
        else:
            global_shopping.update({form.code.data: form.amount.data})
        return redirect(url_for('shopping.index'))
    return render_template('shopping/add_product.html', title='Add a Product', form=form)
