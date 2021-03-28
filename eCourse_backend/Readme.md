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