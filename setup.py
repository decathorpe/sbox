"""
setuptools install script for kentauros
"""

import os
from setuptools import setup

NAME = "sbox"
DATADIR = "/usr/share/" + NAME

setup(name="sbox",
      version=0,
      author="Fabio Valentini",
      author_email="decathorpe@gmail.com",
      description="Simple Application Sandboxing using bubblewrap",
      license="GPLv3",
      url="http://github.com/decathorpe/sbox",
      packages=['sbox'],
      install_requires=[],
      scripts=[],
      entry_points= {'sbox': ['sbox=sbox:main']},
      data_files=[(os.path.join(DATADIR, "profiles"), ['profiles/org.gnome.gedit.json']),
                  (os.path.join(DATADIR, "profiles"), ['profiles/system.json'])],
      classifiers=['Development Status :: 2 - Pre-Alpha',
                   'Intended Audience :: Developers',
                   'Topic :: Security',
                   'Topic :: Software Development',
                   'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.6'])
