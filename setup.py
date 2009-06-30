from setuptools import setup, find_packages
import sys, os

version = '1.0'

readme_fd = open('README.rst')
readme = readme_fd.read()
readme_fd.close()

setup(name='should_dsl',
      version=version,
      description='Should assertions in Python as clear and readable as possible',
      long_description=readme,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Topic :: Software Development :: Documentation',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Testing',
      ],
      keywords='should dsl assertion bdd python',
      author='Hugo Lopes Tavares',
      author_email='hltbra@gmail.com',
      url='http://github.com/hugobr/should-dsl',
      license='MIT License',
      packages=['should_dsl'],
      package_dir={'should_dsl': 'src'},
      package_data={'':['LICENSE', 'INSTALL', '*.rst', '*.txt',]},
      install_requires=['setuptools'],
      entry_points="",
      )
