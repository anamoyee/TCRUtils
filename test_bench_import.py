import time


def benchmark_import(module_name):
    start_time = time.time()
    exec(f'import {module_name}')
    end_time = time.time()

    return end_time - start_time


benchmark_import('module_name_here')
