try:
    import setuptools
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
from setuptools import setup, find_packages

version = '2.1'
readme = open('README.rst').read()

setup(name='should_dsl',
      version=version,
      description='Should assertions in Python as clear and readable as possible',
      long_description=readme,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.4',
          'Programming Language :: Python :: 2.5',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Topic :: Software Development :: Documentation',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Testing',
      ],
      keywords='should dsl assertion bdd python expectation',
      author='Hugo Lopes Tavares',
      author_email='hltbra@gmail.com',
      url='www.should-dsl.info',
      license='MIT License',
      packages=find_packages(),
      test_suite='run_all_examples.test_suite',
      )
