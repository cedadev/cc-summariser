from setuptools import setup, find_packages


__version__ = "0.0.1"
DESCRIPTION = "Summarise the results compliance-checker run on multiple datasets"


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name                 = "cc-summariser",
    version              = __version__,
    description          = DESCRIPTION,
    long_description     = readme(),
    packages             = find_packages(),
    install_requires     = [],
    tests_require        = ["pytest"],
    entry_points         = {"console_scripts": ["cc-summariser = cc_summariser:main"]}
)
