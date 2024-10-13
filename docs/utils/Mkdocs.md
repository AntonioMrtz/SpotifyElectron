# 🗐 Mkdocs development & usage

Project documentation will be deployed at `https://antoniomrtz.github.io/SpotifyElectron/`.

MkDocs is a static site generator specifically designed for creating project documentation. Written in Python, it allows developers to build and deploy documentation websites with ease. It uses Markdown for writing content, supports custom themes, and integrates well with version control systems like Git. With its simple configuration and built-in support for search, MkDocs is a popular choice for creating professional, easy-to-maintain documentation sites. More info [here](https://www.mkdocs.org/)

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
python3.11 -m venv venv &&
source venv/bin/activate &&
pip install -r requirements-docs.txt
```

## 🟩 Deployment

There's a pipeline that pushes the latest documentation files into the prodution website. For manual deployment run:

```console
python -m mkdocs gh-deploy
```

## 🟧 Development

1. Run the hot reload server `python -m mkdocs serve`
2. The website will be located at `http://127.0.0.1:8000/`. Every change you make in the documentation will be shown in the website.
