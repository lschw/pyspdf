from setuptools import setup, find_packages
from codecs import open
import os
import re

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "pyspdf", "__init__.py")) as fh:
    version = re.match(r".*__version__ = \"(.*?)\"", fh.read(),re.S).group(1)

setup(
    name="pyspdf",
    version=version,
    description="a small and simple pdf rendered based pygtk",
    url="https://github.com/lschw/pyspdf",
    author="Lukas Schwarz",
    author_email="ls@lukasschwarz.de",
    license="GPLv3",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7"
    ],
    packages=["pyspdf"],
)

