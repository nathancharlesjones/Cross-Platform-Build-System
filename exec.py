#! /usr/bin/env python3

from helper import execute_shell_cmd
from project_settings import targets, docker_file, docker_name
from ninja_generate import generate_build_dot_ninja_from_targets
import argparse
import docker
import os

# Update help strings

def main():
    parser = argparse.ArgumentParser(description="Helper script for interacting with an embedded systems project.")
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Verbose output. Show the recipe configuration prior to it being built and show all executing commands as they are being run. (Note: Errors are shown regardless of this setting.)')
    subparsers = parser.add_subparsers(dest='action', required=True)
    
    build_docker_container = subparsers.add_parser('build_docker', help="Builds the Docker container specified in a Dockerfile in the same folder as this script with the name specified.")
    build_docker_container.add_argument('-f', '--file', default=docker_file, help="Override the default path to Dockerfile of '{0}'.".format(docker_file))
    build_docker_container.add_argument('-n', '--name', default=docker_name, help="Override the default name of {0}.".format(docker_name))

    build_ninja_file = subparsers.add_parser('build_ninja', help="(Re)Build the file 'build.ninja' according to the project specifications defined in 'project_targets.py'.")

    run_docker_cmd = subparsers.add_parser('run', help="Run the specified command in Docker.")
    run_docker_cmd.add_argument('-c', '--command', required=True, help="The command to run.")
    run_docker_cmd.add_argument('-n', '--name', default=docker_name, help="Override the name in <> with a new name.")

    flash_binary = subparsers.add_parser('flash', help="Flash the specified binary to an attached MCU.")
    flash_binary.add_argument('-t', '--target', choices=list(targets), help="Target that is to be flashed to the attached MCU.")

    list_targets = subparsers.add_parser('list', help="List the available targets (specified in 'project_targets.py'). Use with '-v' to see all components of the specified target.")
    list_targets.add_argument('-t', '--target', nargs=1, choices=list(targets), default=list(targets), help="Target to be listed.")

    start_debug_session = subparsers.add_parser('debug', help="List the available targets (specified in 'project_targets.py'). Use with '-v' to see all components of the specified target.")
    start_debug_session.add_argument('-n', '--name', default=docker_name, help="Override the name in <> with a new name.")
    #  6) Start debug session -d --debug (REQUIRES ARCH)
    #     - Will start a gdbgui session corresponding to the arch specified and exposes the port
    #     - Starts and connects to GDB server on debug adapter?
    #     - Loads target file?
    #     - Runs gdb init script?
    #     - Other stuff I can do with pyGDB?

    git_push = subparsers.add_parser('push', help="Execute 'git add . && git commit -m MESSAGE && git push'.")
    git_push.add_argument('-m', '--message', required=True, help="The commit message.")
    git_push.add_argument('-u', '--username', help="Override the defualt username.")
    git_push.add_argument('-p', '--password', help="Override the default password.")

    args = parser.parse_args()
    
    if args.action == 'build_docker':
        #client = docker.from_env()
        #client.images.build(dockerfile=args.file, tag=args.name)
        execute_shell_cmd('docker build .',args.verbose)
    elif args.action == 'build_ninja':
        generate_build_dot_ninja_from_targets(targets)
    elif args.action == 'run':
        client = docker.from_env()
        container = client.containers.run(image=args.name, volumes=["{0}:/app".format(os.getcwd())], command=args.command, detach=True, auto_remove=True)
        for line in container.logs(stream=True):
            print(line.strip().decode('utf-8'))
    elif args.action == 'flash':
        # Not working
        pass
    elif args.action == 'list':
        for target in args.target:
            print(targets[target])
    elif args.action == 'debug':
        # Not working
        client = docker.from_env()
        client.containers.run(image=args.name, volumes=["{0}:/app".format(os.getcwd())], ports={"5000/tcp:5000"}, command="gdbgui -r --port 5000").decode("utf-8")
    elif args.action == 'push':
        # Not working
        # Switch to GitPython (https://gitpython.readthedocs.io/en/stable/tutorial.html#tutorial-label)
        execute_shell_cmd("git add .", args.verbose)
        #execute_shell_cmd('''git commit -m "{0}"'''.format(args.message),args.verbose)
        #execute_shell_cmd("git push".format(args.message),args.verbose)
        #execute_shell_cmd("git add . && git commit -m \"{0}\" && git push".format(args.message),args.verbose)
    else:
        raise ValueError("Unknown action selected: {0}".format(args.action))

if __name__ == "__main__":
    main()
