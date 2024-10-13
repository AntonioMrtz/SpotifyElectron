# ⚙️ Global Set up

In this section we will cover how to set up common tools for the whole project.


## ⚒️ Set up common project tools


### ⚓ Pre-commit

Pre-commit is used for ensuring code quality before it gets commited. When installing pre-commit hooks a check will be triggered before commiting, according to the rules specified in `.pre-commit-config.yaml`. If the check fails the commit won't be submitted.

#### 1. Install dependencies

```console
pip install -r requirements-global.txt
```

#### 2. Install pre-commits hooks

```console
pre-commit install
pre-commit install --hook-type commit-msg
```

#### 3. Force pre-commit run on all files (optional)

If you want to test pre-commit before commiting to the repository run the following command:

```console
pre-commit run --all-files
```

### 🧩 Extensions (VSCODE)

1. Open the project Backend or Frontend (each one has its own recommended extensions)
2. Go to extensions section on sidebar
3. Select filter extensions
4. Recommended
5. Workspace recommended
6. Install workspace recommended
