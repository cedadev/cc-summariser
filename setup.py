from setuptools import setup, find_packages
from cc_summarizer import __version__


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name                 = "cc-summarizer",
    version              = __version__,
    description          = "Summarizes JSON compliance-checker results for multiple datasets",
    long_description     = readme(),
    packages             = find_packages(),
    install_requires     = [],
    tests_require        = ["pytest"],
    entry_points         = {"console_scripts": ["cc-summarizer = cc_summarizer:main"]}
)
