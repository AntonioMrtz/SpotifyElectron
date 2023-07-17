# Spotify Electron

![Spotify Electron Media Preview](https://raw.githubusercontent.com/AntonioMrtz/SpotifyElectron/master/assets/images/SpotifyElectron_MediaPreview.png)

## Software Architecture

![Spotify_Electron_Software_Diagram](assets/images/Spotify_Electron_Software_Diagram.png)


1. Clone the repository

```
git clone https://github.com/AntonioMrtz/SpotifyElectron.git
```


2. Start Electron App

```
cd SpotifyElectron/Electron
&& npm install && npm start
```

3. Start Python Backend API

```
cd Backend API && pip install -r requirements.txt && python3 -m uvicorn main:app --reload
```
**.env file is needed to access the DB**

* pip install -r requirements.txt || pip3 install -r requirements.txt [ Depends on python version installed ]
* python3 -m uvicorn main:app --reload **[ API is being deployed at http://127.0.0.1:8000/ ]**
* Access visual API swagger documentation at  **http://127.0.0.1:8000/docs**



## Project's goals

* Develop a Spotify Clone using Electron framework, Python API backend with FastAPI and React Interface.
* Add new extra functionality that could improve the original app.
* Works as a team managing Github branches, pull requests and Trello Board to organize tasks in different stages.

## How to Contribute to the project

[CONTRIBUTING readme](https://github.com/AntonioMrtz/SpotifyElectron/blob/master/.github/CONTRIBUTING.md)
