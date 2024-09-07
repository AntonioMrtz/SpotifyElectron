# Testing

In this section we will cover how to run tests and develop them.

## 🧪 Run tests

Standard run

```
npm run test
```

Run test and generate coverage

```
npm run test:coverage
```

### Run only one test

1. Go to the test folder. (The cwd has to be the same as the test file)
2. Run `npx jest filename.test.tsx`

## 👷‍♂️ Develop tests

### Mock Fetch

Every request has to be mocked manually for the test to interactuate with real data. The following
code snippet can be used as a mock template for fetch requests:

```
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

```
"setupFiles": [
      "./.erb/scripts/check-build-exists.ts","./src/utils/loadOpenApiTests.ts"
    ],
```
