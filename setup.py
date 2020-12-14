import os

from setuptools import setup, find_packages

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()

setup(
    name='pynubank',
    version='2.8.0',
    url='https://github.com/andreroggeri/pynubank',
    author='André Roggeri Campos',
    author_email='a.roggeri.c@gmail.com',
    license='MIT',
    packages=find_packages(),
    package_data={'pynubank': ['queries/*.gql', 'utils/mocked_responses/*.json']},
    install_requires=['requests', 'qrcode', 'pyOpenSSL', 'colorama', 'requests-pkcs12'],
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            'pynubank = pynubank.cli:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)
