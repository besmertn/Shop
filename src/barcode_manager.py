from pyzbar.pyzbar import decode
from PIL import Image
from barcode import generate
from barcode.writer import ImageWriter
from flask import current_app


def generate_barcode(product, save_path=current_app.config['BARCODE_PATH']):
    generate(current_app.config['BARCODE_TYPE'],
             product.code,
             writer=ImageWriter(),
             output="{}}/{}{}.png".format(save_path, product.name, product.id))
