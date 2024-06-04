Execute these commands in the terminal:

POSTGRESQL
-Create lac_db in postgre / pg admin

- `py -m venv .venv`
- `source .venv/Scripts/activate`
- `py -m pip install Django`
- `pip install "psycopg[binary]"`
- `cd lac/`
- `py manage.py makemigrations`
- `py manage.py migrate`
- `py manage.py runserver`
