# Git Convention

In this document we will cover the convention applied to git usage in the project.

## Branches

- The main branch of the project is `master`. All pull requests will be created towards `master` branch.
- `gh-pages` branch will host the documentation for the project and will only update using CI. This CI will be triggered when a pull request is merged into `master`.

## Branch convention

We will use the next convention for branch names:

`prefix/IssueNumber-IssueTitle`

- Prefix: select one of the prefixes listed below.
- IssueNumber: the issue number associated with the branch.
- IssueTitle: the title of the issue.

Examples:

```
Issue:

issue-title: Add Home Page
issue-number: #7777
```

- feat/7777-Add-Home-Page

## Commit convention

In order to commit into the repository the next convention has to be applied:

`prefix: changeMade`

- Prefix: select one of the prefixes listed in `Naming convention prefixes` section at the end of this document.
- ChangeMade: the change that has been implemented. In present tense.

Examples:

- feat: add Home Page
- fix: remove failing user login authentication

_pre-commit will insert the issue number if the branch name follows the convention_

## Pull Request convention

After creating your Pull Request rename the title with the issue title and its number:

`#issue-number: IssueTitle`

Examples:

```
Issue:

issue-title: Add Home Page
issue-number: #7777
```

- \#7777: Add Home Page

## Naming convention prefixes

- `feat`: indicates the addition of a new feature or functionality to the project.
- `fix`: used when fixing a bug or error in the code.
- `docs`: changes to the documentation.
- `style`: formatting, missing semi colons, etc; no production code change.
- `refactor`: refactoring production code, eg. renaming a variable.
- `test`: adding missing tests, refactoring tests; no production code change.
- `chore`: updating grunt tasks etc; no production code change.
- `ci`: updating scripts for continuous integration.
- `build`: update building scripts or Docker Images.
- `perf`: update code for performance improvement.
- `revert`: revert changes.
- `release`: only for release versions.
