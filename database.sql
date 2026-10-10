-- ========================================================
-- MAHFOOZ RESTAURANT - COMPLETE MYSQL DATABASE SCHEMA & SEED DATA
-- Location: Patna, Bihar, India
-- Compatible with MySQL 5.7+, MySQL 8.0+, MariaDB, phpMyAdmin
-- ========================================================

CREATE DATABASE IF NOT EXISTS `mahfooz_restaurant` 
DEFAULT CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE `mahfooz_restaurant`;

SET FOREIGN_KEY_CHECKS = 0;

-- --------------------------------------------------------
-- Table structure for `admins`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `admins`;
CREATE TABLE `admins` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(80) NOT NULL UNIQUE,
  `email` VARCHAR(120) NOT NULL UNIQUE,
  `password_hash` VARCHAR(255) NOT NULL,
  `full_name` VARCHAR(100) DEFAULT 'Mahfooz Alam (Executive Chef & Owner)',
  `role` VARCHAR(50) DEFAULT 'superadmin',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `last_login` DATETIME NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------
-- Table structure for `categories`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `categories`;
CREATE TABLE `categories` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(100) NOT NULL UNIQUE,
  `slug` VARCHAR(100) NOT NULL UNIQUE,
  `description` TEXT NULL,
  `image_url` VARCHAR(500) NULL,
  `display_order` INT DEFAULT 0,
  `is_active` TINYINT(1) DEFAULT 1,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------
-- Table structure for `food_items`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `food_items`;
CREATE TABLE `food_items` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `category_id` INT NOT NULL,
  `name` VARCHAR(150) NOT NULL,
  `description` TEXT NULL,
  `price` DECIMAL(10,2) NOT NULL,
  `is_veg` TINYINT(1) NOT NULL DEFAULT 0,
  `image_url` VARCHAR(500) NOT NULL,
  `is_available` TINYINT(1) DEFAULT 1,
  `is_featured` TINYINT(1) DEFAULT 0,
  `rating` DECIMAL(2,1) DEFAULT 4.8,
  `preparation_time` VARCHAR(50) DEFAULT '20-25 mins',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT `fk_food_items_category` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------
-- Table structure for `customers`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `customers`;
CREATE TABLE `customers` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(120) NOT NULL,
  `phone` VARCHAR(20) NOT NULL,
  `email` VARCHAR(120) NULL,
  `address` TEXT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------
-- Table structure for `orders`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `order_number` VARCHAR(50) NOT NULL UNIQUE,
  `customer_name` VARCHAR(120) NOT NULL,
  `customer_phone` VARCHAR(20) NOT NULL,
  `customer_email` VARCHAR(120) NULL,
  `delivery_address` TEXT NOT NULL,
  `subtotal` DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  `delivery_fee` DECIMAL(10,2) NOT NULL DEFAULT 40.00,
  `tax_amount` DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  `total_amount` DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  `payment_method` VARCHAR(50) DEFAULT 'Cash on Delivery',
  `payment_status` VARCHAR(30) DEFAULT 'Pending',
  `order_status` VARCHAR(30) DEFAULT 'Pending',
  `special_notes` TEXT NULL,
  `razorpay_order_id` VARCHAR(100) NULL,
  `razorpay_payment_id` VARCHAR(100) NULL,
  `razorpay_signature` VARCHAR(255) NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------
-- Table structure for `order_items`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `order_items`;
CREATE TABLE `order_items` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `order_id` INT NOT NULL,
  `food_item_id` INT NULL,
  `item_name` VARCHAR(150) NOT NULL,
  `item_price` DECIMAL(10,2) NOT NULL,
  `quantity` INT NOT NULL DEFAULT 1,
  `subtotal` DECIMAL(10,2) NOT NULL,
  CONSTRAINT `fk_order_items_order` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_order_items_food` FOREIGN KEY (`food_item_id`) REFERENCES `food_items` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------
-- Table structure for `table_reservations`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `table_reservations`;
CREATE TABLE `table_reservations` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `reservation_code` VARCHAR(50) NOT NULL UNIQUE,
  `guest_name` VARCHAR(120) NOT NULL,
  `guest_phone` VARCHAR(20) NOT NULL,
  `guest_email` VARCHAR(120) NULL,
  `reservation_date` VARCHAR(30) NOT NULL,
  `reservation_time` VARCHAR(30) NOT NULL,
  `guest_count` INT NOT NULL DEFAULT 2,
  `seating_preference` VARCHAR(80) DEFAULT 'Standard Dining',
  `special_requests` TEXT NULL,
  `status` VARCHAR(30) DEFAULT 'Confirmed',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------
-- Table structure for `contact_messages`
-- --------------------------------------------------------
DROP TABLE IF EXISTS `contact_messages`;
CREATE TABLE `contact_messages` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(120) NOT NULL,
  `email` VARCHAR(120) NOT NULL,
  `phone` VARCHAR(20) NULL,
  `subject` VARCHAR(200) NULL,
  `message` TEXT NOT NULL,
  `is_read` TINYINT(1) DEFAULT 0,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;

-- ========================================================
-- SEED DATA
-- ========================================================

-- Default Admin (username: admin, password: admin123)
-- Hash generated via werkzeug scrypt
INSERT INTO `admins` (`id`, `username`, `email`, `password_hash`, `full_name`, `role`, `created_at`) VALUES
(1, 'admin', 'admin@mahfoozrestaurant.com', 'scrypt:32768:8:1$K5g0G5U7bJ5sQp1o$f7f6f1f45dc2463e8e2023dbdf247ba8d6c77bb3a0cbeec7374b78c93eb87f5835948967812ecbc3b9420b991cf9509df6eb14ddc59e6c4349ee14451735520a', 'Mahfooz Alam (Executive Chef & Owner)', 'superadmin', NOW());

-- Categories
INSERT INTO `categories` (`id`, `name`, `slug`, `description`, `image_url`, `display_order`, `is_active`) VALUES
(1, 'Starters', 'starters', 'Crispy, sizzling appetizers marinated in authentic Awadhi and tandoori spices.', 'https://images.unsplash.com/photo-1544025162-d76694265947?w=800&auto=format&fit=crop&q=80', 1, 1),
(2, 'Biryani', 'biryani', 'Aromatic dum-cooked long-grain Basmati rice infused with saffron and royal spices.', 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=800&auto=format&fit=crop&q=80', 2, 1),
(3, 'Indian Main Course', 'indian-main-course', 'Rich, velvety gravies and traditional royal curries perfected over slow flame.', 'https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?w=800&auto=format&fit=crop&q=80', 3, 1),
(4, 'Chinese', 'chinese', 'Wok-tossed delicacies bursting with oriental sauces and smoky crunch.', 'https://images.unsplash.com/photo-1585032226651-759b368d7246?w=800&auto=format&fit=crop&q=80', 4, 1),
(5, 'Pizza', 'pizza', 'Handcrafted stone-baked pizzas with gourmet mozzarella and fresh toppings.', 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800&auto=format&fit=crop&q=80', 5, 1),
(6, 'Burgers', 'burgers', 'Juicy grilled patties, molten cheese, and toasted artisanal brioche buns.', 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=800&auto=format&fit=crop&q=80', 6, 1),
(7, 'Desserts', 'desserts', 'Royal sweet indulgences, traditional delicacies, and luscious treats.', 'https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=800&auto=format&fit=crop&q=80', 7, 1),
(8, 'Beverages', 'beverages', 'Refreshing mocktails, handcrafted royal shakes, and coolers.', 'https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=800&auto=format&fit=crop&q=80', 8, 1);

-- Food Items
INSERT INTO `food_items` (`id`, `category_id`, `name`, `description`, `price`, `is_veg`, `image_url`, `is_available`, `is_featured`, `rating`, `preparation_time`) VALUES
-- Starters
(1, 1, 'Royal Galouti Kebab', 'Melt-in-mouth smoked lamb patties infused with 24 rare Lucknowi spices served with mint chutney and warqi paratha.', 380.00, 0, 'https://images.unsplash.com/photo-1599488615731-7e5c2823ff28?w=800&auto=format&fit=crop&q=80', 1, 1, 4.9, '25-30 mins'),
(2, 1, 'Tandoori Malai Paneer Tikka', 'Fresh cottage cheese cubes marinated in rich clotted cream, cardamom, and roasted in clay tandoor oven.', 320.00, 1, 'https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=800&auto=format&fit=crop&q=80', 1, 1, 4.8, '20-25 mins'),
(3, 1, 'Bihari Champaran Mutton Boti', 'Slow-marinated tender mutton pieces roasted with whole garlic pods, mustard oil, and ground cumin.', 440.00, 0, 'https://images.unsplash.com/photo-1544025162-d76694265947?w=800&auto=format&fit=crop&q=80', 1, 1, 5.0, '30 mins'),
(4, 1, 'Crispy Corn & Water Chestnut Salt & Pepper', 'Sweet corn and crunchy chestnuts tossed in wok with spring onions, sea salt, and crushed black peppercorns.', 260.00, 1, 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=800&auto=format&fit=crop&q=80', 1, 0, 4.7, '15-20 mins'),

-- Biryani
(5, 2, 'Mahfooz Special Dum Mutton Biryani', 'Our flagship recipe: Slow dum-cooked tender goat meat with fragrant Basmati, golden onions, and royal saffron.', 480.00, 0, 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=800&auto=format&fit=crop&q=80', 1, 1, 5.0, '25-30 mins'),
(6, 2, 'Kolkata-Awadhi Chicken Biryani', 'Juicy marinated chicken, velvety boiled potato, and fragrant long-grain rice scented with kewra and meetha ittar.', 380.00, 0, 'https://images.unsplash.com/photo-1633945274405-b6c8069047b0?w=800&auto=format&fit=crop&q=80', 1, 1, 4.8, '20-25 mins'),
(7, 2, 'Shahi Subz Paneer Dum Biryani', 'Seasonal garden vegetables and grilled cottage cheese layered with saffron-infused rice and caramelized nuts.', 310.00, 1, 'https://images.unsplash.com/photo-1642821373181-696a54913e9a?w=800&auto=format&fit=crop&q=80', 1, 0, 4.7, '20-25 mins'),

-- Indian Main Course
(8, 3, 'Old Delhi Butter Chicken', 'Charcoal-grilled chicken tikka simmered in a velvety sauce of vine-ripened tomatoes, butter, and fenugreek.', 420.00, 0, 'https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?w=800&auto=format&fit=crop&q=80', 1, 1, 4.9, '20-25 mins'),
(9, 3, 'Dal Mahfooz (24-Hour Slow Cooked)', 'Signature black lentils simmered overnight on slow charcoal flame with churned butter and Kashmiri chili.', 290.00, 1, 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=800&auto=format&fit=crop&q=80', 1, 1, 4.9, '15-20 mins'),
(10, 3, 'Patna Kadhai Paneer', 'Fresh cottage cheese tossed with bell peppers, crushed coriander seeds, and tangy masala gravy.', 340.00, 1, 'https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=800&auto=format&fit=crop&q=80', 1, 0, 4.8, '20 mins'),
(11, 3, 'Mutton Rogan Josh', 'Kashmiri style aromatic tender lamb braised with dried ginger, fennel seeds, and ratanjot extract.', 490.00, 0, 'https://images.unsplash.com/photo-1545247181-516773cae7be?w=800&auto=format&fit=crop&q=80', 1, 0, 4.9, '25-30 mins'),

-- Chinese
(12, 4, 'Chilli Chicken Gravy (Kolkata Tangra Style)', 'Batter-fried succulent chicken wok-tossed with fresh green chilies, garlic, and dark soy sauce.', 340.00, 0, 'https://images.unsplash.com/photo-1585032226651-759b368d7246?w=800&auto=format&fit=crop&q=80', 1, 0, 4.7, '20 mins'),
(13, 4, 'Veg Hakka Noodles with Burnt Garlic', 'Hand-pulled noodles stir-fried with crunchy julienned veggies and golden crispy burnt garlic oil.', 240.00, 1, 'https://images.unsplash.com/photo-1612927601601-6638404737ce?w=800&auto=format&fit=crop&q=80', 1, 0, 4.6, '15-20 mins'),
(14, 4, 'Schezwan Fried Rice with Paneer', 'Long grain rice tossed with homemade fiery Schezwan chili paste, crunchy veggies, and diced paneer.', 260.00, 1, 'https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=800&auto=format&fit=crop&q=80', 1, 0, 4.7, '15-20 mins'),

-- Pizza
(15, 5, 'Truffle & Smoked Chicken Pizza (12 inch)', 'Thin crust woodfired pizza layered with San Marzano sauce, smoked chicken, mushrooms, and mozzarella.', 460.00, 0, 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800&auto=format&fit=crop&q=80', 1, 1, 4.8, '20 mins'),
(16, 5, 'Artisanal Margherita Supreme', 'Classic Neapolitan style with fresh buffalo mozzarella, fresh basil leaves, extra virgin olive oil.', 360.00, 1, 'https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?w=800&auto=format&fit=crop&q=80', 1, 0, 4.7, '15-20 mins'),

-- Burgers
(17, 6, 'Mahfooz Double Smashed Lamb Burger', 'Double flame-grilled lamb patties, melted cheddar, caramelized onions, and secret smoked mayo on brioche.', 350.00, 0, 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=800&auto=format&fit=crop&q=80', 1, 0, 4.8, '15-20 mins'),
(18, 6, 'Crispy Peri Peri Paneer Burger', 'Spicy crusted paneer steak with crunchy purple slaw, house pickled jalapeños, and peri-peri sauce.', 270.00, 1, 'https://images.unsplash.com/photo-1550547660-d9450f859349?w=800&auto=format&fit=crop&q=80', 1, 0, 4.6, '15 mins'),

-- Desserts
(19, 7, 'Shahi Tukda with Saffron Rabdi', 'Ghee-fried golden artisanal bread steeped in cardamom syrup and blanketed with thick reduced saffron rabdi.', 220.00, 1, 'https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=800&auto=format&fit=crop&q=80', 1, 1, 4.9, '10-15 mins'),
(20, 7, 'Gulab Jamun with Pistachio Ice Cream', 'Hot, melt-in-mouth milk dumplings served alongside a scoop of handcrafted artisanal pistachio ice cream.', 190.00, 1, 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=800&auto=format&fit=crop&q=80', 1, 0, 4.8, '10 mins'),

-- Beverages
(21, 8, 'Royal Kesar Badam Thandai', 'Chilled whole milk infused with saffron strands, crushed almonds, rose petals, and aromatic fennel.', 180.00, 1, 'https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=800&auto=format&fit=crop&q=80', 1, 0, 4.9, '10 mins'),
(22, 8, 'Spiced Mango Mint Cooler', 'Refreshing Alphonso pulp muddled with garden mint, rock salt, lime juice, and sparkling soda.', 160.00, 1, 'https://images.unsplash.com/photo-1556881286-fc6915169721?w=800&auto=format&fit=crop&q=80', 1, 0, 4.7, '10 mins');

-- Sample Table Reservation
INSERT INTO `table_reservations` (`id`, `reservation_code`, `guest_name`, `guest_phone`, `guest_email`, `reservation_date`, `reservation_time`, `guest_count`, `seating_preference`, `special_requests`, `status`, `created_at`) VALUES
(1, 'TBL-MFZ-8821B4', 'Aditya Verma', '+91 98350 12345', 'aditya.verma@example.com', '2025-10-15', '08:00 PM', 4, 'Royal Family Lounge', 'Window view requested for anniversary dinner celebration.', 'Confirmed', NOW()),
(2, 'TBL-MFZ-9914C2', 'Priya Sinha', '+91 94310 98765', 'priya.sinha@example.com', '2025-10-16', '07:30 PM', 2, 'Rooftop/Balcony', 'Candle light setup if possible.', 'Pending', NOW());

-- Sample Order
INSERT INTO `orders` (`id`, `order_number`, `customer_name`, `customer_phone`, `customer_email`, `delivery_address`, `subtotal`, `delivery_fee`, `tax_amount`, `total_amount`, `payment_method`, `payment_status`, `order_status`, `special_notes`, `created_at`) VALUES
(1, 'MFZ-20251009-A92F1C', 'Rahul Kumar', '+91 97710 44321', 'rahul.kumar@gmail.com', 'Flat 402, Ganga Heights, Bailey Road, Patna, Bihar - 800014', 900.00, 0.00, 45.00, 945.00, 'Cash on Delivery', 'Pending', 'Preparing', 'Please provide extra mint chutney and sliced onions.', NOW());

INSERT INTO `order_items` (`id`, `order_id`, `food_item_id`, `item_name`, `item_price`, `quantity`, `subtotal`) VALUES
(1, 1, 5, 'Mahfooz Special Dum Mutton Biryani', 480.00, 1, 480.00),
(2, 1, 8, 'Old Delhi Butter Chicken', 420.00, 1, 420.00);

-- Sample Contact Message
INSERT INTO `contact_messages` (`id`, `name`, `email`, `phone`, `subject`, `message`, `is_read`, `created_at`) VALUES
(1, 'Sunil Sharma', 'sunil.sharma@patnacorp.in', '+91 93340 77112', 'Corporate Banquet Enquiry for 50 Guests', 'We are looking to host an annual corporate dinner at your banquet hall on Fraser Road next month. Please share menu packages and availability.', 0, NOW());
