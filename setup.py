import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="isitornot",
    version="1.1.1",
    author="Trevor R.H. Clarke",
    author_email="trevor@notcows.com",
    description=("Common utilities, etc. for IsItOrnot",),
    license="GPL3",
    long_description=read('README.md'),
    packages=find_packages(),
    include_package_data=True
)
