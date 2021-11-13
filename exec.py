#! /usr/bin/env python3

from helper import execute_shell_cmd
from project_settings import targets, docker_file, docker_name
from ninja_generate import generate_build_dot_ninja_from_targets
import argparse
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
        # Add options for new filepath, name
        cmd = ['docker', 'build', '.']
        execute_shell_cmd(cmd,args.verbose)
    elif args.action == 'build_ninja':
        generate_build_dot_ninja_from_targets(targets)
    elif args.action == 'run':
        cmd = ['docker', 'run', '-it', '--rm', '-v', '{0}:/app'.format(os.getcwd()), args.name, '/bin/bash', '-c', args.command]
        execute_shell_cmd(cmd, args.verbose)
    elif args.action == 'flash':
        # Not working
        pass
    elif args.action == 'list':
        for target in args.target:
            print(targets[target])
    elif args.action == 'debug':
        cmd = ['docker', 'run', '-it', '--rm', '-v', '{0}:/app'.format(os.getcwd()), '-p 5000:5000', args.name, '/bin/bash', '-c', "gdbgui -r --port 5000"]
        execute_shell_cmd(cmd, args.verbose)
    elif args.action == 'push':
        cmd = ['git', 'add', '.']
        execute_shell_cmd(cmd, args.verbose)
        cmd = ['git', 'commit', '-m', args.message]
        execute_shell_cmd(cmd, args.verbose)
        cmd = ['git', 'push']
        execute_shell_cmd(cmd, args.verbose)
    else:
        raise ValueError("Unknown action selected: {0}".format(args.action))

if __name__ == "__main__":
    main()
