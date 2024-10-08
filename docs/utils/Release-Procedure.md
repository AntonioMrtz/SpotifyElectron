# Release procedure

## 1. Update release version info on codebase

### Frontend

Update `package.json` version in:

* `Electron/package.json`
* `Electron/release/app/package.json`

```json
{
  "name": "spotify-electron",
  "version": "1.0.0",
  ...
}
```

### Backend

Update FastAPI backend version on `Backend/app/common/app_schema.py`

```py
class AppInfo:
    ...
    VERSION = "1.0.0"
    ...
```

## 2. Generate release Github

* Generate release in [Github releases](https://github.com/AntonioMrtz/SpotifyElectron/releases/new)
* Create tag
* Link code commit with release tag


## 3. Package app

* Follow [packaging guide](../frontend/Package-app.md) using production backend URL and architecture.
* Upload exectuables to [Github releases](https://github.com/AntonioMrtz/SpotifyElectron/releases)

## 4. Prepare database

* Prepare data sets
* Delete non compatible data with new version in database

## 5. Deploy backend cloud service

* Select commit to deploy on cloud
* Check environment values are consistent with [PRODUCTION ENVIRONMENT](../backend/Environment.md)

## 6. Misc updates

* [Website](https://github.com/AntonioMrtz/SpotifyElectron_Web)
* Linkedin
* Portfolio
* Github readme and docs
