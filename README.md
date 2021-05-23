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

## Running the frontend tests

To run the tests, you need to install the following packages:

```
pip install selenium
```
```
pip install get-gecko-driver
```

After that, each test can be called normally.\
For example:
```
python frontend_tests/logintest.py
```
