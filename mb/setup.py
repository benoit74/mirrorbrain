#!/usr/bin/env python

from distutils.core import setup, Extension

s = setup(name='mb',
      version='3.0.0-dev0',
      description='mb, a tool to maintain the MirrorBrain database',
      author='MirrorBrain project',
      author_email='info@mirrorbrain.org',
      license='GPLv2',
      url='http://mirrorbrain.org/',

      packages=['mblib'],
      scripts=['mb.py'],

      ext_modules=[Extension('zsync', sources=['zsyncmodule.c'])],
     )