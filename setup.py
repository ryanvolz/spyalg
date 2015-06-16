#-----------------------------------------------------------------------------
# Copyright (c) 2014, Ryan Volz
# All rights reserved.
#
# Distributed under the terms of the BSD 3-Clause ("BSD New") license.
#
# The full license is in the LICENSE file, distributed with this software.
#-----------------------------------------------------------------------------

from setuptools import setup
import codecs

import versioneer

# custom setup.py commands
cmdclass = versioneer.get_cmdclass()

# add nose and sphinx commands since we depend on them but they are not always
# automatically available (e.g. when using conda versions of these packages)
try:
    from nose.commands import nosetests
except ImportError:
    pass
else:
    cmdclass['nosetests'] = nosetests
try:
    from sphinx.setup_command import BuildDoc
except ImportError:
    pass
else:
    cmdclass['build_sphinx'] = BuildDoc

# Get the long description from the relevant file
# Use codecs.open for Python 2 compatibility
with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='prx',
    version=versioneer.get_version(),
    description='Optimization algorithms based on the proximal operator',
    long_description=long_description,

    url='http://github.com/ryanvolz/prx',

    author='Ryan Volz',
    author_email='ryan.volz@gmail.com',

    license='BSD 3-Clause ("BSD New")',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Scientific/Engineering',
    ],

    keywords='optimization prox proximal convex first-order',

    packages=['prx'],
    install_requires=['Bottleneck', 'numpy', 'scipy'],
    extras_require={
        'doc': ['numpydoc', 'sphinx'],
    },

    cmdclass=cmdclass,
)
