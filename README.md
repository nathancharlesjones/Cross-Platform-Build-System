# Cross-Platform Build System with Ninja/Docker/Python

## Contents

1) [What is it?](https://github.com/nathancharlesjones/Cross-Platform-Build-System#what-is-it)
2) [How does it work?](https://github.com/nathancharlesjones/Cross-Platform-Build-System#how-does-it-work)
	- [Creating build.ninja](https://github.com/nathancharlesjones/Cross-Platform-Build-System#creating-buildninja)
		- [`library` objects](https://github.com/nathancharlesjones/Cross-Platform-Build-System#library-objects)
		- [`executable` objects](https://github.com/nathancharlesjones/Cross-Platform-Build-System#executable-objects)
	- [Using Docker](https://github.com/nathancharlesjones/Cross-Platform-Build-System#using-docker)
	- [Python CLI](https://github.com/nathancharlesjones/Cross-Platform-Build-System#python-cli)
3) [How do I use it?](https://github.com/nathancharlesjones/Cross-Platform-Build-System#how-do-i-use-it)
4) [References](https://github.com/nathancharlesjones/Cross-Platform-Build-System#references)
	- [Ninja](https://github.com/nathancharlesjones/Cross-Platform-Build-System#ninja)
	- [Docker](https://github.com/nathancharlesjones/Cross-Platform-Build-System#docker)
	- [Misc](https://github.com/nathancharlesjones/Cross-Platform-Build-System#misc)

## What is it?

An attempt to make a straightforward, cross-platform build system using Ninja, Docker, and Python.

The build system I *had* been using was less-than-ideal for two reasons:

1) It was cryptic and dense. I cut my teeth on `make` and had started learning `CMake` right before this project, but both felt overcomplicated to me.
2) It wasn't truly cross-platform. I have a Windows computer at work and a Linux computer at home, but even if I have the right tools to build a project on both my Windows and Linux computers, building that project on one machine meant I could only debug the resulting binary on *that* machine; the debugging information in the final binary contained filepaths that didn't translate from Windows to Linux or vice versa so GDB couldn't identify the debugging information.

The resulting system isn't perfect by any stretch of the imagination, but I *think* it provides the ability to:
- clearly define and customize different build artifacts (using ninja + some Python),
- build those artifacts in a consistent, cross-platform manner (using ninja + Docker), and
- load those artifacts onto an MCU and debug it, also in a consistent, cross-platform manner (using Docker + gdbgui).

## How does it work?

Three components work together to create this straightforward, cross-platform build system:

1) The Python library `ninja_syntax` allows us to create a `build.ninja` file that defines how we want our project and each target to be built. Because it's Python, we can use standard Python syntax and data structures like dictionaries to easily define each target.
2) Docker provides us with a consistent, cross-platform way to build our project. Additionally, using [gdbgui](https://www.gdbgui.com/) we can debug our project from inside Docker (even if it's running on an MCU that's attached to the host machine with a USB debug adapter) without needing to recompile when moving between host OSes.
3) A Python CLI provides easy aliases for commonly needed commands.

### Creating build.ninja



The Python module `target.py` defines two types of targets: `library` and `executable`. A `library` target builds a static library and `executable` builds an executable binary. They accept the parameters below. Not all are required; `make.py` should warn you when something is missing that's required.

#### `library` objects

| Field              | Type            | Required?                                          | Description                                                                                                                                                                                                                                                   |
|--------------------|-----------------|----------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| name               | String          | No                                                 | Name to be used for this target. Used with `-t` when building/cleaning/purifying/zipping a single target.                                                                                                                                                     |
| build_dir          | String          | Yes                                                | Name of the directory in the project folder where build results should be placed. Doesn't need to be made ahead of time, as the program will create it if it does not exist.                                                                                         |
| target             | String          | Yes                                                | Name (and extension, if used) of the final library to be built (e.g. "libtest.a").                                                                                                                                                            |
| c_compiler         | String          | Yes, if `source_files` includes ".c" files         | Program to be used for compiling ".c" files. Can be the same as cpp_compiler if that is desired. Should match the exact program invocation used in a shell (e.g. "gcc", not "GCC").                                                                           |
| c_flags            | List of strings | No                                                 | List of flags to be passed to the C compiler.                                                                                                                                                                                                                 |
| cpp_compiler       | String          | Yes, if `source_files` includes ".cpp" files       | Program to be used for compiling ".cpp" files. Should match the exact program invocation used in a shell (e.g. "g++", not "G++").                                                                                                                             |
| cpp_flags          | List of strings | No                                                 | List of flags to be passed to the C++ compiler.                                                                                                                                                                                                               |
| assembler          | String          | Yes, if `source_files` includes ".s" or ".S" files | Program to be used for assembling ".s" and ".S" files. Can be the same as c_compiler or cpp_compiler if that is desired. Should match the exact program invocation used in the shell (e.g. "as", not "AS").                                                                                                                    |
| as_flags           | List of strings | No                                                 | List of flags to be passed to the assembler.                                                                                                                                                                                                                  |
| defines            | List of strings | No                                                 | List of defines to be passed to the compiler/assembler. Should not be prefixed with "-D", as this will get added by the program.                                                                                                                                   |
| include_dirs       | List of strings | No                                                 | List of include directories to be added to the compiler, relative to the project's root folder. Should not be prefixed with "-I ", as this will get added by the program.                                                                                     |
| source_files       | List of strings | Yes                                                | List of all source files to be used in the project; it's okay if the list is a mix of ".c", ".cpp", and ".s"/".S" files. Each entry should include a filepath relative to the project's root folder, i.e. "src/main.c".                                       |
| archiver           | String          | Yes                                                | Program to be used for final building of the static library. Should match exactly the program invocation used in the shell (e.g. "ar", not "AR").                                                                                                             |
| archiver_flags     | List of strings | No                                                 | List of flags to be passed to the archiver.                                                                                                                                                       |
| libraries          | List of strings | No                                                 | List of libraries to link against the final executable, including any locally built libraries. Should not be prefixed with "-l", as this will get added by the program.                                                                                       |
| library_dirs       | List of strings | No                                                 | List of directories in which to search for the required libraries, relative to the project's root folder (system folders need not be included).                                                                                                               |
| local_dependencies | List of strings | No                                                 | List of `target.library` objects that this program is dependent on. These need to be the actual `target.library` objects as each objects' build method will be invoked by the program when this executable is being built, to ensure that all files are up to date. |
| post_build_cmds    | List of strings | No                                                 | List of shell commands to be executed after building this project. Should be typed exactly as they would be in the shell, e.g. "./build/main".                                                                                                                |

#### `executable` objects

| Field              | Type            | Required?                                          | Description                                                                                                                                                                                                                                                   |
|--------------------|-----------------|----------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| name               | String          | No                                                 | Name to be used for this target. Given to "-t" when building/cleaning/purifying/zipping a single target.                                                                                                                                                      |
| build_dir          | String          | Yes                                                | Name of the directory in the project folder where build results should be placed. Doesn't need to be made ahead of time, as the program will create it if it does not exist.                                                                                         |
| target             | String          | Yes                                                | Name (and extension, if used) of the final executable to be build (e.g. "main.exe", "myProg.elf").                                                                                                                                                            |
| c_compiler         | String          | Yes, if `source_files` includes ".c" files         | Program to be used for compiling ".c" files. Can be the same as cpp_compiler if that is desired. Should match the exact program invocation used in a shell (e.g. "gcc", not "GCC").                                                                           |
| c_flags            | List of strings | No                                                 | List of flags to be passed to the C compiler.                                                                                                                                                                                                                 |
| cpp_compiler       | String          | Yes, if `source_files` includes ".cpp" files       | Program to be used for compiling ".cpp" files. Should match the exact program invocation used in a shell (e.g. "g++", not "G++").                                                                                                                             |
| cpp_flags          | List of strings | No                                                 | List of flags to be passed to the C++ compiler.                                                                                                                                                                                                               |
| assembler          | String          | Yes, if `source_files` includes ".s" or ".S" files | Program to be used for assembling ".s" and ".S" files. Can be the same as c_compiler or cpp_compiler if that is desired. Should match the exact program invocation used in the shell (e.g. "as", not "AS").                                                                                                                     |
| as_flags           | List of strings | No                                                 | List of flags to be passed to the assembler.                                                                                                                                                                                                                  |
| defines            | List of strings | No                                                 | List of defines to be passed to the compiler/assembler. Should not be prefixed "-D", as this will get added by the program.                                                                                                                                   |
| include_dirs       | List of strings | No                                                 | List of include directories to be added to the compiler, relative to the project's root folder. Should not be prefixed with "-I ", as this will get added by the program.                                                                                     |
| source_files       | List of strings | Yes                                                | List of all source files to be used in the project; it's okay if the list is a mix of ".c", ".cpp", and ".s"/".S" files. Each entry should include a filepath relative to the project's root folder, i.e. "src/main.c".                                       |
| linker             | String          | Yes                                                | Program to be used for final linking of an executable. Should match exactly the program invocation used in the shell (e.g. "ld" or "gcc", not "GCC").                                                                                                         |
| linker_flags       | List of strings | No                                                 | List of flags to be passed to the linker.                                                                                                                                                                                                                     |
| linker_script      | String          | No                                                 | Linker script to be given to the linker (for embedded systems). Should not be prefixed by "-T", as this will get added by the program.                                                                                                                        |
| libraries          | List of strings | No                                                 | List of libraries to link against the final executable, including any locally built libraries. Should not be prefixed with "-l", as this will get added by the program.                                                                                       |
| library_dirs       | List of strings | No                                                 | List of directories in which to search for the required libraries, relative to the project's root folder (system folders need not be included).                                                                                                               |
| local_dependencies | List of strings | No                                                 | List of `target.library` objects that this program is dependent on. These need to be the actual `target.library` objects as each objects' build method will be invoked by the program when this executable is being built, to ensure that all files are up to date. |
| post_build_cmds    | List of strings | No                                                 | List of shell commands to be executed after building this project. Should be typed exactly as they would be in the shell, e.g. "./build/main".                                                                                                                |

### Using Docker

### Python CLI

## How do I use it?

Check out [this sample project](https://github.com/nathancharlesjones/Cross-Platform-Build-System-Example) or follow the directions below:

1) Clone this repo into your desired project folder. I.e.
```
. <-- Root project folder
├── Python-Build-System
│   ├── Dockerfile
│   ├── README.md
│   ├── helper.py
│   ├── make.py
│   ├── ninja_generate.py
│   ├── example_project_settings.py
│   └── target.py
├── inc
├── src
└── Other project folders...
```
2) Set up docker:
    - Inspect the Dockerfile to see if there are any additional programs you'll want. Only `build-essentials` is required for normal GCC projects (it includes `gcc`, `g++`, and `make`).
    - The Dockerfile is hard-coded to download GCC 10.3; edit lines 30 and 31 to use a different version.
    - Under "Notes" at the bottom, the Dockerfile also shows how to:
    	- download other useful programs,
    	- install a project dependency (like another git repo), and
    	- modify the Dockerfile so that a specific command or program is run each time the Docker container starts up.
    - Download and install [Docker](https://docs.docker.com/get-docker/). Ensure it is running.
    - From a shell on your system, navigate to your project folder and run the command below, replacing `Cross-Platform-Build-System` with the path to `make.py` for your system.
    	- If you make that change, you'll also need to tell Docker where to find the Dockerfile. By default, the Python CLI assumes the Dockerfile is inside a folder called `Cross-Platform-Build-System`, as defined in `project_settings.py` (see below). You can either edit the default value for the path in `project_settings.py` or you can run the command with `-p CORRECT_PATH_TO_DOCKERFILE`.
    	- Additionally, you can change the name for your Docker image by either editing the default value in `project_settings.py` (see below) or you can run the command with `-n DIFFERENT_NAME`.

    `./Cross-Platform-Build-System/make.py build_docker`
    
    - Wait. Building this Docker image takes a good 5-10 minutes on my system.
3) Get the following dependencies on your host machine:
- ninja_syntax (run `pip3 install ninja_syntax`)
- [git](https://git-scm.com/downloads)
4) Create or edit `project_settings.py` to be of the following format:
```
import target

default_path_to_docker_file = 'Cross-Platform-Build-System'
default_docker_name = 'devenv-simple-build-system'
default_debug_port_number = '5000'

targets = {}

# Define a new target, e.g. "new_library = target.library(...) or main = target.executable(...)"

# Add the target to the dictionary of targets: targets[main.name] = main
```
You can find an example settings file above (`example_project_settings.py`) or [here](https://github.com/nathancharlesjones/Cross-Platform-Build-System-Example/project_settings.py).
5) Create the `build.ninja` file (used by ninja in order to build your project) by running the following command from the project's root folder:

`./make.py build_ninja`

6) Build, debug, and interact with your project to your heart's content. Running `./make.py -h` will show you the text below, which lists the other available commands in `make.py`. These include the ability to:
- list the targets defined in `project_settings.py` (`list`), 
- build one or all of the targets (`build_target`),
- clean the build directory (`clean`),
- clean the build directory and build one or all of the targets (`clean_build`),
- debug one of the executables (`debug`),
- open up a bash prompt in Docker (`docker_bash`),
- run a specific command in Docker (`run`), or
- execute `git add . && git commit -m <MSG> && git push` (`push`).

```
usage: make.py [-h] [-v] {build_docker,build_ninja,list,build_target,clean,clean_build,debug,docker_bash,run,push} ...

Helper script for interacting with an embedded systems project. Run 'make.py ACTION -h' for further help information about each action that can be run.

positional arguments:
  {build_docker,build_ninja,list,build_target,clean,clean_build,debug,docker_bash,run,push}
    build_docker        Builds the Docker container used to build and debug the project.
    build_ninja         (Re)Build the file 'build.ninja' according to the project specifications defined in 'project_targets.py'. Once generated, used "make.py build_target" to use Docker
                        to build all targets in the project.
    list                List ALL components of ALL available targets (specified in 'project_targets.py'). If '-t' is used, list all components of JUST the target specified after '-t'.
    build_target        Build all of the project targets. If '-t' is used, build just the target specified after '-t'.
    clean               Run 'ninja -t clean'.
    clean_build         Run 'ninja -t clean' and then build all of the project targets. If '-t' is used, build just the target specified after '-t'.
    debug               Start a debug session in gdbgui with the specified target. After running, open a browser on the host machine and navigate to 'localhost:PORT' (default: 5000) to
                        see the gdbgui instance.
    docker_bash         Open up Docker in interactive mode.
    run                 Run the specified command in Docker.
    push                Execute 'git add . && git commit -m MESSAGE && git push'.

options:
  -h, --help            show this help message and exit
  -v, --verbose         Verbose output. (Note: Errors are shown regardless of this setting.)
```
7) Later on, feel free to edit or extend `make.py`! It's just a Python script, after all. It's basically begging for someone to add additional command-line flags that utilize things like [pyOCD](https://github.com/pyocd/pyOCD), [pyGDB](https://pypi.org/project/pygdb/), [pyLink](https://pylink.readthedocs.io/en/latest/), or [pyFTDI](https://eblot.github.io/pyftdi/) to create a singular command-line interface for all of your developing, debugging, and testing needs. Alternatively, you could cut out the parts of this project you like (such as using ninja) and leave the rest behind (such as Docker or the Python CLI); they're each independent of the other, more or less.

## References

### Ninja
- https://github.com/wntrblm/Castor_and_Pollux/blob/main/firmware/configure.py
- https://github.com/wntrblm/wintertools/blob/main/wintertools/buildgen.py
- https://github.com/ninja-build/ninja/blob/84986/misc/ninja_syntax.py
- https://jpospisil.com/2014/03/16/replacing-make-with-ninja.html
- https://ninja-build.org/manual.html#_generating_ninja_files_from_code
- https://lwn.net/Articles/706404/
- https://vector-of-bool.github.io/2018/12/20/build-like-ninja-1.html

### Docker
- 2021 EOC

### Misc
- Memfault invoke