# 🗳️ OpenAPI schema generation & usage

The generated OpenAPI schema from Backend endpoints is used in Frontend for code auto-generation that enables for code reutilization and having an up-to-date status of the endpoints. OpenAPI schema is also used in a client that encapsulates all requests on frontend and makes use of the auto-generated code.

OpenAPI is a standard for describing and documenting APIs. It uses schemas to define API endpoints, including data types, request formats, authentication methods, and more. This allows for automatic generation of interactive documentation, facilitates API testing with mock servers, and simplifies client code generation in multiple programming languages, promoting consistency and interoperability in API development. More info on [OpenAPI docs](https://swagger.io/specification/)


## Generate OpenAPI Schema (Backend)

1. Go to `Backend/`
2. Install app dependencies with `pip install -r requirements.txt`
3. Run `python -m app.tools.generate_openapi`
4. OpenAPI schema can also be found in `Electron/src/swagger` folder,

## Generate OpenAPI Client (Frontend)

1. Go to `Electron/`
2. Install app dependencies with  `npm install && npm run build`
3. Run `npm run generate-openapi-client` for generating code for backend requests based on its endpoints.
