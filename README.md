# Your_finance_helper

This is my pet project of financial accounting. It's working prototype.

I used the following technology stack:

```
- Django
- PostgreSQL
- Psycopg2
- Docker
- Docker-Compose
- Gunicorn
- Pytest
```

Django applications includes:

1. [authentication](https://github.com/Our-Dream-Company/Your_finance_helper/tree/master/your_finance_helper/authentication)
2. [main_page](https://github.com/Our-Dream-Company/Your_finance_helper/tree/master/your_finance_helper/main_page)
3. [reports](https://github.com/Our-Dream-Company/Your_finance_helper/tree/master/your_finance_helper/reports)

## Usage

1. Request an env file from me (contacts will be below).
2. Run services:
   `docker-compose up --build`

If you see an error in your Docker
`your_finance_helper_web_1 exited with code 1`
you need change in [entrypoint.sh](https://github.com/Our-Dream-Company/Your_finance_helper/blob/master/your_finance_helper/entrypoint.sh) from _CRLF_ to _LF_.

## Authentication

I used the standard Django classes for authentification. It includes:

**login/logout:**

![](https://github.com/Our-Dream-Company/Your_finance_helper/blob/master/images/1_login.jpg)

**password change:**

![](https://github.com/Our-Dream-Company/Your_finance_helper/blob/master/images/3_change_password.jpg)
![](https://github.com/Our-Dream-Company/Your_finance_helper/blob/master/images/3_change_password_completed.jpg)

**password reset:**

![](https://github.com/Our-Dream-Company/Your_finance_helper/blob/master/images/2_reset_password.jpg)
![](https://github.com/Our-Dream-Company/Your_finance_helper/blob/master/images/3_reset_password_meassage_to_email.jpg)

**registration:**

![](https://github.com/Our-Dream-Company/Your_finance_helper/blob/master/images/4_registration.jpg)

I have used my own templates in this application. Authentication is designed in such a way, so information about income / expenses is displayed for each individual registered user..

## Main page

In this application, you can see:

- Records of your income / expenses in a readable form by sections, categories and names of the operation.
- Balance from the beginning of the month to the current date.
- Information in the period of interest by dates.

When user see this page first time, the following information will be displayed in front of him:
![](https://github.com/Our-Dream-Company/Your_finance_helper/blob/master/images/5_main_page.jpg)

If the user adds _income_
![](https://github.com/Our-Dream-Company/Your_finance_helper/blob/master/images/6_add_income.jpg)

or _outcome_
![](https://github.com/Our-Dream-Company/Your_finance_helper/blob/master/images/6_add_outcome.jpg)

on the _main page_, he can see this data immediately in main page:
![](https://github.com/Our-Dream-Company/Your_finance_helper/blob/master/images/5_main_page1.jpg)

I am using my own [module](https://github.com/Our-Dream-Company/Your_finance_helper/blob/master/your_finance_helper/main_page/split_queryset.py) for human readable output.

## Reports

This application store reports from the _main page application, savings, a list of planned expenses_. At the moment, the _main page_ application report has been implemented.
![](https://github.com/Our-Dream-Company/Your_finance_helper/blob/master/images/7_reports_buttons.jpg)

In the application report of the main page, the user can see the detailed information about the transaction. The also user can select period for information about transactions.
![](https://github.com/Our-Dream-Company/Your_finance_helper/blob/master/images/7_reports_detailed.jpg)

He can immediately select the desired transaction and update or delete it.
![](https://github.com/Our-Dream-Company/Your_finance_helper/blob/master/images/7_reports_detailed_for_one.jpg)

The meaning of the reports application is that the user can update and delete transactions from all other applications.

Removal is done by changing the **enabled** field of the [model](https://github.com/Our-Dream-Company/Your_finance_helper/blob/master/your_finance_helper/main_page/models.py) from _False_ to _True_. The record remains in the database, but is invisible to the user.

## Test

My application Your_finance_helper has [tests](https://github.com/Our-Dream-Company/Your_finance_helper/tree/master/your_finance_helper/tests). Tests are written with a pytest.
At the moment, the test coverage is 99%.
![](https://github.com/Our-Dream-Company/Your_finance_helper/blob/master/images/8_test_coverage.jpg)

## Contacts

- Instagram: [@igor*komkov*](https://www.instagram.com/igor_komkov_/)
- Vk.com: [Igor Komkov](https://vk.com/zzzscadzzz)
- Linkedin: [Igor Komkov](https://www.linkedin.com/in/igor-komkov/)
- email: **scad200@gmail.com**
