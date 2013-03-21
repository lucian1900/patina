from os.path import join, dirname
from setuptools import setup, find_packages


with open(join(dirname(__file__), 'requirements.txt')) as f:
    requirements = [x.strip() for x in f.readlines()]


setup(
    name='patina',
    version='0.1',
    description='Not quite rust',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'patina=patina:main',
        ]
    },
    install_requires=requirements,
    zip_safe=False,
)
