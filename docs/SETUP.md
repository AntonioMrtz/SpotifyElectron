# Common Set up

In this section we will cover how to set up common tools for the whole project.


## 🛠 Set up common project tools

### ⚓ Pre-commit

Pre-commit is used for ensuring code quality before it gets commited. When you install pre-commit hooks a check will be triggered before commiting ensuring the rules specified in `.pre-commit-config.yaml`, if the check fails the commit wont be submitted. By default pre-commit will check the linting and formatting of the code that its going to be commited.

### 1. Install dependencies

```
pip install -r requirements-commons.txt
```


#### 2. Install pre-commits hooks

```
pre-commit install
```

#### 3. Force pre-commit run on all files (optional)

If you want to test pre-commit before commiting to the repository run the following command:

```
pre-commit run --all-files
```
