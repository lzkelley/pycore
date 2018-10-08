from setuptools import setup

with open('requirements.txt') as inn:
    requirements = inn.read().splitlines()

with open("README.md", "r") as inn:
    long_description = inn.read().strip()

with open('pycore/VERSION') as inn:
    version = inn.read().strip()

setup(
    name="pycore",
    version=version,
    author="Luke Zoltan Kelley",
    author_email="lzkelley@northwestern.edu",
    description=("Core structures for simulations and analysis in python."),
    license="MIT",
    keywords="",
    url="https://github.com/lzkelley/pycore/",
    packages=['pycore'],
    include_package_data=True,
    install_requires=requirements,
    long_description=long_description
)
