# HOW TO CONTRIBUTE

## STEPS TO CONTRIBUTE

1. Create a new branch with the feature youre implementing with the name convention type/BranchName [ej : feat/Home , fix/UserLogin]
2. Push your changes to the new branch with one of the following prefix:
  - `feat`: indicates the addition of a new feature or functionality to the project.
  - `fix`: used when fixing a bug or error in the code.
  - `docs`: changes to the documentation
  - `style`: formatting, missing semi colons, etc; no production code change
  - `refactor`: refactoring production code, eg. renaming a variable
  - `test`: adding missing tests, refactoring tests; no production code change
  - `chore`: updating grunt tasks etc; no production code change
  - `ci`: updating scripts for continuous integration
  - `build`: update building scripts or Docker Images
  - `perf`: update code for performance improvement
  - `revert`: revert changes
  - `docs`: Used when making changes or improvements to the project's documentation.
3. Add tests for every change you made.
4. Go to your branch in Git and then select Pull Request and field the fields indicated in the template.
5. Check if Github Actions CI tests are passing, any pull request with errors on CI would not be merged to the master branch.
6. The owner of the project will check the Pull Request and then merge it with the main branch.

## STYLE GUIDE

* The new branch name must be the feature that is going to be implemented.
* Fill the fields of the pull_request_template.

## TOOLS

* There are recommended extensions for VS Code inside both backend and frontend. Refer to their respective documentation for installation.

## MUST-HAVE SOFTWARE

* Node >= v20.12.2
* Python >= 3.11
* Git
