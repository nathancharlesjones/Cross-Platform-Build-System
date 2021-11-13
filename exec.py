#! /usr/bin/env python3

import argparse
import subprocess
import docker
import os

def execute_shell_cmd(cmd, verbose):
    if verbose:
        print("Executing: " + cmd)
    process = subprocess.run([cmd], shell=True, text=True)
    if verbose and process.stdout:
        print("Output: " + process.stdout)

def main():
    parser = argparse.ArgumentParser(description="Helper script for interacting with an embedded systems project.")
    #parser.add_argument('-n', '--ninja', action='store', help='Use Docker to run the ninja command which follows this flag. Multi-word commands should be wrapped in single-quotes.')
    #parser.add_argument('-t', '--target', action='store', dest='target', default='all', help='Specify a single target to be built, cleaned, purified, or zipped. All targets are built if none is specified.')
    #non_build_option_group = parser.add_mutually_exclusive_group(required=True)
    #non_build_option_group.add_argument('-b', '--build', action='store_const', const='build', dest='execute', help='Build the specified target (or all targets if no target was specified).')
    #non_build_option_group.add_argument('-c', '--clean', action='store_const', const='clean', dest='execute', help='Clean the build folder for the specified target (or for all targets if no target was specified). Removes all files (such as object and dependency files) EXCEPT for each of the build targets and any zipped folders.')
    #non_build_option_group.add_argument('-p', '--purify', action='store_const', const='purify', dest='execute', help='Purify the build folder. Removes the build folder and all subfiles and subdirectories for each target.')
    #non_build_option_group.add_argument('-z', '--zip', action='store_const', const='zip', dest='execute', help='Purify the build folder. Removes the build folder and all subfiles and subdirectories for each target.')
    #non_build_option_group.add_argument('-l', '--list', action='store_const', const='list', dest='execute', help="List the available target names, as defined in 'project_targets.py'. When used with verbose option, list all settings for all available targets.")
    #parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Verbose output. Show the recipe configuration prior to it being built and show all executing commands as they are being run. (Note: Errors are shown regardless of this setting.)')

    # New CLIs:
    #  1) Build Docker container -c --build-container
    #     - Container name listed in exec.py as a variable (file?), allowed to be overridden on the command-line
    #  2) Generate build.ninja -g --generate
    #  3) Run docker command -r --docker-run
    #     - Build all with "-r 'ninja'"
    #     - Build a single target with "-r 'ninja -t TARGET'"
    #     - Clean all with "-r 'ninja -t clean'"
    #     - Run executable with "-r './path/to/executable'"
    #  4) Flash binary to target -f --flash (REQUIRES TARGET)
    #     - J-Link/OpenOCD settings stored in a file; can specify different input file or alternates on the command-line
    #  5) List -l --list
    #     - Can be combined with -v to get full target descriptions
    #     - Target optional, all by default
    #  6) Start debug session -d --debug (REQUIRES ARCH)
    #     - Will start a gdbgui session corresponding to the arch specified and exposes the port
    #     - Starts and connects to GDB server on debug adapter?
    #     - Loads target file?
    #     - Runs gdb init script?
    #     - Other stuff I can do with pyGDB?
    #  7) Git push -p --git-push
    #     - Allow for overridding the UN/PW on command line
    #  8) Verbose output -v --verbose
    args = parser.parse_args()

    client = docker.from_env()

    print(client.containers.run('devenv-simple-build-system', volumes=["{0}:/app".format(os.getcwd())], command='ninja').decode("utf-8"))
    #execute_shell_cmd("docker run -it --rm -v PWD:/app devenv-simple-build-system /bin/bash -c 'echo Starting program'", True)
    #execute_shell_cmd("docker run -it --rm -v $\{PWD}:/app devenv-simple-build-system /bin/bash -c '{0}'".format(args.ninja), True)

if __name__ == "__main__":
    main()
