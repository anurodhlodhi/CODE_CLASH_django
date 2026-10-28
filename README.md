# The Code Clash 2026 · FaultLine Commerce (Django)

This is the Django REST Framework track of the individual debugging round. You have 120 minutes to investigate and improve the supplied application while preserving working behavior. The number and location of defects are not disclosed. Use only agents and resources approved by the organisers. Payments are simulated.

## Explore the app

The customer shop at /shop/ supports product browsing, customer sign in, cart changes, coupon entry at checkout and order history. The protected Django /admin/ panel covers products, coupons, carts, orders, payments and audit history. The REST API is under /api/. Shop and admin actions use commerce services.

## Setup with Python 3.10

Run these commands from this directory in PowerShell:

~~~powershell
py -3.10 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py seed_demo
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe -m pytest tests/ -q
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
~~~

On macOS/Linux use python3.10 and .venv/bin/python. Visit http://127.0.0.1:8000/shop/, /admin/ or /api/health/. Stop the server with Ctrl+C.

seed_demo creates demo products, coupons and customers if absent. For local demo data, customer a@test.invalid uses password_a and customer b@test.invalid uses password_b. Create an admin locally with python manage.py createsuperuser. Never submit .env or a local database.

requirements.txt is the documented Python 3.10 install path; requirements.lock pins its tested dependency closure. Use one of them for installation. The project declares Python >=3.10 in pyproject.toml.

## Business rules

- Money uses integer paise in the API and database. The pages display rupees.
- Product price, stock and cart quantity have validation rules. Adding the same product increases its cart quantity.
- Checkout checks current stock, creates a complete order with price snapshots or makes no change, and clears the cart.
- Coupons may be percentage or fixed value and can have dates, minimum spend and usage limits.
- Cancellation must respect payment state and restore inventory once. Simulated payment confirmation and refunds validate references and amounts.
- Customer orders belong to one customer. Staff operations require permissions and CSRF checks.

See CHALLENGE_SPEC.md for exact Django routes, fields, status codes and admin behavior. The Django API currently differs from the FastAPI track; use this track's specification and public tests. Start with tests/ and add your own tests when useful.

## Submission and evaluation

Edit application code, add tests and document fixes. Do not alter protected evaluator files or fixtures, hardcode judge data, or bypass authentication and CSRF. Work individually under the announced tool policy.

Submit the final source ZIP in the organiser's format, including completed DEBUG_REPORT.md and SUBMISSION.json. Exclude .env, credentials, databases, virtual environments and caches. Stop editing at the official 16:00 freeze; the next 15 minutes are for collection. The organiser's timestamped ZIP is the primary submission.

DEBUG_REPORT.md should describe failures found, files changed, reasons for fixes, public tests run, remaining issues and permitted agent tools used. Evaluation checks functional, regression, boundary, concurrency and admin browser behavior. The announced ranking order is correctly resolved defects, fewer regressions, code quality and then completion time. Faculty and organisers control final policy and allowed tools.


