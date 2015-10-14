# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "Sphere Engine"
VERSION = "3.0.0"

REQUIRES = ["urllib3 >= 1.10", "six >= 1.9", "certifi", "python-dateutil", 'requests']

setup(
    name=NAME,
    version=VERSION,
    description="Sphere Engine SDK",
    author='Michal Koperkiewicz, Robert Lewon',
    author_email="contact@sphere-research.com",
    url="http://sphere-engine.com",
    keywords=['Sphere Research Labs', 'Sphere Engine', 'Online Compiler', 'Problems', 'Online Judge'],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    Sphere Engine Problems API allows you to: submit submissions to your problems, run the program with test data on server side in more than 60 programming languages and download results of the execution.
    """
)
