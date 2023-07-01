from setuptools import setup, find_packages
import os

# Get version from __version__.py file
current_folder = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(current_folder, "omnivoreql", "__version__.py")) as f:
    exec(f.read(), about)

setup(
    name='omnivoreql',
    version=about["__version__"],
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
    classifiers=[
        "Development Status :: 3 - Alpha",
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
