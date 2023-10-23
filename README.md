# Spotify Electron

![Spotify Electron Media Preview](https://raw.githubusercontent.com/AntonioMrtz/SpotifyElectron/master/assets/images/SpotifyElectron_MediaPreview.png)

## Website

Check our [website](https://antoniomrtz.github.io/SpotifyElectron_Web/)

## Software Architecture

![Spotify_Electron_Software_Diagram](assets/images/master-arch.png)

## API Endpoints

![Api Endpoints](assets/images/backend-endpoints.png)

## 1. Clone the repository

```
git clone https://github.com/AntonioMrtz/SpotifyElectron.git
```


## 2. Start Electron App

```
cd SpotifyElectron/Electron;
npm install;
npm start;
```

## 3. Start Python Backend API

```
cd '.\Backend API\';
pip install -r requirements.txt;
cd src/;
python3 -m uvicorn main:app --reload;
```
**.env file is needed with**

* MONGO_PASSWORD: password of mongodb database
* SECRET_KEY_SIGN: byte key for signing tokens
* Check **.env.example** for more info

**FAQ**

* pip install -r requirements.txt || pip3 install -r requirements.txt [ Depends on python version installed ]
* API is being deployed at **http://127.0.0.1:8000/**
* Access visual API swagger documentation at  
  * **Backend API/api-docs-spotify-electron.html**
  * Or deploying the app and accessing **http://127.0.0.1:8000/docs**
## 4. Tests

### Backend

```
cd Backend API/src;
python3 -m pytest -s;
```

### Frontend

```
cd Electron/;
npm run test;
```

## 5. Containerize 

### Docker

```
docker build -t spotify_electron_backend_image .

docker run -d --name spotify_electron_backend -e MONGO_PASSWORD=password SECRET_KEY_SIGN=secret-key-sign -p 8000:8000 spotify_electron_backend_image

```

---


## Project's goals

* Develop a Spotify Clone using Electron framework, Python API backend with FastAPI and React Interface.
* Frontend and Backend testing
* Work with AWS services
* Add new extra functionality that could improve the original app.
* Works as a team managing Github branches, pull requests,Github Actions and Trello Board to organize tasks in different stages.

## How to Contribute to the project

[CONTRIBUTING readme](https://github.com/AntonioMrtz/SpotifyElectron/blob/master/.github/CONTRIBUTING.md)

## Walkthrough

### Home

![Home](assets/images/Walkthrough/Home.png)

### Playlist

![Home](assets/images/Walkthrough/Playlist.png)

### Upload Song

![Home](assets/images/Walkthrough/UploadSong.png)

### Explorar

![Explorar](assets/images/Walkthrough/Explorar.png)

### Login

![Login](assets/images/Walkthrough/Login.png)


### Update Playlist

![Home](assets/images/Walkthrough/UpdatePlaylist.png)


