from setuptools import setup, find_packages

VERSION = "0.2.3.1"
PROJECT_URLS = {
    "Bug Tracker": "https://github.com/yazdipour/OmnivoreQL/issues",
    "Source Code": "https://github.com/yazdipour/OmnivoreQL",
}

setup(
    name='omnivoreql',
    version=VERSION,
    description='Omnivore API Client for Python',
    author='Shahriar Yazdipour',
    author_email='git@yazdipour.com',
    packages=find_packages(),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="omnivore api readlater graphql gql client",
    platforms="any",
    url="https://github.com/yazdipour/OmnivoreQL",
    project_urls=PROJECT_URLS,
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        'gql==3.4.1',
        'requests-toolbelt==1.0.0'
    ],
)
