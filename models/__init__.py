from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100))
    role = db.Column(db.String(50), default='admin')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    display_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('FoodItem', backref='category', lazy=True, cascade='all, delete-orphan')

class FoodItem(db.Model):
    __tablename__ = 'food_items'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    is_veg = db.Column(db.Boolean, default=True, nullable=False)
    image_url = db.Column(db.String(500), default='')
    is_available = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Float, default=4.5)
    preparation_time = db.Column(db.String(50), default='20-30 min')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    customer_name = db.Column(db.String(120), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    customer_email = db.Column(db.String(120))
    delivery_address = db.Column(db.Text, nullable=False)
    subtotal = db.Column(db.Float, nullable=False, default=0)
    delivery_fee = db.Column(db.Float, nullable=False, default=0)
    tax_amount = db.Column(db.Float, nullable=False, default=0)
    total_amount = db.Column(db.Float, nullable=False, default=0)
    payment_method = db.Column(db.String(50), default='COD')
    payment_status = db.Column(db.String(30), default='Pending')
    order_status = db.Column(db.String(30), default='Pending')
    special_notes = db.Column(db.Text)
    razorpay_order_id = db.Column(db.String(120))
    razorpay_payment_id = db.Column(db.String(120))
    razorpay_signature = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    food_item_id = db.Column(db.Integer, db.ForeignKey('food_items.id'))
    item_name = db.Column(db.String(150), nullable=False)
    item_price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    subtotal = db.Column(db.Float, nullable=False)

class TableReservation(db.Model):
    __tablename__ = 'table_reservations'
    id = db.Column(db.Integer, primary_key=True)
    reservation_code = db.Column(db.String(50), unique=True, nullable=False)
    guest_name = db.Column(db.String(120), nullable=False)
    guest_phone = db.Column(db.String(20), nullable=False)
    guest_email = db.Column(db.String(120))
    reservation_date = db.Column(db.String(30), nullable=False)
    reservation_time = db.Column(db.String(30), nullable=False)
    guest_count = db.Column(db.Integer, nullable=False, default=2)
    seating_preference = db.Column(db.String(80))
    special_requests = db.Column(db.Text)
    status = db.Column(db.String(30), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
