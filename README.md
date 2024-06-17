

POSTGRESQL
-Create lac_db in postgre / pg admin

Execute these commands in the terminal:
VSCODE TERMINAL
- `py -m venv .venv`
- `source .venv/Scripts/activate`
- `py -m pip install Django`
- `pip install "psycopg[binary]"`
- `pip install pillow`
- `cd lac/`
- `py manage.py createsuperuser`
- `py manage.py makemigrations`
- `py manage.py migrate`
- `py manage.py runserver`


UPLOADING FILES IN BRANCH COLLAB

- `git checkout collab`
- `git add .`
- `git commit -m "Message"`
- `git commit -m "Message"`
- `git push origin -m "Message"`

MERGE BRANCH
- `git merge 'branch'`
- `git push origin 'branch'`

