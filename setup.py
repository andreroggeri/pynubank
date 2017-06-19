from setuptools import setup

setup(
    name='pynubank',
    version='0.1',
    url='https://github.com/andreroggeri/pynubank',
    author='André Roggeri Campos',
    author_email='a.roggeri.c@gmail.com',
    license='BSD',
    packages=['pynubank'],
    install_requires=[
        'certifi==2017.4.17',
        'chardet==3.0.4',
        'idna==2.5',
        'requests==2.18.1',
        'urllib3==1.21.1'
    ]
)
