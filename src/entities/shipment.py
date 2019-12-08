from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import desc

from src import db


class Shipment(db.Model):
    __tablename__ = 'shipments'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    products = db.relationship('Product', backref='shipment', lazy=True)

    def __init__(self, date):
        self.date = date

    @classmethod
    def find_by_date(cls, date):
        return cls.query.filter_by(date=date).first()

    @classmethod
    def find_last(cls):
        return cls.query.order_by(desc('id')).first()
