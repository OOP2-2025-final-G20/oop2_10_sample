from peewee import Model, ForeignKeyField, DateTimeField, IntegerField # IntegerFieldを追加
from .db import db
from .user import User
from .product import Product

class Order(Model):
    user = ForeignKeyField(User, backref='orders')
    product = ForeignKeyField(Product, backref='orders')
    order_date = DateTimeField()
    # 以下の1行を追加してください
    quantity = IntegerField() 

    class Meta:
        database = db