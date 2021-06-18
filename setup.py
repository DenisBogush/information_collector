# -*- coding: utf-8 -*-

from pathlib import Path
from setuptools import find_packages, setup

SCRIPT_DIR = Path(__file__).parent

setup(name='information_collector',
      python_requires='>=3.6',
      install_requires=[
          'num2words',
          'openpyxl',
          'pandas',
          'selenium',
      ],
      packages=find_packages(where=str(SCRIPT_DIR)),
      )
