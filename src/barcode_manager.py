from pyzbar.pyzbar import decode
from PIL import Image
from barcode import generate
from barcode.writer import ImageWriter
from flask import current_app


def generate_barcode(product, save_path):
    generate(current_app.config['BARCODE_TYPE'],
             product.code,
             writer=ImageWriter(),
             output="{0}/{1}{2}".format(save_path, product.name, product.shipment_id))


def scan_barcode(path):
    pass
