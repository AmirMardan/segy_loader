from setuptools import setup, find_packages

setup(
    name='segy_loader',
    version = "0.0.1",
    description = "A package to perform first break",
    long_description = open("readme.md", 
                            encoding="utf8").read(),
    author='Amir Mardan',
    uthor_email = "mardan.amir.h@gmail.com",
    license = "MIT",
    packages=find_packages(exclude=["*.pyc"]),
    include_package_data=True,
    package_data={
        "": ["*.so"],
        },
    install_requires=[
        'numpy',
        'matplotlib',
    ],
    entry_points={
        'console_scripts': [
            'segy_loader=segy_loader.cli:main',
        ],
    },
)