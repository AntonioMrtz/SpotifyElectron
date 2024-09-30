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

## 2. Backend Configuration

Select backend enviroment values as shown in [PRODUCTION ENVIRONMENT](../backend/Environment.md)


## 3. Generate release Github

* Generate release in [Github releases](https://github.com/AntonioMrtz/SpotifyElectron/releases/new)
* Create tag
* Link code commit with release tag


## 4. Packaged app

* Follow [packaging guide](../frontend/Package-app.md) using production backend URL and architecture.
* Upload exectuables to [Github releases](https://github.com/AntonioMrtz/SpotifyElectron/releases)

## 5. Prepare database

* Prepare data sets
* Delete non compatible data with new version in database

## 6. Deploy backend cloud service

* Select commit to deploy on cloud

## 7. Misc updates

* [Website](https://github.com/AntonioMrtz/SpotifyElectron_Web)
* Linkedin
* Portfolio
* Github readme and docs
