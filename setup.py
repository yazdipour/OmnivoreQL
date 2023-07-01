from setuptools import setup, find_packages

setup(
    name='omnivoreql',
    version='0.1',
    description='A library to interact with the Omnivore API',
    author='Shahriar Yazdipour',
    author_email='git@yazdipour.com',
    packages=find_packages(),
    install_requires=[
        'gql==3.4.1',
        'requests-toolbelt==1.0.0'
    ],
)
