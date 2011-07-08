#!/usr/bin/env python
import os
import glob
from run_examples import run

def all_examples():
    documentation = glob.glob('docs/*.rst') + ['README.rst']
    doctests_path = os.path.join('should_dsl', 'doctests')
    doctests = list(map(lambda f: os.path.join(doctests_path, f),
        filter(lambda f: f.endswith('.txt'), os.listdir(doctests_path))))
    return documentation + doctests

if __name__ == '__main__':
    run(all_examples())

