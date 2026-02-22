# OmnivoreAPI：Omnivore API 的 Python 客户端

**中文 | [English](README.md)**

**Forked from [OmnivoreQL](https://github.com/yazdipour/OmnivoreQL)**

本项目是 [Omnivore API](https://omnivore.app) 的 Python 客户端。

<!-- [![Tests](https://github.com/Benature/OmnivoreAPI/actions/workflows/test.yml/badge.svg)](https://github.com/Benature/OmnivoreAPI/actions/workflows/test.yml) -->
[![PyPI version](https://badge.fury.io/py/omnivore_api.svg)](https://pypi.org/project/omnivore_api/)

## 安装

```bash
pip install omnivore_api
```

## CLI

安装后，终端中即可使用 `omnivore` 命令。

### 初始化配置

```bash
omnivore init
```

按提示输入 API Token 和 Endpoint URL，配置将写入 `~/.config/omnivore-api/config.yaml`。

### 命令列表

```bash
# 保存 URL（可选添加标签）
omnivore save-url https://example.com
omnivore save-url https://example.com --label 阅读 --label python

# 获取收件箱文章
omnivore get-articles
omnivore get-articles --limit 20 --query "in:inbox" --format markdown

# 获取个人信息
omnivore get-profile

# 获取所有标签
omnivore get-labels
```

所有命令均输出 JSON 到标准输出，可配合 `jq` 使用：

```bash
omnivore get-labels | jq '.[].name'
```

## Python API

导入并创建客户端实例：

```python
from omnivore_api import OmnivoreAPI

omnivore = OmnivoreAPI("your_api_token_here", "your_api_url_here")
```

```python
profile = omnivore.get_profile()

saved_page = omnivore.save_url("https://www.google.com")
saved_page_with_label = omnivore.save_url("https://www.google.com", ["label1", "label2"])

articles = omnivore.get_articles()

username = profile['me']['profile']['username']
slug = articles['search']['edges'][0]['node']['slug']
article = omnivore.get_article(username, slug)

subscriptions = omnivore.get_subscriptions()

labels = omnivore.get_labels()
from omnivore_api import CreateLabelInput
omnivore.create_label(CreateLabelInput("label1", "#00ff00", "标签描述"))
```

## 文档

* Omnivore GraphQL Schema：[schema.graphql](https://github.com/omnivore-app/omnivore/blob/main/packages/api/src/schema.ts)
* 贡献指南：[CONTRIBUTING.md](docs/CONTRIBUTING.md)
* 发布流程：[RELEASE.md](docs/RELEASE.md)、[PYPI.md](docs/PYPI.md)

<!-- ## 支持

如果本项目对你有帮助，欢迎通过赞助支持维护。 -->

<!-- [![GitHub stars](https://img.shields.io/github/stars/Benature/omnivore_api.svg?style=social&label=Star)](https://github.com/Benature/omnivore_api/stargazers)
[![Github Sponsor](https://img.shields.io/static/v1?label=Sponsor&message=%E2%9D%A4&logo=GitHub&color=%23fe8e86)](https://github.com/sponsors/Benature) -->

## 许可证

本项目基于 MIT 许可证，详见 [LICENSE](LICENSE)。

<!-- ## Star 历史 -->

<!-- [![Star History Chart](https://api.star-history.com/svg?repos=Benature/OmnivoreAPI&type=Date)](https://star-history.com/#Benature/OmnivoreAPI&Date) -->
