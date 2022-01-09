from .base_algorithm import BaseAlgorithm


def import_all_algorithms():
    ignore_files = {'__init__.py', 'base_algorithm.py'}
    import os
    import importlib
    dir_name = os.path.dirname(__file__)
    for path, dirs, files in os.walk(dir_name):
        for file in files:
            if file.endswith('.py') and file not in ignore_files:
                module = '.' + file[:-3]  # remove .py
                importlib.import_module(module, package='algorithms')


import_all_algorithms()
del import_all_algorithms
