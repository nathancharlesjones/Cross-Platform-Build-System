import ninja_syntax
from helper import get_file_extension, execute_shell_cmd
import os
from functools import reduce

python_dependencies_for_build_dot_ninja = ['make.py', 'target.py', 'ninja_generate.py', 'project_settings.py', 'helper.py']     

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
            command="$archiver $flags $out $in"
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
                
                # Form the string for defines by prefixing each item in targets[target].defines with "-D"
                define_str = ' '.join(["-D"+define for define in targets[target].defines])

                # Form the string for include dirs by prefixing each item in targets[target].include_dirs with "-I "
                include_dirs_str = ' '.join(["-I "+inc_dir for inc_dir in targets[target].include_dirs])

                # Form the path for the object file by replacing the source file extension with ".o" (e.g.
                # "src/sub1/main.c" becomes "src/sub1/main.o") and prefixing the result with the path to the 
                # build dir (e.g. "src/sub1/main.o" becomes "build/src/sub1/main.o").
                obj_file = "{0}/{1}".format(targets[target].build_dir,source_file.replace(get_file_extension(source_file), ".o"))
                
                # Append item to list of object files (used later by add_final_build_edge)
                targets[target].obj_files.append(obj_file)
                
                # Add the build edge for this specific object file
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

            # For targets with post-build commands, we have to create some indirection.
            # 1) The final target will be "name", and it will have an implicit dependency 
            #    on "name_post_build_cmd" so that "name_post_build_cmd" will be run any
            #    time "name" is built. I.e.
            #        build name: phony | name_post_build_cmd

            # 2) The build edge for "name_post_build_cmd" will run "name_post_build_cmd"
            #    AND it will have an implicit dependency on "name.ext", so that "name.ext"
            #    is always brought up-to-date prior to running "name_post_build_cmd". I.e.
            #        rule name_post_build_cmd
            #            command=...
            #        build name_post_build_cmd: name_post_build_cmd | name.elf

            # 3) The actual target, "name.ext", is built like normal, per the format for either
            #    an executable or library. I.e.
            #        build name.ext: ...

            # For targets withOUT post-build commands, we'll still need some indirection, but it's
            # for the purpose of having all targets match the format shown above, with the final
            # target being "name" instead of "name.elf"
            # 1) To do that, we'll create a final target called "name", in order to match the format
            #    of the targets above that DO have post-build commands, that has an implicit 
            #    dependency on "name.ext". I.e.
            #        build name: phony | name.ext

            # 2) The actual target, "name.ext", is built like normal, per the format for either
            #    an executable or library. I.e.
            #        build name.ext: ...
            
            # So both targets will get an additional build edge to "rename" them to "name", but targets
            # WITH post-build commands will have the implicit dependency be "name_post_build_cmds"
            # while targets withOUT post-build commnds will have the implicit dependency be "name.ext".

            # So the pattern is...
            # if the target DOES have post-build commands...
            if len(targets[target].post_build_cmds) > 0:

                # ...Add the rule "name_post_build_cmds"
                ninja_file.rule(
                    name=targets[target].name+"_post_build_cmd",
                    command=reduce(lambda a, b: a + " && " + b, targets[target].post_build_cmds)
                )
                
                # ...And the build edge that runs "name_post_build_cmd" with an implicit
                # dependency on "name.ext"
                ninja_file.build(
                    outputs=targets[target].name+"_post_build_cmd",
                    rule=targets[target].name+"_post_build_cmd",
                    implicit=targets[target].target_file_and_path,
                )

                # ...And set the implicit dependency for the final target to "name_post_build_cmds"
                implicit = targets[target].name+"_post_build_cmd"

            # ...but if the target does NOT have any post-build commands...
            else:

                # ...Just set the implicit dependency for the final target to "name.ext"
                implicit = targets[target].target_file_and_path

            # Lastly, add the build edge for the final target of "name", with the implicit dependency
            # that was set above.
            ninja_file.build(
                outputs=targets[target].name,
                rule='phony',
                implicit=implicit
            )

if __name__ == "__main__":
    from project_settings import targets
    import sys

    generate_build_dot_ninja_from_targets(targets, sys.argv[0])