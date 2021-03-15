from setuptools import setup
from maltego_stix2 import VERSION

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

dependencies = [
    'Pillow==8.1.1',
    'maltego-trx==1.3.8',
    'stix2==2.1.0',
    'python-dateutil==2.8.1'
]

setup(
    name='maltego-stix2',
    version=VERSION,
    description='Helper utilities for building Maltego transforms that consume or produce data in STIX2 format.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/amr-cossi/maltego-stix2',
    author='ANSSI, Samuel Hassine, Maltego Technologies GmbH',
    author_email='moa.amr.cossi@ssi.gouv.fr, samuel.hassine@luatix.org, support@maltego.com',
    license='Apache License 2.0',
    setup_requires=dependencies,
    install_requires=dependencies,
    packages=[
        'maltego_stix2'
    ],
    zip_safe=False
)
