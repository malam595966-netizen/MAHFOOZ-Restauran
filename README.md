# MAHFOOZ Restaurant — fixed starter project

A responsive Flask restaurant website with a menu, cart, checkout/order creation, order tracking, table reservation requests, contact form, and a staff dashboard for orders, dishes, reservations, and messages.

## Run on Windows

1. Install Python 3.10+ from https://www.python.org/downloads/ and select **Add Python to PATH**.
2. Extract this folder to a normal location such as `C:\Projects\mahfooz_restaurant_fixed_project`.
3. Double-click `run.bat`. It installs the packages and starts the local server.
4. Open `http://127.0.0.1:5000` in your browser.
5. Admin panel: `http://127.0.0.1:5000/admin/login`.

Local demo admin login: `admin` / `admin123`. Change this before making the site public.

## Run from a terminal

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py app.py
```

Open `http://127.0.0.1:5000`. Health check: `http://127.0.0.1:5000/health`.

## Included features

- Responsive home page and menu with search, category and vegetarian filters.
- Cart saved in browser storage; checkout validates menu item IDs and prices on the server.
- Order number and tracking page.
- Table booking requests and confirmation reference.
- Customer contact form.
- Admin login, order status management, menu item add/edit/delete, reservation status updates, and customer messages.
- Automatic SQLite schema repair for the three Razorpay order columns that were missing from the supplied database.
- SQLite works out of the box. Optional MySQL can be configured in `.env` using `DB_TYPE=mysql` and the MySQL values, or set `DATABASE_URL`.

## Important notes before public deployment

- Copy `.env.example` to `.env`; set a long random `SECRET_KEY` and a strong `ADMIN_PASSWORD`. Never upload `.env` or real payment secrets to GitHub.
- The checkout currently supports **Cash on Delivery** and **UPI on delivery** as order/payment labels. It does not collect online payments. Razorpay keys alone do not activate a verified online-payment flow; implement and test the complete order/signature/webhook flow before advertising online payments.
- Use a persistent database/storage plan when hosting. Local SQLite files on many cloud hosts may be ephemeral.
- Sample records in the included database are demo data. Remove them before real business use.
- Customer-facing business address/phone are configurable with `RESTAURANT_ADDRESS` and `RESTAURANT_PHONE`.

## Troubleshooting

- If `py` is not recognized, install Python and enable **Add Python to PATH**, then restart the terminal.
- If dependencies fail to install, run `py -m pip install --upgrade pip` and then `py -m pip install -r requirements.txt`.
- If port 5000 is busy, set `PORT=5001` in the terminal before running `py app.py` and open `http://127.0.0.1:5001`.
- If a traceback appears, copy the full terminal error; a screenshot of just the browser page may hide the useful line.
