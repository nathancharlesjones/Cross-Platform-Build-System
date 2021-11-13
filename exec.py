#! /usr/bin/env python3

from helper import execute_shell_cmd
from project_targets import targets
import argparse
import subprocess
import docker
import os

def main():
    parser = argparse.ArgumentParser(description="Helper script for interacting with an embedded systems project.")
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Verbose output. Show the recipe configuration prior to it being built and show all executing commands as they are being run. (Note: Errors are shown regardless of this setting.)')
    subparsers = parser.add_subparsers(dest='action', required=True)
    
    build_docker_container = subparsers.add_parser('build_docker', help="Builds the Docker container specified in a Dockerfile in the same folder as this script with the name specified.")
    build_docker_container.add_argument('-n', '--name', help="Override the name in <> with a new name.")

    build_ninja_file = subparsers.add_parser('build_ninja', help="(Re)Build the file 'build.ninja' according to the project specifications defined in 'project_targets.py'.")

    run_docker_cmd = subparsers.add_parser('run', help="Run the specified command in Docker.")
    run_docker_cmd.add_argument('-c', '--command', required=True, help="The command to run.")
    run_docker_cmd.add_argument('-n', '--name', help="Override the name in <> with a new name.")

    flash_binary = subparsers.add_parser('flash', help="Flash the specified binary to an attached MCU.")
    flash_binary.add_argument('-t', '--target', choices=list(targets), help="Target that is to be flashed to the attached MCU.")

    list_targets = subparsers.add_parser('list', help="List the available targets (specified in 'project_targets.py'). Use with '-v' to see all components of the specified target.")
    list_targets.add_argument('-t', '--target', choices=list(targets), help="Target to be listed.")

    start_debug_session = subparsers.add_parser('debug', help="List the available targets (specified in 'project_targets.py'). Use with '-v' to see all components of the specified target.")

    git_push = subparsers.add_parser('push', help="Execute 'git add . && git commit -m MESSAGE && git push'.")
    git_push.add_argument('-m', '--message', required=True, help="The commit message.")
    git_push.add_argument('-u', '--username', help="Override the defualt username.")
    git_push.add_argument('-p', '--password', help="Override the default password.")

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
    print(args)
    
    if args.action == 'build_docker':
        # Build docker file
        pass
    elif args.action == 'build_ninja':
        generate_build_dot_ninja_from_targets(targets)
    elif args.action == 'run':
        client = docker.from_env()
        print(client.containers.run('devenv-simple-build-system', volumes=["{0}:/app".format(os.getcwd())], command=args.command).decode("utf-8"))
    elif args.action == 'flash':
        pass
    elif args.action == 'list':
        if args.target:
            print(targets[args.target])
        else:
            for target in targets:
                print(targets[target])
    elif args.action == 'debug':
        #print(client.containers.run('devenv-simple-build-system', volumes=["{0}:/app".format(os.getcwd())], command=args.command).decode("utf-8"))
        pass
    elif args.action == 'push':
        execute_shell_cmd("git add . && git commit -m \"{0}\" && git push".format(args.message),args.verbose)
    else:
        raise ValueError("Unknown action selected: {0}".format(args.action))

if __name__ == "__main__":
    main()
