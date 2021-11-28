import ninja_syntax
from helper import get_file_extension, execute_shell_cmd, prepare_target_for_building
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
            
            thisTarget = targets[target]

            # Check for error conditions (such as a missing "build_dir" or no source files).
            # Define dependent keys such as "target_file_and_path" and object files.
            # Set all possible keys to empty values if not defined.
            prepare_target_for_building(thisTarget)

            # Form the string for defines by prefixing each item in targets[target].defines with "-D"
            define_str = ' '.join(["-D"+define for define in thisTarget["defines"]])

            # Form the string for include dirs by prefixing each item in targets[target].include_dirs with "-I "
            include_dirs_str = ' '.join(["-I "+inc_dir for inc_dir in thisTarget["include_dirs"]])
            
            for source_file in thisTarget["obj_files_dict"]:

                # Get the right compiler/assembler and flags, based on source file extension

                if get_file_extension(source_file) == ".cpp":
                    program = thisTarget["cpp_compiler"]
                    flags = thisTarget["cpp_flags"]
                elif get_file_extension(source_file) == ".c":
                    program = thisTarget["c_compiler"]
                    flags = thisTarget["c_flags"]
                elif get_file_extension(source_file) == ".s" or get_file_extension(source_file) == ".S":
                    program = thisTarget["assembler"]
                    flags = thisTarget["as_flags"]
                else:
                    raise ValueError("Unrecognized file extension in source files: {0}".format(get_file_extension(source_file)))
                
                # Form the string for the compiler/assembler flags by prefixing each item in flags with "-W"
                flags_str = ' '.join(["-W"+flag for flag in flags])

                # Add the build edge for this specific object file
                ninja_file.build(
                    outputs=thisTarget["obj_files_dict"][source_file], 
                    rule="compile", 
                    inputs=source_file, 
                    variables=
                    {
                        'compiler':program, 
                        'flags':flags_str,
                        'defines':define_str,
                        'include_dirs':include_dirs_str
                    }
                )

            # Add build edge to build final target (based on target type)
            if( get_file_extension(thisTarget["target"]) == ".a" ):
                ninja_file.build(
                    outputs=thisTarget["target_file_and_path"], 
                    rule="archive", 
                    inputs=list(thisTarget["obj_files_dict"].values()),
                    implicit=[lib.target_file_and_path for lib in thisTarget["local_dependencies"]],
                    variables=
                    {
                        'archiver':thisTarget["archiver"],
                        'flags':' '.join(thisTarget["archiver_flags"])
                    }
                )
            else:
                library_dirs_str = ' '.join(["-L "+lib_dir for lib_dir in thisTarget["library_dirs"]])
                libraries_str = ' '.join(["-l"+lib for lib in thisTarget["libraries"]])
                ninja_file.build(
                    outputs=thisTarget["target_file_and_path"], 
                    rule="link", 
                    inputs=list(thisTarget["obj_files_dict"].values()),
                    implicit=[lib.target_file_and_path for lib in thisTarget["local_dependencies"]],
                    variables=
                    {
                        'linker':thisTarget["linker"],
                        'linker_flags':' '.join(thisTarget["linker_flags"]),
                        'linker_script':"-T " + thisTarget["linker_script"] if targets[target]["linker_script"] else '',
                        'defines':define_str,
                        'include_dirs':include_dirs_str,
                        'library_dirs':library_dirs_str,
                        'libraries':libraries_str
                    }
                )

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
            if len(thisTarget["post_build_cmds"]) > 0:

                # ...Add the rule "name_post_build_cmds"
                ninja_file.rule(
                    name=thisTarget["name"]+"_post_build_cmd",
                    command=reduce(lambda a, b: a + " && " + b, thisTarget["post_build_cmds"])
                )
                
                # ...And the build edge that runs "name_post_build_cmd" with an implicit
                # dependency on "name.ext"
                ninja_file.build(
                    outputs=thisTarget["name"]+"_post_build_cmd",
                    rule=thisTarget["name"]+"_post_build_cmd",
                    implicit=thisTarget["target_file_and_path"],
                )

                # ...And set the implicit dependency for the final target to "name_post_build_cmds"
                implicit = thisTarget["name"]+"_post_build_cmd"

            # ...but if the target does NOT have any post-build commands...
            else:

                # ...Just set the implicit dependency for the final target to "name.ext"
                implicit = thisTarget["target_file_and_path"]

            # Lastly, add the build edge for the final target of "name", with the implicit dependency
            # that was set above.
            ninja_file.build(
                outputs=thisTarget["name"],
                rule='phony',
                implicit=implicit
            )

if __name__ == "__main__":
    from project_settings import targets
    import sys

    generate_build_dot_ninja_from_targets(targets, sys.argv[0])