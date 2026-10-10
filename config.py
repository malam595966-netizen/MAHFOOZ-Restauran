import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'dev-only-change-this-secret-before-deployment'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_pre_ping': True}
    RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID', '')
    RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET', '')
    RAZORPAY_CURRENCY = os.getenv('RAZORPAY_CURRENCY', 'INR')
    RESTAURANT_UPI_ID = os.getenv('RESTAURANT_UPI_ID', 'mahfoozrestaurant@oksbi')
    RESTAURANT_UPI_NAME = os.getenv('RESTAURANT_UPI_NAME', 'MAHFOOZ RESTAURANT PATNA')
    RESTAURANT_PHONE = os.getenv('RESTAURANT_PHONE', '')
    RESTAURANT_ADDRESS = os.getenv('RESTAURANT_ADDRESS', 'Patna, Bihar, India')
    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')

    @staticmethod
    def database_uri():
        explicit = os.getenv('DATABASE_URL') or os.getenv('POSTGRES_URL')
        if explicit:
            # Pin the driver: SQLAlchemy 2.1+ defaults "postgresql://" to psycopg v3, but we ship psycopg2.
            for prefix in ('postgres://', 'postgresql://'):
                if explicit.startswith(prefix):
                    explicit = 'postgresql+psycopg2://' + explicit[len(prefix):]
                    break
            return explicit
        db_type = os.getenv('DB_TYPE', 'sqlite').lower()
        if db_type == 'mysql':
            from urllib.parse import quote_plus
            user = quote_plus(os.getenv('MYSQL_USER', 'root'))
            password = quote_plus(os.getenv('MYSQL_PASSWORD', ''))
            host = os.getenv('MYSQL_HOST', 'localhost')
            port = os.getenv('MYSQL_PORT', '3306')
            name = os.getenv('MYSQL_DB', 'mahfooz_restaurant')
            return f'mysql+pymysql://{user}:{password}@{host}:{port}/{name}?charset=utf8mb4'
        bundled_db = BASE_DIR / 'mahfooz_restaurant.db'
        if os.getenv('VERCEL'):
            # Vercel's filesystem is read-only except /tmp, so copy the bundled SQLite DB there.
            import shutil
            tmp_db = Path('/tmp/mahfooz_restaurant.db')
            if not tmp_db.exists() and bundled_db.exists():
                shutil.copy(bundled_db, tmp_db)
            return 'sqlite:///' + str(tmp_db)
        return 'sqlite:///' + str(bundled_db)

    SQLALCHEMY_DATABASE_URI = database_uri.__func__()
