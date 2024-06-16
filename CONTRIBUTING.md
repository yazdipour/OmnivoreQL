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

## Release process

1. Create a new tag with the version number
2. Push the tag to GitHub
3. The release will be automatically published to PyPI

You can see how the Github Action for releasing works in the `.github/workflows/release.yml` file.