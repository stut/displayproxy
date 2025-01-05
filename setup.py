#!/usr/bin/env python
import os
import sys
from codecs import open

from setuptools import setup

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 6)

if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write(
        """
==========================
Unsupported Python version
==========================
This version of DisplayProxy requires at least Python {}.{}, but
you're trying to install it on Python {}.{}. To resolve this,
consider upgrading to a supported Python version.
""".format(*(REQUIRED_PYTHON + CURRENT_PYTHON)))
    sys.exit(1)


# 'setup.py publish' shortcut.
if sys.argv[-1] == "publish":
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")
    sys.exit()

requires = [
    "pillow>=11.1.0",
    "inky>=1.5.0",
    "pygame>=2.6.1",
]
test_requirements = [
]

about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "src", "displayproxy", "__version__.py"), "r", "utf-8") as f:
    exec(f.read(), about)

with open("README.md", "r", "utf-8") as f:
    readme = f.read()

setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    packages=["displayproxy"],
    package_data={"": ["LICENSE", "NOTICE"]},
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=requires,
    license=about["__license__"],
    zip_safe=False,
    # TODO: Fill this out!
    classifiers=[],
    tests_require=test_requirements,
    extras_require={},
    project_urls={
        # TODO: Change this URL when the docs are live
        "Documentation": "https://go.stut.net/displayproxy",
        "Source": "https://github.com/stut/displayproxy",
    },
)
