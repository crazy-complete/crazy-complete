#!/usr/bin/python3

from setuptools import setup

setup(
    name='crazy-complete',
    version='0.3.1',
    author='Benjamin Abendroth',
    author_email='braph93@gmx.de',
    packages=['crazy_complete'],
    scripts=['crazy-complete'],
    description='Generate shell completion files for all major shells',
    url='https://github.com/crazy-complete/crazy-complete',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Unix Shell',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Software Development :: Code Generators',
        'Topic :: System :: Shells',
        'Topic :: Utilities',
    ],
    license='GPL-3.0',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    python_requires='>=3.0',
)
