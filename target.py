from helper import (execute_shell_cmd, list_of_files_contains_c_files,
                    list_of_files_contains_cpp_files, list_of_files_contains_s_or_S_files,
                    convert_list_to_str_for_printing, get_file_extension)
import os
import ninja_syntax

class target:
    """ Parent class for defining project targets. """

    print_padding = 25

    def __init__(self,build_dir,target,source_files,name='unnamed target',
        assembler='',as_flags=[],c_compiler='',c_flags=[],cpp_compiler='',cpp_flags=[],
        defines=[],include_dirs=[],libraries=[],library_dirs=[],
        local_dependencies=[],pre_build_cmds=[],post_build_cmds=[]):
        #raise NameError("Class target does not support creating objects; use target.executable or target.library instead.")
        self.name = name
        self.source_files = source_files
        if len(self.source_files) == 0:
            raise ValueError("No source files listed for {0}".format(self.name))        
        self.cpp_compiler = cpp_compiler
        self.cpp_flags = cpp_flags
        if list_of_files_contains_cpp_files(self.source_files) and self.cpp_compiler == '':
            raise ValueError("C++ compiler not specified though .cpp files are listed amongst the source files.")
        self.c_compiler = c_compiler        
        self.c_flags = c_flags
        if list_of_files_contains_c_files(self.source_files) and self.c_compiler == '':
            raise ValueError("C compiler not specified though .c files are listed amongst the source files; use the same program as the C++ compiler if that is intended to compile both.")        
        self.assembler = assembler
        self.as_flags = as_flags
        if list_of_files_contains_s_or_S_files(self.source_files) and self.assembler == '':
            raise ValueError("Assembler not specified though .s/.S files are listed in the source files; use the same program as the C/C++ compiler if that is intended to compile/assemble both.")        
        self.defines = defines        
        self.build_dir = build_dir        
        self.target = target
        self.target_file_and_path = "{0}/{1}".format(self.build_dir, self.target)
        self.include_dirs = include_dirs
        self.libraries = libraries
        self.library_dirs = library_dirs
        self.local_dependencies = local_dependencies
        self.local_dep_target_list = ["{0}/{1}".format(dep.build_dir,dep.target) for dep in self.local_dependencies]
        self.pre_build_cmds = pre_build_cmds
        self.post_build_cmds = post_build_cmds
        self.obj_files = []
    
    def clean(self, verbose=False):
        execute_shell_cmd("find {0}".format(self.build_dir)+r" -mindepth 1 -maxdepth 1 -type d -exec rm -r {} \;", verbose)
    
    def execute(self, cmd, verbose=False):
        if cmd == 'clean':
            self.clean(verbose)
        elif cmd == 'purify':
            self.purify(verbose)
        elif cmd == 'zip':
            self.zip(verbose)
        elif cmd == 'list':
            self.show(verbose)
        elif cmd == 'build':
            self.build(verbose)

    def purify(self, verbose=False):
        execute_shell_cmd("rm -r -f {0}".format(self.build_dir), verbose)

    def show(self, verbose=False):
        if not verbose:
            print("- {0}".format(self.name))
        else:
            print(self)

    def zip(self, verbose=False):
        execute_shell_cmd("zip -r {0}/{1}.zip {2} {3}".format(self.build_dir,self.name,self.target_file_and_path,self.local_dep_target_list), verbose)

    def __str__(self):
        pass

class executable(target):
    """ Helpful docstring """

    def __init__(self,linker,build_dir,target,source_files,name='unnamed target',
        assembler='',as_flags=[],c_compiler='',c_flags=[],cpp_compiler='',cpp_flags=[],
        defines=[],linker_flags=[],include_dirs=[],libraries=[],library_dirs=[],
        linker_script='',local_dependencies=[],pre_build_cmds=[],post_build_cmds=[]):
        """ Helpful docstring """

        super().__init__(build_dir,target,source_files,name,
        assembler,as_flags,c_compiler,c_flags,cpp_compiler,cpp_flags,
        defines,include_dirs,libraries,library_dirs,
        local_dependencies,pre_build_cmds,post_build_cmds)

        self.linker = linker
        self.linker_flags = linker_flags
        self.linker_script = linker_script

    def add_final_build_edge(self, ninja_file):
        define_str = ' '.join(["-D"+define for define in self.defines])
        include_dirs_str = ' '.join(["-I "+inc_dir for inc_dir in self.include_dirs])
        library_dirs_str = ' '.join(["-L "+lib_dir for lib_dir in self.library_dirs])
        libraries_str = ' '.join(["-l"+lib for lib in self.libraries])
        ninja_file.build(
            outputs=self.target_file_and_path, 
            rule="link", 
            inputs=self.obj_files, 
            implicit=[lib.target_file_and_path for lib in self.local_dependencies],
            variables=
            {
                'linker':self.linker,
                'linker_flags':' '.join(self.linker_flags),
                'linker_script':"-T " + self.linker_script,
                'defines':define_str,
                'include_dirs':include_dirs_str,
                'library_dirs':library_dirs_str,
                'libraries':libraries_str
            }
        )

    def __str__(self):
        padding = self.print_padding
        repr =  self.name + " is defined as follows:\n" + \
                "- name:".ljust(padding,'.') + self.name + "\n" + \
                "- target:".ljust(padding,'.') + self.target + "\n" + \
                "- build_dir:".ljust(padding,'.') + self.build_dir + "\n" + \
                "- assembler:".ljust(padding,'.') + self.assembler + "\n" + \
                "- as_flags:".ljust(padding,'.') + convert_list_to_str_for_printing(self.as_flags, padding) + "\n" + \
                "- c_compiler:".ljust(padding,'.') + self.c_compiler + "\n" + \
                "- c_flags:".ljust(padding,'.') + convert_list_to_str_for_printing(self.c_flags, padding) + "\n" + \
                "- cpp_compiler:".ljust(padding,'.') + self.cpp_compiler + "\n" + \
                "- cpp_flags:".ljust(padding,'.') + convert_list_to_str_for_printing(self.cpp_flags, padding) + "\n" + \
                "- linker:".ljust(padding,'.') + self.linker + "\n" + \
                "- linker_flags:".ljust(padding,'.') + convert_list_to_str_for_printing(self.linker_flags, padding) + "\n" + \
                "- linker_script:".ljust(padding,'.') + self.linker_script + "\n" + \
                "- defines:".ljust(padding,'.') + convert_list_to_str_for_printing(self.defines, padding) + "\n" + \
                "- include_dirs:".ljust(padding,'.') + convert_list_to_str_for_printing(self.include_dirs, padding) + "\n" + \
                "- source_files:".ljust(padding,'.') + convert_list_to_str_for_printing(self.source_files, padding) + "\n" + \
                "- libraries:".ljust(padding,'.') + convert_list_to_str_for_printing(self.libraries, padding) + "\n" + \
                "- library_dirs:".ljust(padding,'.') + convert_list_to_str_for_printing(self.library_dirs, padding) + "\n" + \
                "- local_dependencies:".ljust(padding,'.') + convert_list_to_str_for_printing([dep.name for dep in self.local_dependencies], padding) + "\n" + \
                "- pre_build_cmds:".ljust(padding,'.') + convert_list_to_str_for_printing(self.pre_build_cmds, padding) + "\n" + \
                "- post_build_cmds:".ljust(padding,'.') + convert_list_to_str_for_printing(self.post_build_cmds, padding)
        return repr

class library(target):
    """ Helpful docstring """

    def __init__(self,archiver,build_dir,target,source_files,name='unnamed target',
        assembler='',as_flags=[],c_compiler='',c_flags=[],cpp_compiler='',cpp_flags=[],
        defines=[],archiver_flags=[],include_dirs=[],libraries=[],
        library_dirs=[],local_dependencies=[],pre_build_cmds=[],post_build_cmds=[]):
        """ Helpful docstring """

        super().__init__(build_dir,target,source_files,name,
        assembler,as_flags,c_compiler,c_flags,cpp_compiler,cpp_flags,
        defines,include_dirs,libraries,library_dirs,
        local_dependencies,pre_build_cmds,post_build_cmds)

        self.archiver = archiver
        self.archiver_flags = archiver_flags

    def add_final_build_edge(self, ninja_file):
        define_str = ' '.join(["-D"+define for define in self.defines])
        ninja_file.build(
            outputs=self.target_file_and_path, 
            rule="archive", 
            inputs=self.obj_files, 
            implicit=[lib.target_file_and_path for lib in self.local_dependencies],
            variables=
            {
                'archiver':self.archiver,
                'flags':' '.join(self.archiver_flags),
                'defines':define_str
            }
        )

    def __str__(self):
        padding = self.print_padding
        repr =  self.name + " is defined as follows:\n" + \
                "- name:".ljust(padding,'.') + self.name + "\n" + \
                "- target:".ljust(padding,'.') + self.target + "\n" + \
                "- build_dir:".ljust(padding,'.') + self.build_dir + "\n" + \
                "- assembler:".ljust(padding,'.') + self.assembler + "\n" + \
                "- as_flags:".ljust(padding,'.') + convert_list_to_str_for_printing(self.as_flags, padding) + "\n" + \
                "- c_compiler:".ljust(padding,'.') + self.c_compiler + "\n" + \
                "- c_flags:".ljust(padding,'.') + convert_list_to_str_for_printing(self.c_flags, padding) + "\n" + \
                "- cpp_compiler:".ljust(padding,'.') + self.cpp_compiler + "\n" + \
                "- cpp_flags:".ljust(padding,'.') + convert_list_to_str_for_printing(self.cpp_flags, padding) + "\n" + \
                "- archiver:".ljust(padding,'.') + self.archiver + "\n" + \
                "- archiver_flags:".ljust(padding,'.') + convert_list_to_str_for_printing(self.archiver_flags, padding) + "\n" + \
                "- defines:".ljust(padding,'.') + convert_list_to_str_for_printing(self.defines, padding) + "\n" + \
                "- include_dirs:".ljust(padding,'.') + convert_list_to_str_for_printing(self.include_dirs, padding) + "\n" + \
                "- source_files:".ljust(padding,'.') + convert_list_to_str_for_printing(self.source_files, padding) + "\n" + \
                "- libraries:".ljust(padding,'.') + convert_list_to_str_for_printing(self.libraries, padding) + "\n" + \
                "- library_dirs:".ljust(padding,'.') + convert_list_to_str_for_printing(self.library_dirs, padding) + "\n" + \
                "- local_dependencies:".ljust(padding,'.') + convert_list_to_str_for_printing([dep.name for dep in self.local_dependencies], padding) + "\n" + \
                "- pre_build_cmds:".ljust(padding,'.') + convert_list_to_str_for_printing(self.pre_build_cmds, padding) + "\n" + \
                "- post_build_cmds:".ljust(padding,'.') + convert_list_to_str_for_printing(self.post_build_cmds, padding)
        return repr
