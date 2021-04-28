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
coverage run ./*/tests.py --settings=test_sqlite --parallel=1
```
oder so ähnlich. noch nicht ganz sicher tbh

Generate the html report by running:
```
coverage html
```

Look at the created report, starting at `/htmlcov/index.html`
