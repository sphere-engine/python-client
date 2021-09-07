# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = 'sphere-engine'
VERSION = '0.27'

REQUIRES = ["urllib3 >= 1.10", "six >= 1.9", "certifi", "python-dateutil", 'requests']

setup(
    name=NAME,
    version=VERSION,
    description="Sphere Engine SDK",
    author='Michal Koperkiewicz, Robert Lewon',
    author_email="contact@sphere-research.com",
    url="https://github.com/sphere-engine/python-client",
    download_url="https://github.com/sphere-engine/python-client/archive/master.zip",
    keywords=['Sphere Research Labs', 'Sphere Engine', 'Online Compiler', 'Problems', 'Online Judge', 'api', 'sdk', 'online compiler', 'spoj', 'ideone'],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    Sphere Engine Problems API allows you to: submit submissions to your problems, run the program with test data on server side in more than 60 programming languages and download results of the execution.
    """
)
