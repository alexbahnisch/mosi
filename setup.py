#!/usr/bin/env python
from setuptools import find_packages, setup
from sys import argv

long_description = "!!! pypandoc and/or pandoc not found, long_description is bad, don't upload this to PyPI !!!"

if any(arg in argv for arg in ["sdist", "bdist_wheel"]):
    try:
        # noinspection PyPackageRequirements,PyPackageRequirements
        from pypandoc import convert, download_pandoc

        download_pandoc()
        long_description = convert("README.md", "rst")

    except (ImportError, OSError):
        pass

setup(
    name="mosi",
    version="0.0.4.dev2",
    description="Modelling & Optimization Solver Interface (MOSI).",
    url="https://github.com/alexbahnisch/mosi.py",
    author="Alex Bahnisch",
    author_email="alexbahnisch@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython"
    ],
    keywords="optimization",
    packages=find_packages("src/main"),
    package_dir={"": "src/main"},
    python_requires=">=3.5",
    install_requires=[
        "pyplus>=0.1.5"
    ],
    setup_requires=[
        "pypandoc>=1.4<2"
    ],
    tests_require=[
        "pytest>=3.2.3,<4",
        "pytest-runner>=2.12.1,<3"
    ],
    test_suite="src.tests"
)
