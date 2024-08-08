#!/usr/bin/env python

# Installation script for diffpy.nmf_mapping

"""nmf_mapping - tools for performing NMF on PDF and XRD data.
Packages:   diffpy.nmf_mapping
"""

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="diffpy.nmf_mapping",
    version="1.0.0",
    author="Simon J.L. Billinge",
    author_email="sb2896@columbia.edu",
    description="Run NMF analysis on PDF and XRD data",
    long_description=long_description,
    test_suite="tests",
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests", "applications", "examples"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": ["nmf_mapping = diffpy.nmf_mapping.nmf_mapping.main:main"],
    },
    data_files=[("", ["LICENSE.txt"])],
    url="http://www.diffpy.org/",
    download_url="http://www.diffpy.org/packages/",
    license="BSD",
    keywords="diffpy PDF NMF",
    python_requires=">=3.6",
    zip_safe=False,
)
