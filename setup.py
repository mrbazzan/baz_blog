
# project description and the files that belong to the project.
from setuptools import find_packages, setup

setup(
    name='bazblog',
    version='1.0.1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'pytest',
        'coverage',
    ],
)
