# Package Your Library

These files are used to package your library.

- `setup.py` is the build script for setuptools. It tells setuptools about your package (such as the name and version) as well as files to include.
- `setup.cfg` is a configuration file that can be used to set package metadata and options for various command line commands.
- `MANIFEST.in` is used to include other files in your package like the README, the tests, etc.

To create a source distribution, you run:

```bash
pip install setuptools wheel
python setup.py sdist bdist_wheel
```

The Python Package Index (PyPI) is a repository of software for Python. You can use the twine tool to upload your package to PyPI:

```bash
pip install twine
twine upload dist/*
twine upload --repository omnivore dist/* # if your tokens are set in .pypirc
```
