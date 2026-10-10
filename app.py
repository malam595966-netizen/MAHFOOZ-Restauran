import os, secrets, sqlite3
from datetime import datetime, date
from functools import wraps
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, abort
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import db, Admin, Category, FoodItem, Order, OrderItem, TableReservation, ContactMessage

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Lightweight schema migration: SQLAlchemy create_all does not add columns to existing tables.
def migrate_schema():
    uri = app.config['SQLALCHEMY_DATABASE_URI']
    if not uri.startswith('sqlite:///'):
        return
    db_path = uri.replace('sqlite:///', '', 1)
    if not os.path.exists(db_path):
        return
    con = sqlite3.connect(db_path)
    try:
        existing = {r[1] for r in con.execute('PRAGMA table_info(orders)').fetchall()}
        for name, typ in [('razorpay_order_id', 'VARCHAR(120)'), ('razorpay_payment_id', 'VARCHAR(120)'), ('razorpay_signature', 'VARCHAR(255)')]:
            if name not in existing:
                con.execute(f'ALTER TABLE orders ADD COLUMN {name} {typ}')
        con.commit()
    finally:
        con.close()

with app.app_context():
    db.create_all()
    migrate_schema()
    # Add missing admin only on a new/empty database. Change credentials in .env for public hosting.
    if not Admin.query.filter_by(username=app.config['ADMIN_USERNAME']).first():
        admin = Admin(username=app.config['ADMIN_USERNAME'], email='admin@mahfoozrestaurant.com',
                      password_hash=generate_password_hash(app.config['ADMIN_PASSWORD']),
                      full_name='MAHFOOZ Administrator', role='superadmin')
        db.session.add(admin)
        db.session.commit()

@app.context_processor
def inject_globals():
    return {'restaurant_name': 'MAHFOOZ', 'restaurant_address': app.config.get('RESTAURANT_ADDRESS'),
            'restaurant_phone': app.config.get('RESTAURANT_PHONE'), 'current_year': datetime.now().year}

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get('admin_id'):
            flash('Please log in to access the dashboard.', 'warning')
            return redirect(url_for('admin_login', next=request.path))
        return fn(*args, **kwargs)
    return wrapper

def new_code(prefix):
    return f'{prefix}-{datetime.now():%y%m%d}-{secrets.token_hex(3).upper()}'

@app.get('/')
def index():
    featured = FoodItem.query.filter_by(is_available=True, is_featured=True).limit(6).all()
    if not featured:
        featured = FoodItem.query.filter_by(is_available=True).limit(6).all()
    return render_template('index.html', featured=featured, categories=Category.query.filter_by(is_active=True).order_by(Category.display_order).all())

@app.get('/menu')
def menu():
    categories = Category.query.filter_by(is_active=True).order_by(Category.display_order).all()
    q = request.args.get('q', '').strip()
    category_id = request.args.get('category', type=int)
    veg = request.args.get('veg')
    query = FoodItem.query.filter_by(is_available=True)
    if q: query = query.filter(FoodItem.name.ilike(f'%{q}%'))
    if category_id: query = query.filter_by(category_id=category_id)
    if veg == '1': query = query.filter_by(is_veg=True)
    elif veg == '0': query = query.filter_by(is_veg=False)
    return render_template('menu.html', categories=categories, items=query.order_by(FoodItem.is_featured.desc(), FoodItem.name).all(), q=q, category_id=category_id, veg=veg)

@app.get('/about')
def about(): return render_template('about.html')

@app.get('/contact')
def contact(): return render_template('contact.html')

@app.post('/contact')
def contact_submit():
    name=request.form.get('name','').strip(); email=request.form.get('email','').strip(); message=request.form.get('message','').strip()
    if not name or not email or not message:
        flash('Please fill in your name, email and message.', 'error'); return redirect(url_for('contact'))
    db.session.add(ContactMessage(name=name, email=email, phone=request.form.get('phone','').strip(), subject=request.form.get('subject','').strip(), message=message))
    db.session.commit(); flash('Thank you! Your message has been sent.', 'success'); return redirect(url_for('contact'))

@app.get('/book-table')
def book_table(): return render_template('book_table.html', today=date.today().isoformat())

@app.post('/book-table')
def book_table_submit():
    f=request.form
    required=['name','phone','date','time','guests']
    if any(not f.get(k,'').strip() for k in required):
        flash('Please complete all required booking fields.', 'error'); return redirect(url_for('book_table'))
    try: guests=max(1,min(30,int(f['guests'])))
    except ValueError: guests=2
    booking=TableReservation(reservation_code=new_code('MR'), guest_name=f['name'].strip(), guest_phone=f['phone'].strip(), guest_email=f.get('email','').strip(), reservation_date=f['date'], reservation_time=f['time'], guest_count=guests, seating_preference=f.get('seating','Any'), special_requests=f.get('requests','').strip(), status='Pending')
    db.session.add(booking); db.session.commit()
    return render_template('reservation_confirmation.html', booking=booking)

@app.get('/checkout')
def checkout(): return render_template('checkout.html')

@app.post('/checkout')
def checkout_submit():
    f=request.form
    name=f.get('name','').strip(); phone=f.get('phone','').strip(); address=f.get('address','').strip()
    try: cart=__import__('json').loads(f.get('cart_json','[]'))
    except Exception: cart=[]
    if not name or not phone or not address or not isinstance(cart,list) or not cart:
        flash('Add food to your cart and fill in your name, phone and delivery address.', 'error'); return redirect(url_for('menu'))
    items=[]; subtotal=0
    for row in cart:
        try: item_id=int(row.get('id')); qty=max(1,min(20,int(row.get('quantity',1))))
        except (ValueError,TypeError,AttributeError): continue
        food=FoodItem.query.filter_by(id=item_id,is_available=True).first()
        if food:
            line=round(food.price*qty,2); subtotal+=line; items.append((food,qty,line))
    if not items:
        flash('Your cart items are unavailable. Please refresh the menu and try again.', 'error'); return redirect(url_for('menu'))
    delivery=0 if subtotal>=799 else 49; tax=round(subtotal*0.05,2); total=round(subtotal+delivery+tax,2)
    order=Order(order_number=new_code('MF'), customer_name=name, customer_phone=phone, customer_email=f.get('email','').strip(), delivery_address=address, subtotal=round(subtotal,2), delivery_fee=delivery, tax_amount=tax, total_amount=total, payment_method=f.get('payment_method','COD'), payment_status='Pending', order_status='Pending', special_notes=f.get('notes','').strip())
    db.session.add(order); db.session.flush()
    for food,qty,line in items: db.session.add(OrderItem(order_id=order.id,food_item_id=food.id,item_name=food.name,item_price=food.price,quantity=qty,subtotal=line))
    db.session.commit()
    return render_template('order_confirmation.html', order=order)

@app.get('/track-order')
def track_order(): return render_template('track_order.html', order=None)

@app.post('/track-order')
def track_order_submit():
    number=request.form.get('order_number','').strip()
    order=Order.query.filter_by(order_number=number).first()
    if not order: flash('No order found. Check the order number and try again.', 'error')
    return render_template('track_order.html', order=order)

@app.get('/health')
def health(): return jsonify(status='ok', app='MAHFOOZ', time=datetime.utcnow().isoformat()+'Z')

@app.route('/admin/login', methods=['GET','POST'])
def admin_login():
    if request.method=='POST':
        username=request.form.get('username','').strip(); password=request.form.get('password','')
        admin=Admin.query.filter_by(username=username).first()
        if admin and check_password_hash(admin.password_hash,password):
            session.clear(); session['admin_id']=admin.id; session['admin_name']=admin.full_name or admin.username
            admin.last_login=datetime.utcnow(); db.session.commit()
            return redirect(request.args.get('next') if request.args.get('next','').startswith('/admin') else url_for('admin_dashboard'))
        flash('Incorrect username or password.', 'error')
    return render_template('admin/login.html')

@app.get('/admin/logout')
def admin_logout(): session.clear(); flash('You have been logged out.', 'success'); return redirect(url_for('index'))

@app.get('/admin')
@app.get('/admin/dashboard')
@admin_required
def admin_dashboard():
    return render_template('admin/dashboard.html', order_count=Order.query.count(), pending_count=Order.query.filter_by(order_status='Pending').count(), item_count=FoodItem.query.count(), reservation_count=TableReservation.query.filter_by(status='Pending').count(), orders=Order.query.order_by(Order.created_at.desc()).limit(10).all(), reservations=TableReservation.query.order_by(TableReservation.created_at.desc()).limit(6).all(), messages=ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all())

@app.get('/admin/orders')
@admin_required
def admin_orders(): return render_template('admin/orders.html', orders=Order.query.order_by(Order.created_at.desc()).all())

@app.post('/admin/orders/<int:order_id>/status')
@admin_required
def admin_order_status(order_id):
    order=Order.query.get_or_404(order_id); status=request.form.get('status','Pending')
    if status not in {'Pending','Confirmed','Preparing','Out for delivery','Delivered','Cancelled'}: abort(400)
    order.order_status=status
    if status=='Delivered' and order.payment_method=='COD': order.payment_status='Paid'
    db.session.commit(); flash(f'Order {order.order_number} updated.', 'success'); return redirect(url_for('admin_orders'))

@app.get('/admin/menu')
@admin_required
def admin_menu(): return render_template('admin/menu.html', items=FoodItem.query.order_by(FoodItem.name).all(), categories=Category.query.order_by(Category.display_order).all())

@app.route('/admin/menu/add', methods=['GET','POST'])
@app.route('/admin/menu/<int:item_id>/edit', methods=['GET','POST'])
@admin_required
def admin_item_form(item_id=None):
    item=FoodItem.query.get_or_404(item_id) if item_id else None
    if request.method=='POST':
        f=request.form
        try: price=float(f.get('price','0')); category_id=int(f.get('category_id','0'))
        except ValueError: price=0; category_id=0
        if not f.get('name','').strip() or price<=0 or not Category.query.get(category_id):
            flash('Enter a valid name, price and category.', 'error')
        else:
            if item is None: item=FoodItem(); db.session.add(item)
            item.name=f['name'].strip(); item.description=f.get('description','').strip(); item.price=price; item.category_id=category_id; item.is_veg=f.get('is_veg')=='yes'; item.image_url=f.get('image_url','').strip(); item.is_available=f.get('is_available')=='yes'; item.is_featured=f.get('is_featured')=='yes'; item.preparation_time=f.get('preparation_time','20-30 min').strip()
            db.session.commit(); flash('Menu item saved.', 'success'); return redirect(url_for('admin_menu'))
    return render_template('admin/item_form.html', item=item, categories=Category.query.order_by(Category.display_order).all())

@app.post('/admin/menu/<int:item_id>/delete')
@admin_required
def admin_item_delete(item_id):
    item=FoodItem.query.get_or_404(item_id); db.session.delete(item); db.session.commit(); flash('Menu item deleted.', 'success'); return redirect(url_for('admin_menu'))

@app.get('/admin/reservations')
@admin_required
def admin_reservations(): return render_template('admin/reservations.html', reservations=TableReservation.query.order_by(TableReservation.created_at.desc()).all())

@app.post('/admin/reservations/<int:reservation_id>/status')
@admin_required
def admin_reservation_status(reservation_id):
    reservation=TableReservation.query.get_or_404(reservation_id); status=request.form.get('status','Pending')
    if status not in {'Pending','Confirmed','Cancelled','Completed'}: abort(400)
    reservation.status=status; db.session.commit(); flash('Reservation updated.', 'success'); return redirect(url_for('admin_reservations'))

@app.get('/admin/messages')
@admin_required
def admin_messages(): return render_template('admin/messages.html', messages=ContactMessage.query.order_by(ContactMessage.created_at.desc()).all())

@app.errorhandler(404)
def not_found(_): return render_template('error.html', code=404, message='The page you are looking for was not found.'), 404

@app.errorhandler(500)
def server_error(_): db.session.rollback(); return render_template('error.html', code=500, message='Something went wrong. Please try again.'), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=int(os.getenv('PORT','5000')), debug=os.getenv('FLASK_DEBUG','false').lower()=='true')
