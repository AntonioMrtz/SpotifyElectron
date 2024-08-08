# Testing

In this section we will cover how to run tests and develop them. Make sure `Backend/` folder is the root directory when launching the tests.


## ⚙ Previous configuration

❗ Enviroment variables defined in `.env` file will affect the execution of tests. See [enviroments](Enviroment.md) for more info.

Default configuration will only need a serverless function path if using `STREAMING_SERVERLESS_FUNCTION` for executing tests. If another architecture is selected you can run tests out of the box locally.

If the app is being executed for running test the file `pytest.ini` will override `ENV_VALUE` enviroment variable with `TEST` mode. This behaviour triggers the app to load an in-memory database instead of a real one. This can be side stepped by changing the `TEST` env value in `pytest.ini` to something like `PROD` or `DEV` **if you need a real database for testing**.

### STREAMING_SERVERLESS_FUNCTION

A valid path for a serverless function `SERVERLESS_FUNCTION_URL` is needed in enviroment variables for proper functioning.



## 🧪 Run tests

Standar test run

```
python -m pytest tests/
```

Test run and generate code coverage in folder htmlcov/index.html.

```
python -m pytest tests/ --cov=app/ --cov-report=html
```
_If your browser is in a sandbox enviroment use `python -m http.server [port]` inside `htmlcov/` folder to serve an HTTP Server._

_Its also possible to run tests using the vscode launch script **[Run tests - Pytest]**._

## 👷‍♂️ Develop tests

### Testing framework

We're using **Pytest**. Its easier, has less boilerplate than UnitTest and matches our
functions over classes develop approach for the project.

### Recommendations

- Implement features in a way that they can be testable.
- Try to use as few mocks as possible, it will help us test the actual behaviour of all the app components.


### Testing Principles

These are the principles that our tests have to follow:

- **Automation:** Tests must be able to be carried out without manual intervention.
- **Repeatable:** They must be repeatable any number of times, yielding the same results. This includes not persisting data that could influence other tests.
- **Independence:** Each test must be able to run independently, without depending on the results of other tests or functions.
- **Executable in any environment:** A test suite should be executable on any machine regardless of the environment.
- **Coverage:** Tests must cover the majority of the code.

### Testing Methodology

#### ·Setup·
- **Purpose:** This phase involves setting up the necessary preconditions and state before executing the actual test.
- **Actions:**
  - Initialize any objects or resources required for the test.
  - Set up test data or environment variables.
  - Establish connections to databases or external services if needed.
- **Example:** Before testing a function that calculates a result based on input data, you might initialize the function parameters and set up any mock objects or fixtures necessary for the test.

#### ·Execution·
- **Purpose:** This phase involves the actual execution of the test case.
- **Actions:**
  - Invoke the code or function under test with the prepared input.
  - Execute the specific functionality being tested.
- **Example:** Execute the function with the initialized parameters and capture the output or behavior that the test is evaluating.

#### ·Assertion·
- **Purpose:** This phase verifies whether the behavior or output of the executed code matches the expected result.
- **Actions:**
  - Compare the actual output or behavior of the executed code against the expected outcome.
  - Use assertions to check conditions that must be true for the test to pass.
  - Raise failures or errors if the actual result does not match the expected result.
- **Example:** Check that the result returned by the function matches the expected output based on the input parameters.

#### ·Teardown·
- **Purpose:** This phase cleans up resources or state after the test has been executed, ensuring a clean environment for subsequent tests.
- **Actions:**
  - Release any resources acquired during the setup phase.
  - Reset or revert any changes made to the environment during the test execution.
  - Close connections to databases or external services.
- **Example:** Reset global variables, close open files, or clean up temporary data created during the test execution.
