import unittest
from setuptools import setup, find_packages


def my_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite


setup(
    name="Mancala",
    version="0.1",
    packages=find_packages(),
    test_suite='setup.my_test_suite'

)
