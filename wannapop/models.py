from flask_login import UserMixin
from flask import url_for
from . import db_manager as db
from sqlalchemy.sql import func
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import check_password_hash, generate_password_hash
from .mixins import BaseMixin, SerializableMixin
from typing import Optional
from datetime import datetime
from datetime import timedelta
from datetime import timezone

import secrets

class User(UserMixin, db.Model, BaseMixin, SerializableMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    role = db.Column(db.String, nullable=False)
    __password = db.Column("password", db.String, nullable=False)
    verified = db.Column(db.Integer, nullable=False)
    email_token = db.Column(db.String, nullable=True, server_default=None)
    created = db.Column(db.DateTime, server_default=func.now())
    updated = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    token: db.Mapped[Optional[str]] = db.mapped_column(
        db.String(32), index=True, unique=True)
    token_expiration: db.Mapped[Optional[datetime]]

    def get_id(self):
        return self.email
    
    @hybrid_property
    def password(self):
        # https://stackoverflow.com/a/31915355
        return ""
    
    @password.setter
    def password(self, plain_text_password):
        self.__password = generate_password_hash(plain_text_password, method="scrypt")

    def check_password(self, some_password):
        return check_password_hash(self.__password, some_password)

    def is_admin(self):
        return self.role == "admin"

    def is_moderator(self):
        return self.role == "moderator"
    
    def is_admin_or_moderator(self):
        return self.is_admin() or self.is_moderator()
    
    def is_wanner(self):
        return self.role == "wanner"

    def is_action_allowed_to_product(self, action, product = None):
        from .helper_role import _permissions, Action

        current_permissions = _permissions[self.role]
        if not current_permissions:
            return False
        
        if not action in current_permissions:
            return False
        
        # Un usuari wanner sols pot modificar el seu propi producte
        if (action == Action.products_update and self.is_wanner()):
            if not product:
                return False
            return self.id == product.seller_id
        
        # Un usuari wanner sols pot eliminar el seu propi producte
        if (action == Action.products_delete and self.is_wanner()):
            if not product:
                return False
            return self.id == product.seller_id
        
        # si hem arribat fins aquí, l'usuari té permisos
        return True

   
    def get_token(self, expires_in=3600):
        now = datetime.now(timezone.utc)
        if self.token and self.token_expiration.replace(
                tzinfo=timezone.utc) > now + timedelta(seconds=60):
            return self.token
        self.token = secrets.token_hex(16)
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.now(timezone.utc) - timedelta(
            seconds=1)

    @staticmethod
    def check_token(token):
        user = db.session.scalar(db.select(User).where(User.token == token))
        if user is None or user.token_expiration.replace(
                tzinfo=timezone.utc) < datetime.now(timezone.utc):
            return None
        return user

class Product(db.Model, BaseMixin, SerializableMixin):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    photo = db.Column(db.String, nullable=False)
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey("statuses.id"), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created = db.Column(db.DateTime, server_default=func.now())
    updated = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    slug = db.Column(db.String, nullable=False)

class Status(db.Model, BaseMixin, SerializableMixin):
    __tablename__ = "statuses"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    slug = db.Column(db.String, nullable=False)

class BlockedUser(db.Model, BaseMixin, SerializableMixin):
    __tablename__ = 'blocked_users'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    admin_id = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime, server_default=func.now())

class Order(db.Model, BaseMixin, SerializableMixin):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    offer = db.Column(db.Numeric(precision=10, scale=2))
    created = db.Column(db.DateTime, server_default=func.now())

    # product = db.relationship('Product', backref='orders')
    # buyer = db.relationship('User', backref='orders')

class ConfirmedOrder(db.Model, BaseMixin, SerializableMixin):
    __tablename__ = 'confirmed_orders'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    created = db.Column(db.DateTime, server_default=func.now())

    # order = db.relationship('Order', backref=db.backref('confirmed_order', uselist=False))
