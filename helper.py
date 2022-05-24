import subprocess
import os
from functools import reduce

def convert_list_to_str_for_printing(list, padding):
    return str(list).replace(", ",",\n" + " "*(padding + 1))

def execute_shell_cmd(cmd, verbose):
    if verbose:
        print("Executing:", cmd)
    process = subprocess.run(cmd, shell=True, text=True)
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

def mergesum(tgt_dictionary, second_dictionary):
    for key in second_dictionary:
        if key in tgt_dictionary:
            tgt_dictionary[key] += second_dictionary[key]
    return {**tgt_dictionary, **second_dictionary}

def prepare_target_for_building(target):
    if "name" not in target or len(target["name"]) == 0:
        raise ValueError
    if "build_dir" not in target:
        raise ValueError
    if "target" not in target:
        raise ValueError
    target["target_file_and_path"] = "{0}/{1}".format(target["build_dir"], target["target"])
    if get_file_extension(target["target"]) == ".a":
        if "archiver" not in target:
            raise ValueError
    else:
        if "linker" not in target:
            raise ValueError
    if "source_files" not in target or len(target["source_files"]) == 0:
        raise ValueError("No source files listed for {0}".format(target["name"]))        
    if list_of_files_contains_cpp_files(target["source_files"]) and target["cpp_compiler"] == '':
        raise ValueError("C++ compiler not specified though .cpp files are listed amongst the source files.")
    if list_of_files_contains_c_files(target["source_files"]) and target["c_compiler"] == '':
        raise ValueError("C compiler not specified though .c files are listed amongst the source files; use the same program as the C++ compiler if that is intended to compile both.")        
    if list_of_files_contains_s_or_S_files(target["source_files"]) and target["assembler"] == '':
        raise ValueError("Assembler not specified though .s/.S files are listed in the source files; use the same program as the C/C++ compiler if that is intended to compile/assemble both.")

    target["obj_files_dict"] = {}
    for source_file in target["source_files"]:
        # Form the path for the object file by replacing the source file extension with ".o" (e.g.
        # "src/sub1/main.c" becomes "src/sub1/main.o") and prefixing the result with the path to the 
        # build dir (e.g. "src/sub1/main.o" becomes "build/src/sub1/main.o").
        target["obj_files_dict"][source_file] = "{0}/{1}".format(target["build_dir"],source_file.replace(get_file_extension(source_file), ".o"))

    if "c_compiler" not in target:
        target["c_compiler"] = ""
    if "c_flags" not in target:
        target["c_flags"] = []
    if "cpp_compiler" not in target:
        target["cpp_compiler"] = ""
    if "cpp_flags" not in target:
        target["cpp_flags"] = []
    if "assembler" not in target:
        target["assembler"] = ""
    if "as_flags" not in target:
        target["as_flags"] = []
    if "debugger" not in target:
        target["debugger"] = ""
    if "defines" not in target:
        target["defines"] = []
    if "include_dirs" not in target:
        target["include_dirs"] = []
    if "linker_flags" not in target:
        target["linker_flags"] = []
    if "linker_script" not in target:
        target["linker_script"] = ""
    if "libraries" not in target:
        target["libraries"] = []
    if "library_dirs" not in target:
        target["library_dirs"] = []
    if "local_dependencies" not in target:
        target["local_dependencies"] = []
    target["local_dep_target_list"] = ["{0}/{1}".format(dep.build_dir,dep.target) for dep in target["local_dependencies"]]
    if "post_build_cmds" not in target:
        target["post_build_cmds"] = []        
