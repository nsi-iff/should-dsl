try:
    import setuptools
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
from setuptools import setup, find_packages

version = '2.0a3'

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
          'Topic :: Software Development :: Documentation',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Testing',
      ],
      keywords='should dsl assertion bdd python expectation',
      author='Hugo Lopes Tavares',
      author_email='hltbra@gmail.com',
      url='http://github.com/hugobr/should-dsl',
      license='MIT License',
      packages=['should_dsl'],
      package_dir={'should_dsl': 'should_dsl'},
      test_suite='run_all_examples.test_suite',
      install_requires=[],
      entry_points="",
      )
