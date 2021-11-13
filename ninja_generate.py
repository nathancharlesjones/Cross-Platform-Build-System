import ninja_syntax
from helper import get_file_extension

# How to do pre-/post-commands?
# Add self-rebuilding rule?
# Add renaming step?      

def generate_build_dot_ninja_from_targets(targets):
    with open('build.ninja', 'w') as build_file:
        ninja_file = ninja_syntax.Writer(build_file)
        
        ninja_file.rule(
            name="compile", 
            command="$compiler $flags $defines $include_dirs -MMD -MF $out.d -c $in -o $out", 
            depfile="$out.d"
        )
        
        ninja_file.rule(
            name="link", 
            command="$linker $linker_flags $linker_script $defines $include_dirs $in $library_dirs $libraries -o $out"
        )
        
        ninja_file.rule(
            name="archive", 
            command="$archiver $flags $defines $out $in"
        )

        for target in targets:
            for source_file in targets[target].source_files:
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

            targets[target].add_final_build_edge(ninja_file)