# Omnivore API client for Python

## To install

```
pip install omnivore_api
```
## Package Your Library

These files are used to package your library.

- `setup.py` is the build script for setuptools. It tells setuptools about your package (such as the name and version) as well as files to include.
- `setup.cfg` is a configuration file that can be used to set package metadata and options for various command line commands.
- `MANIFEST.in` is used to include other files in your package like the README, the tests, etc.

To create a source distribution, you run:

```
python setup.py sdist
```

The Python Package Index (PyPI) is a repository of software for Python. You can use the twine tool to upload your package to PyPI:

```
pip install twine
twine upload dist/*
```