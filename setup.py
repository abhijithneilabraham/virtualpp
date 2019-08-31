#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 23:27:34 2019

@author: abhijithneilabraham
"""


import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="virtualpp",
    version="0.0.7",
    author="Abhijith Neil Abraham",
    author_email="abhijithneilabrahampk@gmail.com",
    description="An opencv based virtual pingpong",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abhijithneilabraham/PINGPONG-hand",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
