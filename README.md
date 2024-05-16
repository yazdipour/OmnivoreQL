# OmnivoreQL: Omnivore API client for Python

![OmnivoreQL Icon](https://github.com/yazdipour/OmnivoreQL/assets/8194807/d51d462d-4f5a-4031-980e-1faa5ca3f6e0)

This is a Python client for the [Omnivore API](https://omnivore.app).

[![GitHub stars](https://img.shields.io/github/stars/yazdipour/omnivoreql.svg?style=social&label=Star)](https://github.com/yazdipour/omnivoreql/stargazers)
[![Github Sponsor](https://img.shields.io/static/v1?label=Sponsor&message=%E2%9D%A4&logo=GitHub&color=%23fe8e86)](https://github.com/sponsors/yazdipour)

[![Tests](https://github.com/yazdipour/OmnivoreQL/actions/workflows/test.yml/badge.svg)](https://github.com/yazdipour/OmnivoreQL/actions/workflows/test.yml)
[![PyPI version](https://badge.fury.io/py/omnivoreql.svg)](https://pypi.org/project/omnivoreql/)

## Setup

To use `omnivoreql` in your Python project, install the `omnivoreql` package using either [pip](#pip) or [poetry](#poetry).

### pip

```bash
pip install omnivoreql
```

### poetry

Install [Poetry](https://python-poetry.org/docs/).

```bash
# use working directory virtual environment
poetry config virtualenvs.in-project true

# install dependencies and setup virutal environment
poetry install

# activate virtual environment
poetry shell
```

## Quickstart

Import the package into your project and Create a new instance of the client:

```python
from omnivoreql import OmnivoreQL

omnivoreql_client = OmnivoreQL("your_api_token_here")
```

Use the methods of the OmnivoreQL class to interact with the Omnivore API. 

```python
profile = omnivoreql_client.get_profile()

result = omnivoreql_client.save_url("https://www.google.com")

articles = omnivoreql_client.get_articles()

username = profile['me']['profile']['username']
slug = articles['search']['edges'][0]['node']['slug']
articles = omnivoreql_client.get_article(username, slug)

labels = omnivoreql_client.get_labels()
subscriptions = omnivoreql_client.get_subscriptions()
```

## Development

In addition to using [poetry](#poetry), `asdf` can be used to manage python runtimes. Follow the [official instructions](https://asdf-vm.com/guide/getting-started.html#_2-download-asdf) to install `asdf`.

Then install the python and/or poetry [runtimes](#runtimes), respectively.

### Runtimes
#### Python
```bash
# add python plugin
asdf plugin-add python

# install python
asdf install python 3.11.4  # <version|latest>
```

#### Poetry
```bash
# Add poetry asdf plugin
asdf plugin-add poetry https://github.com/asdf-community/asdf-poetry.git

# Install latest version via asdf
asdf install poetry 1.5.1   # <version|latest>
```
