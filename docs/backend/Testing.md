# Testing

In this section we will cover how to run tests and develop them. Make sure Backend is the root directory when launching the tests.

## 🧪 Run tests

Standar test run

```
python -m pytest tests/
```

Test run and generate code coverage in folder htmlcov/index.html. If your browser is in a sandbox enviroment use `python -m http.server` inside `htmlcov/` folder
to serve an HTTP Server.

```
python -m pytest tests/ --cov=app/ --cov-report=html
```

## 👷‍♂️ Develop tests

#todo
