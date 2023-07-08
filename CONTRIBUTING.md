# Contributing

Thanks for helping to makeing this project better!

We welcome all kinds of contributions:

- Bug fixes
- Documentation improvements
- New features
- Refactoring & tidying

## Getting started

If you have a specific contribution in mind, be sure to check the **issues and pull requests** in progress - someone could already be working on something similar
and you can help out.

## Project setup

### Development with virtualenv (recommended)

After cloning this repo, create a virtualenv:

```console
python -m venv .venv
```

Activate the virtualenv and install dependencies by running:

```console
python -m pip install -r requirements.txt
```

## How to create a good Pull Request

1. Make a fork of the master branch on github
2. Clone your forked repo on your computer
3. Create a feature branch `git checkout -b feature_my_awesome_feature`
4. Modify the code
5. Verify that the [Coding guidelines](#coding-guidelines) are respected
6. Verify that the [automated tests](#running-tests) are passing
7. Make a commit and push it to your fork
8. From github, create the pull request. Automated tests from GitHub actions
and codecov will then automatically run the tests and check the code coverage
9. If other modifications are needed, you are free to create more commits and
push them on your branch. They'll get added to the PR automatically.

Once the Pull Request is accepted and merged, you can safely
delete the branch (and the forked repo if no more development is needed).