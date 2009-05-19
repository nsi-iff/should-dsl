from setuptools import setup, find_packages
import sys, os

version = '0.3'

setup(name='should_dsl',
      version=version,
      description="Should DSL",
      long_description="",
      classifiers=[],
      keywords='bdd dsl python',
      author='Hugo Lopes Tavares',
      author_email='hltbra@gmail.com',
      url='http://code.google.com/p/should-dsl/',
      license='MIT License',
      packages=['should_dsl'],
      package_dir={'should_dsl': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools'],
      entry_points="",
      )
