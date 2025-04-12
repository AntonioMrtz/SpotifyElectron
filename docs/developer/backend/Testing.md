# 🧪 Testing

In this section we will cover how to run tests and develop them. Make sure `Backend/` folder is the root directory when launching the tests. See more on testing principles [here](../utils/Testing-Principles.md)


## ⚙ Previous configuration

❗ Environment variables defined in `.env` file will affect the execution of tests. See [environments](Environment.md) for more info.

Default configuration will only need a serverless function path if using `SERVERLESS` for executing tests. If another architecture is selected you can run tests out of the box locally.

If the app is being executed for running test the file `pytest.ini` will override `ENV_VALUE` environment variable with `TEST` mode. This behaviour triggers the app to load an in-memory database instead of a real one. This can be side-stepped by changing the `TEST` env value in `pytest.ini` to something like `PROD` or `DEV` **if you need a real database for testing**.

### SERVERLESS(deprecated)

A valid path for a serverless function `SERVERLESS_FUNCTION_URL` is needed in environment variables for proper functioning.



## 🧪 Run tests

### Standar test run

```console
python -m pytest tests/
```

### Coverage run

Test run and generate code coverage in folder `htmlcov/index.html`.

```console
python -m pytest tests/ --cov=app/ --cov-report=html
```
_If your browser is in a sandbox environment use `python -m http.server [port]` inside `htmlcov/` folder to serve an HTTP Server with the generated coverage._

### Debug run VSCODE

In debug section launch `Run tests - Pytest`. This will run all the tests and will stop the execution on any provided breakpoints

## 👷‍♂️ Develop tests
