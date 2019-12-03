from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from src import db


class Shipment(db.Model):
    __tablename__ = 'shipments'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    products = db.relationship('Product', backref='shipment', lazy=True)
