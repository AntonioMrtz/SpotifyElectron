# CI/CD

In this section we will cover the pourpose of our CI/CD architecture and the Github Actions workflows deployed in the repository.

## Pourpose

The Pourpose of the CI/CD implemented is automating the process of code checking for ensuring standards and quality before it reaches the production codebase. The reviewers can simply check the workflows runs made and check if the different standards are being met without to do the repetitive and time spending cicle of deploying the pull requests changes and verify it manually. These are the maing goals for our CI/CD pipelines:

* Ensure code quality using linters
* Ensure code standards
* Generating documentation

## Workflows

* Running linter for ensuring code quality and preveting bad practices
* Running style checks on the codebase for ensuring standards
* Running tests for ensuring the app works as expected
* Generate updated docs on every pull request merged
