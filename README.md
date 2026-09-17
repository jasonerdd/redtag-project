<<<<<<< HEAD
# Red Tag System

Django web app that replaces the Assembly Red Tag Report Excel workbook. Capture, store, search, close, and export red tag records on a local server with PostgreSQL.

## Features

- Create / edit / close red tags (Pending `P` / Closed `C`)
- Vehicle, dealer, model, section, station, category, and staff lookups
- Dashboard with counts and top issue/station/section summaries
- Filter, search, and Excel export
- Import historical data from `Red Tag Report 2024.xlsx`
- Django admin for master data maintenance

## Setup (Windows)

1. Create and activate a virtualenv, then install dependencies:

```bash
python -m venv venv
source venv/Scripts/activate   # Git Bash
pip install -r requirements.txt
```

2. Copy `.env` values for PostgreSQL (`DB_NAME`, `DB_USER`, `DB_PASSWORD`, etc.).

3. Create the database (once):

```bash
psql -U postgres -c "CREATE DATABASE redtag_db;"
```

4. Migrate and create an admin user:

```bash
python manage.py migrate
python manage.py createsuperuser
```

5. Import Excel lookups + historical tags:

```bash
python manage.py import_excel "Red Tag Report 2024.xlsx"
```

Use `--skip-tags` for lookups only, or `--limit 500` for a sample import.

6. Run the app:

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/ and sign in.

## Local server deployment

On the company server:

1. Install Python 3.12+, PostgreSQL, and dependencies.
2. Set `DEBUG=False` and a strong `SECRET_KEY` in `.env`.
3. Set `ALLOWED_HOSTS` to the server hostname/IP.
4. Collect static files: `python manage.py collectstatic`
5. Run with a production WSGI server (IIS + HttpPlatformHandler, Waitress, or Nginx + Gunicorn on Linux).

## Excel column mapping

| Excel column | System field |
|---|---|
| Date | date_raised |
| Section | section |
| Dealer | vehicle.dealer |
| Model | vehicle.model |
| Lot | vehicle.lot |
| Chassis no. | vehicle.chassis_no |
| Part Number / Part Name / Qnty | part fields |
| Issue Description | issue_description |
| Category / Issue Type | category / issue_type |
| Raised By | raised_by (employee no) |
| Station | station |
| Status (P/C) | status |
| Closing Date / Cleared By | closing_date / verified_by |
| Location (EOL/FINAL) | location |
=======
# redtag-project
>>>>>>> 54586409c90b7624187bc6d4303db7b09377ad29
