# File requirements.txt:

```
pip install -r requirements.txt
```
* is needed for automated django test
* please add all requirements that are needed for the Django tests to this file, otherwise they won't run!!!

# Running the App

Before running the app and after installing the dependencies, doing the necessary database migrations is mandatory.
```
python manage.py migrate
```

# Running tests

```
./manage.py test
```

## Coverage

Install with pip

Execute with:
```
coverage run --source='.' manage.py test users courses fileexchange
```

Generate the html report by running:
```
coverage html
```

Look at the created report, starting at `/htmlcov/index.html`

The test coverage for the whole project is at 78%.