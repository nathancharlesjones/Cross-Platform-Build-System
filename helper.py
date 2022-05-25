import subprocess
import os
from functools import reduce

def convert_list_to_str_for_printing(list, padding):
    return str(list).replace(", ",",\n" + " "*(padding + 1))

def execute_shell_cmd(cmd, verbose):
    if verbose:
        print("Executing:", cmd)
    process = subprocess.run(cmd, text=True)
    if verbose and process.stdout:
        print("Output:", process.stdout)
    return process.stdout

def get_file_extension(file):
    return os.path.splitext(file)[1]

def list_of_files_contains_c_files(files):
    return reduce(lambda a, b: a or b, [get_file_extension(file) == '.c' for file in files])

def list_of_files_contains_cpp_files(files):
    return reduce(lambda a, b: a or b, [get_file_extension(file) == '.cpp' for file in files])

def list_of_files_contains_s_or_S_files(files):
    return reduce(lambda a, b: a or b, [get_file_extension(file) == '.s' or get_file_extension(file) == '.S' for file in files])
