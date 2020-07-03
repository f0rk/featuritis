# Copyright 2020, Ryan P. Kelly.

from setuptools import setup


setup(
    name="featuritis",
    version="0.1",
    description="feature tracking: know what features your deployed software has",
    author="Ryan P. Kelly",
    author_email="ryan@ryankelly.us",
    url="https://github.com/f0rk/featuritis",
    install_requires=[
    ],
    tests_require=[
        "pytest",
    ],
    package_dir={"": "lib"},
    packages=["featuritis"],
    scripts=["tools/featuritis"],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development",
    ],
)
