# Testing

In this section we will cover how to run tests and develop them. See more on testing principles [here](../utils/Testing-Principles.md).

## 🧪 Run tests

### Standard run

```console
npm run test
```

### Coverage run

Run test and generate coverage, there will be a coverage folder under `Electron/`. Open `index.html` file to get an UI for visualizing coverage.

```console
npm run test:coverage
```

### Standalone test run

Go to the test file folder. (The cwd has to be the same as the test file)

```ts
npx jest filename.test.tsx
```

### Debug run VSCODE

In debug section launch `Debug Jest Tests`. This will run all the tests and will stop the execution on any provided breakpoints

## 👷‍♂️ Develop tests


### Test interface result

For debugging the state of the interface we'll be using [Jest Preview](https://www.jest-preview.com/docs/api/debug/). This package will help us preview the state of the interface in certain point after the test finished running.

First launch Jest preview server:
```console
npx jest-preview
```

An output with the port should be logged. Launch a browser instance and go to `localhost:3336` or the output port shown after running the command:
```console
Jest Preview Server listening on port 3336
```

Select the state of the code that you want to preview and add `debug()` statement:
```ts
import { debug } from 'jest-preview'; // ---> Import this line to the test file

test('renders the component and displays title and form', async () => {
    await act(async () => {
      render(
        <StartMenu
          setIsLogged={setIsLoggedMock}
          setIsSigningUp={setIsSigningUpMock}
        />,
      );
    });

    expect(screen.getByText('Spotify Electron')).toBeInTheDocument();
    expect(
      screen.getByText('Inicia sesión en Spotify Electron'),
    ).toBeInTheDocument();
    expect(screen.getByText('Nombre de usuario')).toBeInTheDocument();
    expect(screen.getByText('Contraseña')).toBeInTheDocument();

    debug() // ---> Add this statement, the browser will reflect the state of the UI in this point
  });
```
Run tests and go to the previously opened browser instance and check the state of the UI in the last `debug` statement.


### Mock Fetch

Every request has to be mocked manually for the test to interactuate with real data. The following
code snippet can be used as a mock template for fetch requests:

```ts
global.fetch = jest.fn(async (url: string) => {
    if (url === `${Global.backendBaseUrl}/genres/`) {
      return Promise.resolve({
        json: () => JSON.stringify({ Rock: 'Rock', Pop: 'Pop' }),
        status: 200,
        ok: true,
        headers: getMockHeaders(),
      }).catch((error) => {
        console.log(error);
      });
    }
  }) as jest.Mock;
```

Note that there's two fields included in the response that can be useful/necessary in some situations:

-`headers`: inserts `application/json` headers so if they're accessed the test run doesn't crash.
-`ok`: if frontend is checking `response.ok`. (not used anymore)

### Global set up for tests

If it´s necessary to run a script before any test execution you can specify it in `package.json`file under `jest` section:

```json
"setupFiles": [
      "./.erb/scripts/check-build-exists.ts","./src/utils/loadOpenApiTests.ts"
    ],
```
