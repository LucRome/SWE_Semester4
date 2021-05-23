# setup frontend tests

## python  

```
pip install selenium

pip install get-gecko-driver
```

## db 

```
./manage.py setup_tests
```

* will delete your db
* creates a new db setup for frontend tests

## executing tests

```
./manage.py runserver
```

```
cd frontend_tests

python -m unittest discover ./
```

* cook tea and wait
