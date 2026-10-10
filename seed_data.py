"""
Database Seeder Script for MAHFOOZ Restaurant
Populates categories, gourmet food items, default admin user, and sample data.
"""

from app import app
from models import db, Admin, Category, FoodItem, Order, OrderItem, TableReservation, ContactMessage
from werkzeug.security import generate_password_hash
from datetime import datetime

def seed_database():
    with app.app_context():
        # Create tables
        db.create_all()
        print("[SEED] Checked and created tables if not existing.")

        # Seed Admin if none exists
        admin = Admin.query.filter_by(username='admin').first()
        if not admin:
            admin = Admin(
                username='admin',
                email='admin@mahfoozrestaurant.com',
                password_hash=generate_password_hash('admin123'),
                full_name='Chef Mahfooz Alam',
                role='superadmin'
            )
            db.session.add(admin)
            print("[SEED] Created default admin user: 'admin' (password: 'admin123')")
        else:
            print("[SEED] Admin user already exists.")

        # Seed Categories
        categories_data = [
            {
                'name': 'Starters',
                'slug': 'starters',
                'description': 'Crispy, sizzling appetizers marinated in authentic Awadhi and tandoori spices.',
                'image_url': 'https://images.unsplash.com/photo-1544025162-d76694265947?w=800&auto=format&fit=crop&q=80',
                'display_order': 1
            },
            {
                'name': 'Biryani',
                'slug': 'biryani',
                'description': 'Aromatic dum-cooked long-grain Basmati rice infused with saffron and royal spices.',
                'image_url': 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=800&auto=format&fit=crop&q=80',
                'display_order': 2
            },
            {
                'name': 'Indian Main Course',
                'slug': 'indian-main-course',
                'description': 'Rich, velvety gravies and traditional royal curries perfected over slow flame.',
                'image_url': 'https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?w=800&auto=format&fit=crop&q=80',
                'display_order': 3
            },
            {
                'name': 'Chinese',
                'slug': 'chinese',
                'description': 'Wok-tossed delicacies bursting with oriental sauces and smoky crunch.',
                'image_url': 'https://images.unsplash.com/photo-1585032226651-759b368d7246?w=800&auto=format&fit=crop&q=80',
                'display_order': 4
            },
            {
                'name': 'Pizza',
                'slug': 'pizza',
                'description': 'Handcrafted stone-baked pizzas with gourmet mozzarella and fresh toppings.',
                'image_url': 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800&auto=format&fit=crop&q=80',
                'display_order': 5
            },
            {
                'name': 'Burgers',
                'slug': 'burgers',
                'description': 'Juicy grilled patties, molten cheese, and toasted artisanal brioche buns.',
                'image_url': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=800&auto=format&fit=crop&q=80',
                'display_order': 6
            },
            {
                'name': 'Desserts',
                'slug': 'desserts',
                'description': 'Royal sweet indulgences, traditional delicacies, and luscious treats.',
                'image_url': 'https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=800&auto=format&fit=crop&q=80',
                'display_order': 7
            },
            {
                'name': 'Beverages',
                'slug': 'beverages',
                'description': 'Refreshing mocktails, handcrafted royal shakes, and coolers.',
                'image_url': 'https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=800&auto=format&fit=crop&q=80',
                'display_order': 8
            }
        ]

        cat_map = {}
        for cat in categories_data:
            existing_cat = Category.query.filter_by(slug=cat['slug']).first()
            if not existing_cat:
                new_cat = Category(**cat)
                db.session.add(new_cat)
                db.session.flush()
                cat_map[cat['slug']] = new_cat.id
            else:
                cat_map[cat['slug']] = existing_cat.id

        db.session.commit()
        print(f"[SEED] Categories verified/seeded ({len(categories_data)} categories).")

        # Seed Food Items if none exists
        if FoodItem.query.count() == 0:
            food_items_data = [
                # Starters
                {
                    'category_slug': 'starters',
                    'name': 'Royal Galouti Kebab',
                    'description': 'Melt-in-mouth smoked lamb patties infused with 24 rare Lucknowi spices served with mint chutney and warqi paratha.',
                    'price': 380.0,
                    'is_veg': False,
                    'image_url': 'https://images.unsplash.com/photo-1599488615731-7e5c2823ff28?w=800&auto=format&fit=crop&q=80',
                    'is_available': True,
                    'is_featured': True,
                    'rating': 4.9,
                    'preparation_time': '25-30 mins'
                },
                {
                    'category_slug': 'starters',
                    'name': 'Tandoori Malai Paneer Tikka',
                    'description': 'Fresh cottage cheese cubes marinated in rich clotted cream, cardamom, and roasted in clay tandoor oven.',
                    'price': 320.0,
                    'is_veg': True,
                    'image_url': 'https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=800&auto=format&fit=crop&q=80',
                    'is_available': True,
                    'is_featured': True,
                    'rating': 4.8,
                    'preparation_time': '20-25 mins'
                },
                {
                    'category_slug': 'starters',
                    'name': 'Bihari Champaran Mutton Boti',
                    'description': 'Slow-marinated tender mutton pieces roasted with whole garlic pods, mustard oil, and freshly ground cumin.',
                    'price': 440.0,
                    'is_veg': False,
                    'image_url': 'https://images.unsplash.com/photo-1544025162-d76694265947?w=800&auto=format&fit=crop&q=80',
                    'is_available': True,
                    'is_featured': True,
                    'rating': 5.0,
                    'preparation_time': '30 mins'
                },
                {
                    'category_slug': 'starters',
                    'name': 'Crispy Corn & Water Chestnut Salt & Pepper',
                    'description': 'Sweet corn and crunchy chestnuts tossed in wok with spring onions, sea salt, and crushed black peppercorns.',
                    'price': 260.0,
                    'is_veg': True,
                    'image_url': 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=800&auto=format&fit=crop&q=80',
                    'is_available': True,
                    'is_featured': False,
                    'rating': 4.7,
                    'preparation_time': '15-20 mins'
                },

                # Biryani
                {
                    'category_slug': 'biryani',
                    'name': 'Mahfooz Special Dum Mutton Biryani',
                    'description': 'Our flagship recipe: Slow dum-cooked tender goat meat with fragrant Basmati, golden onions, and royal saffron.',
                    'price': 480.0,
                    'is_veg': False,
                    'image_url': 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=800&auto=format&fit=crop&q=80',
                    'is_available': True,
                    'is_featured': True,
                    'rating': 5.0,
                    'preparation_time': '25-30 mins'
                },
                {
                    'category_slug': 'biryani',
                    'name': 'Kolkata-Awadhi Chicken Biryani',
                    'description': 'Juicy marinated chicken, velvety boiled potato, and fragrant long-grain rice scented with kewra and meetha ittar.',
                    'price': 380.0,
                    'is_veg': False,
                    'image_url': 'https://images.unsplash.com/photo-1633945274405-b6c8069047b0?w=800&auto=format&fit=crop&q=80',
                    'is_available': True,
                    'is_featured': True,
                    'rating': 4.8,
                    'preparation_time': '20-25 mins'
                },
                {
                    'category_slug': 'biryani',
                    'name': 'Shahi Subz Paneer Dum Biryani',
                    'description': 'Seasonal garden vegetables and grilled cottage cheese layered with saffron-infused rice and caramelized nuts.',
                    'price': 310.0,
                    'is_veg': True,
                    'image_url': 'https://images.unsplash.com/photo-1642821373181-696a54913e9a?w=800&auto=format&fit=crop&q=80',
                    'is_available': True,
                    'is_featured': False,
                    'rating': 4.7,
                    'preparation_time': '20-25 mins'
                },

                # Indian Main Course
                {
                    'category_slug': 'indian-main-course',
                    'name': 'Old Delhi Butter Chicken',
                    'description': 'Charcoal-grilled chicken tikka simmered in a velvety sauce of vine-ripened tomatoes, churned butter, and fenugreek.',
                    'price': 420.0,
                    'is_veg': False,
                    'image_url': 'https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?w=800&auto=format&fit=crop&q=80',
                    'is_available': True,
                    'is_featured': True,
                    'rating': 4.9,
                    'preparation_time': '20-25 mins'
                },
                {
                    'category_slug': 'indian-main-course',
                    'name': 'Dal Mahfooz (24-Hour Slow Cooked)',
                    'description': 'Signature black lentils simmered overnight on slow charcoal flame with churned butter and Kashmiri chili.',
                    'price': 290.0,
                    'is_veg': True,
                    'image_url': 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=800&auto=format&fit=crop&q=80',
                    'is_available': True,
                    'is_featured': True,
                    'rating': 4.9,
                    'preparation_time': '15-20 mins'
                },
                {
                    'category_slug': 'indian-main-course',
                    'name': 'Patna Kadhai Paneer',
                    'description': 'Fresh cottage cheese tossed with bell peppers, crushed coriander seeds, and tangy masala gravy.',
                    'price': 340.0,
                    'is_veg': True,
                    'image_url': 'https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=800&auto=format&fit=crop&q=80',
                    'is_available': True,
                    'is_featured': False,
                    'rating': 4.8,
                    'preparation_time': '20 mins'
                },
                {
                    'category_slug': 'indian-main-course',
                    'name': 'Mutton Rogan Josh',
                    'description': 'Kashmiri style aromatic tender lamb braised with dried ginger, fennel seeds, and ratanjot extract.',
                    'price': 490.0,
                    'is_veg': False,
                    'image_url': 'https://images.unsplash.com/photo-1545247181-516773cae7be?w=800&auto=format&fit=crop&q=80',
                    'is_available': True,
                    'is_featured': False,
                    'rating': 4.9,
                    'preparation_time': '25-30 mins'
                },

                # Chinese
                {
                    'category_slug': 'chinese',
                    'name': 'Chilli Chicken Gravy (Kolkata Tangra Style)',
                    'description': 'Batter-fried succulent chicken wok-tossed with fresh green chilies, garlic, and dark soy sauce.',
                    'price': 340.0,
                    'is_veg': False,
                    'image_url': 'https://images.unsplash.com/photo-1585032226651-759b368d7246?w=800&auto=format&fit=crop&q=80',
                    'is_available': True,
                    'is_featured': False,
                    'rating': 4.7,
                    'preparation_time': '20 mins'
                },
                {
                    'category_slug': 'chinese',
                    'name': 'Veg Hakka Noodles with Burnt Garlic',
                    'description': 'Hand-pulled noodles stir-fried with crunchy julienned veggies and golden crispy burnt garlic oil.',
                    'price': 240.0,
                    'is_veg': True,
                    'image_url': 'https://images.unsplash.com/photo-1612927601601-6638404737ce?w=800&auto=format&fit=crop&q=80',
                    'is_available': True,
                    'is_featured': False,
                    'rating': 4.6,
                    'preparation_time': '15-20 mins'
                },
                {
                    'category_slug': 'chinese',
                    'name': 'Schezwan Fried Rice with Paneer',
                    'description': 'Long grain rice tossed with homemade fiery Schezwan chili paste, crunchy veggies, and diced paneer.',
                    'price': 260.0,
                    'is_veg': True,
                    'image_url': 'https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=800&auto=format&fit=crop&q=80',
                    'is_available': True,
                    'is_featured': False,
                    'rating': 4.7,
                    'preparation_time': '15-20 mins'
                },

                # Pizza
                {
                    'category_slug': 'pizza',
                    'name': 'Truffle & Smoked Chicken Pizza (12 inch)',
                    'description': 'Thin crust woodfired pizza layered with San Marzano sauce, smoked chicken, mushrooms, and mozzarella.',
                    'price': 460.0,
                    'is_veg': False,
                    'image_url': 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800&auto=format&fit=crop&q=80',
                    'is_available': True,
                    'is_featured': True,
                    'rating': 4.8,
                    'preparation_time': '20 mins'
                },
                {
                    'category_slug': 'pizza',
                    'name': 'Artisanal Margherita Supreme',
                    'description': 'Classic Neapolitan style with fresh buffalo mozzarella, fresh basil leaves, and extra virgin olive oil.',
                    'price': 360.0,
                    'is_veg': True,
                    'image_url': 'https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?w=800&auto=format&fit=crop&q=80',
                    'is_available': True,
                    'is_featured': False,
                    'rating': 4.7,
                    'preparation_time': '15-20 mins'
                },

                # Burgers
                {
                    'category_slug': 'burgers',
                    'name': 'Mahfooz Double Smashed Lamb Burger',
                    'description': 'Double flame-grilled lamb patties, melted cheddar, caramelized onions, and secret smoked mayo on brioche.',
                    'price': 350.0,
                    'is_veg': False,
                    'image_url': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=800&auto=format&fit=crop&q=80',
                    'is_available': True,
                    'is_featured': False,
                    'rating': 4.8,
                    'preparation_time': '15-20 mins'
                },
                {
                    'category_slug': 'burgers',
                    'name': 'Crispy Peri Peri Paneer Burger',
                    'description': 'Spicy crusted paneer steak with crunchy purple slaw, house pickled jalapeños, and peri-peri sauce.',
                    'price': 270.0,
                    'is_veg': True,
                    'image_url': 'https://images.unsplash.com/photo-1550547660-d9450f859349?w=800&auto=format&fit=crop&q=80',
                    'is_available': True,
                    'is_featured': False,
                    'rating': 4.6,
                    'preparation_time': '15 mins'
                },

                # Desserts
                {
                    'category_slug': 'desserts',
                    'name': 'Shahi Tukda with Saffron Rabdi',
                    'description': 'Ghee-fried golden artisanal bread steeped in cardamom syrup and blanketed with thick reduced saffron rabdi.',
                    'price': 220.0,
                    'is_veg': True,
                    'image_url': 'https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=800&auto=format&fit=crop&q=80',
                    'is_available': True,
                    'is_featured': True,
                    'rating': 4.9,
                    'preparation_time': '10-15 mins'
                },
                {
                    'category_slug': 'desserts',
                    'name': 'Gulab Jamun with Pistachio Ice Cream',
                    'description': 'Hot, melt-in-mouth milk dumplings served alongside a scoop of handcrafted artisanal pistachio ice cream.',
                    'price': 190.0,
                    'is_veg': True,
                    'image_url': 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=800&auto=format&fit=crop&q=80',
                    'is_available': True,
                    'is_featured': False,
                    'rating': 4.8,
                    'preparation_time': '10 mins'
                },

                # Beverages
                {
                    'category_slug': 'beverages',
                    'name': 'Royal Kesar Badam Thandai',
                    'description': 'Chilled whole milk infused with saffron strands, crushed almonds, rose petals, and aromatic fennel.',
                    'price': 180.0,
                    'is_veg': True,
                    'image_url': 'https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=800&auto=format&fit=crop&q=80',
                    'is_available': True,
                    'is_featured': False,
                    'rating': 4.9,
                    'preparation_time': '10 mins'
                },
                {
                    'category_slug': 'beverages',
                    'name': 'Spiced Mango Mint Cooler',
                    'description': 'Refreshing Alphonso pulp muddled with garden mint, rock salt, lime juice, and sparkling soda.',
                    'price': 160.0,
                    'is_veg': True,
                    'image_url': 'https://images.unsplash.com/photo-1556881286-fc6915169721?w=800&auto=format&fit=crop&q=80',
                    'is_available': True,
                    'is_featured': False,
                    'rating': 4.7,
                    'preparation_time': '10 mins'
                }
            ]

            for item in food_items_data:
                cat_id = cat_map.get(item['category_slug'])
                if cat_id:
                    new_item = FoodItem(
                        category_id=cat_id,
                        name=item['name'],
                        description=item['description'],
                        price=item['price'],
                        is_veg=item['is_veg'],
                        image_url=item['image_url'],
                        is_available=item['is_available'],
                        is_featured=item['is_featured'],
                        rating=item['rating'],
                        preparation_time=item['preparation_time']
                    )
                    db.session.add(new_item)

            db.session.commit()
            print(f"[SEED] Successfully seeded {len(food_items_data)} gourmet food items!")

        # Sample Reservation if empty
        if TableReservation.query.count() == 0:
            res1 = TableReservation(
                reservation_code='TBL-MFZ-8821B4',
                guest_name='Aditya Verma',
                guest_phone='+91 98350 12345',
                guest_email='aditya.verma@example.com',
                reservation_date='2025-10-15',
                reservation_time='08:00 PM',
                guest_count=4,
                seating_preference='Royal Family Lounge',
                special_requests='Window view requested for anniversary dinner celebration.',
                status='Confirmed'
            )
            res2 = TableReservation(
                reservation_code='TBL-MFZ-9914C2',
                guest_name='Priya Sinha',
                guest_phone='+91 94310 98765',
                guest_email='priya.sinha@example.com',
                reservation_date='2025-10-16',
                reservation_time='07:30 PM',
                guest_count=2,
                seating_preference='Rooftop/Balcony',
                special_requests='Candle light setup if possible.',
                status='Pending'
            )
            db.session.add_all([res1, res2])
            db.session.commit()
            print("[SEED] Seeded initial sample reservations.")

        # Sample Order if empty
        if Order.query.count() == 0:
            first_food = FoodItem.query.first()
            if first_food:
                order = Order(
                    order_number='MFZ-20251009-A92F1C',
                    customer_name='Rahul Kumar',
                    customer_phone='+91 97710 44321',
                    customer_email='rahul.kumar@gmail.com',
                    delivery_address='Flat 402, Ganga Heights, Bailey Road, Patna, Bihar - 800014',
                    subtotal=760.0,
                    delivery_fee=0.0,
                    tax_amount=38.0,
                    total_amount=798.0,
                    payment_method='Cash on Delivery',
                    payment_status='Pending',
                    order_status='Preparing',
                    special_notes='Please provide extra mint chutney and sliced onions.'
                )
                db.session.add(order)
                db.session.flush()

                order_item = OrderItem(
                    order_id=order.id,
                    food_item_id=first_food.id,
                    item_name=first_food.name,
                    item_price=first_food.price,
                    quantity=2,
                    subtotal=first_food.price * 2
                )
                db.session.add(order_item)
                db.session.commit()
                print("[SEED] Seeded sample order.")

        # Sample Contact Message if empty
        if ContactMessage.query.count() == 0:
            msg = ContactMessage(
                name='Sunil Sharma',
                email='sunil.sharma@patnacorp.in',
                phone='+91 93340 77112',
                subject='Corporate Banquet Enquiry for 50 Guests',
                message='We are looking to host an annual corporate dinner at your banquet hall on Fraser Road next month. Please share menu packages and availability.',
                is_read=False
            )
            db.session.add(msg)
            db.session.commit()
            print("[SEED] Seeded sample contact message.")

        print("[SEED] Database initialization and seeding completed successfully!")

if __name__ == '__main__':
    seed_database()
