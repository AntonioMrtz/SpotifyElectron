# Generate OpenAPI Schema

OpenAPI is a standard for describing and documenting APIs. It uses schemas to define API endpoints, including data types, request formats, authentication methods, and more. This allows for automatic generation of interactive documentation, facilitates API testing with mock servers, and simplifies client code generation in multiple programming languages, promoting consistency and interoperability in API development. More info on [OpenAPI docs](https://swagger.io/specification/)

1. Go to `Backend/`
2. Install app dependencies with `pip install -r requirements.txt`
3. Run `python -m app.tools.generate_openapi`
4. OpenAPI schema will be generated under `app/resources`
5. OpenAPI schema can also be found in `Electron/src/swagger` folder,
