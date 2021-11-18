import ninja_syntax
from helper import get_file_extension, execute_shell_cmd
import os
from functools import reduce

python_dependencies_for_build_dot_ninja = ['exec.py', 'target.py', 'ninja_generate.py', 'project_settings.py', 'helper.py']     

def generate_build_dot_ninja_from_targets(targets, path_to_exec):

    # Convert Windows paths to Linux format
    path_to_exec = (path_to_exec).replace('\\','/')

    python_scripts_dir = os.path.dirname(path_to_exec)

    with open('build.ninja', 'w') as build_file:
        ninja_file = ninja_syntax.Writer(build_file)
        
        # Rule for compiling source files (.c/.cpp/.s/.S) into object files (.o)
        ninja_file.rule(
            name="compile", 
            command="$compiler $flags $defines $include_dirs -MMD -MF $out.d -c $in -o $out", 
            depfile="$out.d"
        )
        
        # Rule for linking together object files and static libraries into an executable
        ninja_file.rule(
            name="link", 
            command="$linker $linker_flags $linker_script $defines $include_dirs $in $library_dirs $libraries -o $out"
        )
        
        # Rule for using an archiver to create a static library from object files
        ninja_file.rule(
            name="archive", 
            command="$archiver $flags $defines $out $in"
        )

        # Rule for rebuilding "build.ninja" if any of the Python scripts are out-of-date
        ninja_file.rule(
            name="rebuild",
            command='{0} build_ninja'.format(path_to_exec),
            generator=1
        )


        # Build edge for rebuilding "build.ninja" if any of the Python scripts are out-of-date
        ninja_file.build(
            outputs='build.ninja',
            rule="rebuild",
            inputs=[python_scripts_dir+"/"+file for file in python_dependencies_for_build_dot_ninja]
        )

        # For each target in project_settings.py...
        for target in targets:

            # Compile all of the source files into object files...
            for source_file in targets[target].source_files:

                # Get the right compiler/assembler and flags, based on source file extension
                if get_file_extension(source_file) == ".cpp":
                    program = targets[target].cpp_compiler
                    flags = targets[target].cpp_flags
                elif get_file_extension(source_file) == ".c":
                    program = targets[target].c_compiler
                    flags = targets[target].c_flags
                elif get_file_extension(source_file) == ".s" or get_file_extension(source_file) == ".S":
                    program = targets[target].assembler
                    flags = targets[target].as_flags
                else:
                    raise ValueError("Unrecognized file extension in source files: {0}".format(get_file_extension(source_file)))
                
                define_str = ' '.join(["-D"+define for define in targets[target].defines])
                include_dirs_str = ' '.join(["-I "+inc_dir for inc_dir in targets[target].include_dirs])
                obj_file = "{0}/{1}".format(targets[target].build_dir,source_file.replace(get_file_extension(source_file), ".o"))
                targets[target].obj_files.append(obj_file)
                ninja_file.build(
                    outputs=obj_file, 
                    rule="compile", 
                    inputs=source_file, 
                    variables=
                    {
                        'compiler':program, 
                        'flags':' '.join(flags),
                        'defines':define_str,
                        'include_dirs':include_dirs_str
                    }
                )

            # Add build edge to build final target (based on target type)
            targets[target].add_final_build_edge(ninja_file)

            # Add one or two extra build edges to either:
            #  - Allow for post-build commands to be run every time the project is built, or
            #  - If no post-build commands are defined, rename the target to match the format of the
            #    targets with post-build commands ("target name", no extension)

            # For targets with post-build commands:
            # rule name_post_build_cmd
            #     command=...
            # build name.elf: ...
            # build name_post_build_cmd: name_post_build_cmd | name.elf
            # build name: phony | name_post_build_cmd

            # For targets withOUT post-build commands:
            # build name.elf: ...
            # build name: phony | name.elf
            if len(targets[target].post_build_cmds) > 0:
                ninja_file.rule(
                    name=targets[target].name+"_post_build_cmd",
                    command=reduce(lambda a, b: a + " && " + b, targets[target].post_build_cmds) if len(targets[target].post_build_cmds)>0 else ''
                )
                
                ninja_file.build(
                    outputs=targets[target].name+"_post_build_cmd",
                    rule=targets[target].name+"_post_build_cmd",
                    implicit=targets[target].target_file_and_path,
                )

                implicit = targets[target].name+"_post_build_cmd"
            else:
                implicit = targets[target].target_file_and_path

            ninja_file.build(
                outputs=targets[target].name,
                rule='phony',
                implicit=implicit
            )
