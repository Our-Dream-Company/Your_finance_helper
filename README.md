# Your_finance_helper

This is my pet project of financial accounting. He is a working prototype.

I used the following technology stack: **Django, PostgresQL, Docker, Docker-Compose and other(you can see in requurements.txt)**

Django applications includes:

1. [authentication](https://github.com/Our-Dream-Company/Your_finance_helper/tree/master/your_finance_helper/authentication)
2. [main_page](https://github.com/Our-Dream-Company/Your_finance_helper/tree/master/your_finance_helper/main_page)
3. [reports](https://github.com/Our-Dream-Company/Your_finance_helper/tree/master/your_finance_helper/reports)

Financial assistant project development

1. download PostgresQL and install from https://www.postgresql.org/download/

2. Create a virtual environment using the command - python -m venv sand\_(you can give any name)

3. run your virtual environment . ../Scripts/activate

4. use - pip install -r requirements.txt

5. click Cntl+Shift+P and choose Python:Select Interpreter>Python from virtual environment(for VScode)

6. use - python manage.py makemigrations

- after use - python manage.py migrate

6. use - python manage.py loaddata main_page_data.json

7. If you need admin control(http://127.0.0.1:8000/admin), you can create superuser using the command python manage.py createsuperuser
