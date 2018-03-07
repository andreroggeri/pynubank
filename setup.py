from setuptools import setup
from pip.req import parse_requirements


def _to_list(requires):
    return [str(ir.req) for ir in requires]


install_requires = _to_list(parse_requirements('requirements.txt', session=False))
tests_require = _to_list(parse_requirements('requirements-test.txt', session=False))

setup(
    name='pynubank',
    version='0.3',
    url='https://github.com/andreroggeri/pynubank',
    author='André Roggeri Campos',
    author_email='a.roggeri.c@gmail.com',
    license='BSD',
    packages=['pynubank'],
    package_data={'pynubank': ['queries/*.gql']},
    install_requires=install_requires,
    tests_require=tests_require,
)
