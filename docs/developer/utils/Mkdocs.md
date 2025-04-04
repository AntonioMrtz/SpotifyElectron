# 🗐 Mkdocs development & usage

Project documentation will be deployed at `https://antoniomrtz.github.io/SpotifyElectron_Web/docs/`.

MkDocs is a static site generator specifically designed for creating project documentation. Written in Python, it allows developers to build and deploy documentation websites with ease. It uses Markdown for writing content, supports custom themes, and integrates well with version control systems like Git. More info [here](https://www.mkdocs.org/)

## 🔨 Set up

1. Go to root folder of the project
2. Create virtual environment and install dependencies

🪟 **Windows**
```console
python -m venv venv;
venv/Scripts/activate;
pip install -r requirements-docs.txt
```

🐧 **Linux**
```console
python3.12 -m venv venv &&
source venv/bin/activate &&
pip install -r requirements-docs.txt
```

## 🟩 Deployment

Generated MkDocs static files are deployed on this [URL](https://antoniomrtz.github.io/SpotifyElectron_Web/docs/) when a Pull Request is merged on master branch or the deploy documentation pipeline action is triggered manually. This integration is done by one Github Action that triggers the deployment of the website on the [website repository](https://github.com/AntonioMrtz/SpotifyElectron_Web).

## 🟧 Development

1. Run the hot reload server `python -m mkdocs serve`
2. The website will be located at `http://127.0.0.1:8000/`. Every change you make in the documentation will be shown in the website.
