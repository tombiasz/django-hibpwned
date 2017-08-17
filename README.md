# django-hibpwned
Django (>=1.9) password validator based on haveibeenpwned.com API

## Requirements

```
Python 3.5+
Django 1.9+
requests 2+
```

## Installation

```
pip install django-hibpwned
```

## Usage

Add to settings.py:

```
AUTH_PASSWORD_VALIDATORS = [
    (...)
    {
        'NAME': 'haveibeenpwned.validators.HaveIBeenPwnedValidator'
    },
]
```
[reference](https://docs.djangoproject.com/en/1.9/topics/auth/passwords/#module-django.contrib.auth.password_validation)

## Tests

To run the test suite create and activate a virtual environment. Then install some requirements and run the tests:

```
$ cd tests
$ pip install -e ..
$ ./runtests.py
```

## Credits:

1. [Troy Hunt](https://www.troyhunt.com/)
2. [HaveIBeenPwned.com](https://haveibeenpwned.com/)
3. [Django](https://www.djangoproject.com/)
4. [Requests](http://docs.python-requests.org/en/master/)
