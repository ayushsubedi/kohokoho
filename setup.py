from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='kohokoho',
    version='0.0.1',
    py_modules=['kohokoho'],
    author='Ayush Subedi',
    author_email='ayush.subedi@gmail.com',
    description='A CLI tool to obfuscate/anonymize a dataset.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ayushsubedi/kohokoho',
    python_requires='>=3.6, <3.9',
    install_requires=[
        'Click',
        'pandas',
        'Faker'
    ],
    entry_points='''
        [console_scripts]
        kohokoho=kohokoho:cli
    ''',
    project_urls={
        'Bug Reports': 'https://github.com/ayushsubedi/kohokoho/issues',
        'Source': 'https://github.com/ayushsubedi/kohokoho',
    },
)
