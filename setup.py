from setuptools import setup

setup(
    name='pynubank',
    version='0.3',
    url='https://github.com/andreroggeri/pynubank',
    author='André Roggeri Campos',
    author_email='a.roggeri.c@gmail.com',
    license='BSD',
    packages=['pynubank'],
    install_requires=[
        'requests==2.18.1',
    ]
)
