from setuptools import setup, find_packages

setup(
    name='pynubank',
    version='2.1.0',
    url='https://github.com/andreroggeri/pynubank',
    author='André Roggeri Campos',
    author_email='a.roggeri.c@gmail.com',
    license='MIT',
    packages=find_packages(),
    package_data={'pynubank': ['queries/*.gql']},
    install_requires=['requests', 'qrcode', 'pyOpenSSL', 'colorama', 'requests-pkcs12'],
    entry_points={
        'console_scripts': [
            'pynubank = pynubank.cli:main'
        ]
    }
)
