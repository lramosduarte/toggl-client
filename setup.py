from codecs import open
from os import path
from setuptools import setup
from pip.download import PipSession
from pip.req import parse_requirements

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

lista_objetos_dependencias = parse_requirements('requirements.txt', session=PipSession())
lista_dependencias = [str(objeto.req) for objeto in lista_objetos_dependencias]

setup(
    name='toggl-client',
    packages=["client"],
    version='0.1.1',
    description='Cliente para a toggl API',
    long_description=long_description,
    url='https://github.com/lramosduarte/toggl-client',
    author='Leonardo Ramos Duarte',
    author_email='lramosduarte@gmail.com',
    license='MIT',

    entry_points={
        'console_scripts': [
            'tgc = client.main:main',
        ]
    },

    data_files=['requirements.txt'],

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
    ],

    python_requires='>=3',

    keywords='toggl toggl-api toggl-client',

    install_requires=lista_dependencias,

    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },

)
