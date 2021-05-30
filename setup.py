#!/usr/bin/env python

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    LONG_DESC = fh.read()
    setup(
        name="slurm_to_wandb",
        version="0.1.0",
        packages=find_packages(include=["slurm_to_wandb", "slurm_to_wandb.*"]),
        entry_points={"console_scripts": ["slurm_to_wandb = slurm_to_wandb.main:main"]},
        long_description=LONG_DESC,
        long_description_content_type="text/markdown",
        license="MIT",
        author="Jeroen Overschie",
        url="https://dunnkers.com/",
        install_requires=[
            "pandas==1.2.4",
            "wandb==0.10.31",
            "numpy==1.20.2",
            "humanfriendly==9.1",
        ],
        setup_requires=["black==21.4b2", "pytest-runner==5.3.0"],
        tests_require=["pytest==6.2.3"],
    )
