from setuptools import setup, find_packages
import subprocess

def get_latest_git_tag():
    try:
        version = subprocess.check_output(["git", "describe", "--tags", "--abbrev=0"])
        version = version.strip().decode("utf-8")  # Remove trailing newline and decode bytes to string

        # Remove the 'v' from the tag
        if version.startswith('v'):
            version = version[1:]

        return version
    except Exception as e:
        print(f"An exception occurred while getting the latest git tag: {e}")
        return None

VERSION = get_latest_git_tag() or "0.0.1"  # Fallback version

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
    packages=find_packages("omnivoreql"),
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
