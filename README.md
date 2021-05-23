![](logo_eCourse.png)
# eCourse

A replacement for moodle and dualis.

## Installing

Change inside the `eCourse_backend` directory and then run:

```
python -m venv venv
```
After the creation of the virtual environment, enter it:

Windows: TODO  
Unix: `source venv/bin/activate`

Before running the project, you need to install the needed dependencies:
```
pip install -r requirements.txt
```

Then you need to setup the database

```
./manage.py migrate
```

Finally, apply the permissions and groups:

```
./manage.py loadperms groups.yml
```

## Running the django project

You can run the django project with the built in webserver via:

```
python eCourse_backend/manage.py runserver
```

## tests coverage

```
coverage run -p ./frontend_tests/frontend_tests_helper.py
coverage run -p eCourse_backend/manage.py test ./
coverage combine
coverage report
```