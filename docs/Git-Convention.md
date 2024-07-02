# Git Convention

In this document we will cover the convention applied to git usage in the project.

## Branches

- The main branch of the project is `master`. All pull request will be created towards `master` branch.
- `gh-pages` branch whill host the documentation for the project and will only update using CI. This CI will be trigger when a pull request is merged into `master`.

## Branch convention

For naming branch we will use the next convention:

`prefix/BranchName`

- Prefix: select one of the prefixes listed below.
- BranchName: the feature that is going to be implemented.

Examples:

- `feat/Home-Page`
- `fix/User-Login`

## Commit convention

For commiting into the repository the next convention has to be applied:

`prefix: changeMade`

- Prefix: select one of the prefixes listed below.
- ChangeMade: the change that has been implemented. In present tense.

Examples:

- feat: add Home Page
- fix: remove failing user login authentication

## Pull Request convention

After creating your Pull Request rename the title with a descriptive summary of the changes.

Example:

- Add Home Page
- Remove User failing login Authentication
- Refactor backend song service
- Update git contributing documentation

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
- `docs`: Used when making changes or improvements to the project's documentation.
