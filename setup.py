#!/usr/bin/env python

from distutils.core import setup

setup(name='gstream',
      version='0.5',
      author='Matteo Landi',
      author_email='landimatte@gmail.com',
      scripts=['bin/gstream'],
      package_dir={'gstreamlib': 'gstreamlib'},
      packages=['gstreamlib'],
     )
