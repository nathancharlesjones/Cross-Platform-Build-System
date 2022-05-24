#! /usr/bin/env python3

from project_settings import (targets, default_path_to_docker_file, default_docker_name,
                                default_debug_port_number)
from helper import execute_shell_cmd
from ninja_generate import generate_build_dot_ninja_from_targets
import argparse
import os
import sys

def main():
    args = get_command_line_args()
    if args.verbose:
        print(args)

    # TODO: Test that all of the Docker stuff works on Linux, too
    # TODO: Add "build_target" action
    # TODO: Add "clean" action
    # TODO: Add "clean_and_build" action
    # TODO: Add "docker_bash" action
    # TODO: build_docker & build_ninja need to be run from inside build system folder, but run has to be from project folder??
    
    if args.action == 'build_docker':
        cmd = ['docker', 'build', '-t', args.name, args.path]
        execute_shell_cmd(cmd, args.verbose)
    
    elif args.action == 'build_ninja':
        # TODO: Change this to use Docker?
        generate_build_dot_ninja_from_targets(targets, sys.argv[0])
    
    elif args.action == 'run':
        cmd = ['docker', 'run', '-it', '--rm', '-v', '{0}:/app'.format(os.getcwd()), \
                args.name, '/bin/bash', '-c', args.command]
        execute_shell_cmd(cmd, args.verbose)
    
    elif args.action == 'list':
        try:
            import json
            for target in args.target:
                print(json.dumps(targets[target], indent=4, sort_keys=args.sorted))
        except:
            for target in args.target:
                print("*"*50)
                print("\n".join("{0}{1}".format(key.ljust(25, '.'), value) for key, value in targets[target].items()))
                print("*"*50)

    elif args.action == 'debug':
        # TODO: Test connecting to a GDB server on the host. Can I just add 2331:2331 to the port list?
        # TODO: Possible to start a GDB server in the background? If not, add "start_gdb_server" action
        cmd = ['docker', 'run', '-it', '--rm', '-v', '{0}:/app'.format(os.getcwd()), \
                '-p', '{0}:{0}'.format(default_debug_port_number), "--network='host'", args.name, '/bin/bash', \
                '-c', "gdbgui -g {0} -r --port {1} --args {2}".format(targets[args.target].debugger, \
                default_debug_port_number, targets[args.target].target_file_and_path)]
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

def get_command_line_args():
    # TODO: Update help strings
    parser = argparse.ArgumentParser(description="Helper script for interacting with an embedded systems project. Run 'exec.py ACTION -h' for further help information about each action that can be run.")
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Verbose output. (Note: Errors are shown regardless of this setting.)')
    subparsers = parser.add_subparsers(dest='action', required=True)
    
    build_docker_container = subparsers.add_parser('build_docker', help="Builds the Docker container used with the 'run' and 'debug' actions.")
    build_docker_container.add_argument('-p', '--path', default=default_path_to_docker_file, help="Path to Dockerfile to be used when building the Docker image; default is '{0}'.".format(default_path_to_docker_file))
    build_docker_container.add_argument('-n', '--name', default=default_docker_name, help="Name to be associated with the Docker image once built; default is '{0}'.".format(default_docker_name))

    build_ninja_file = subparsers.add_parser('build_ninja', help='''(Re)Build the file 'build.ninja' according to the project specifications defined in 'project_targets.py'. Once generated, used "exec.py run -c 'ninja'" to use Docker to build all targets in the project.''')

    run_docker_cmd = subparsers.add_parser('run', help="Run the specified command in Docker.")
    run_docker_cmd.add_argument('-n', '--name', default=default_docker_name, help="Docker image to be used; default is {0}.".format(default_docker_name))
    run_docker_cmd.add_argument('-c', '--command', required=True, help="The command to be run.")

    #flash_binary = subparsers.add_parser('flash', help="Flash the specified binary to an attached MCU.")
    #flash_binary.add_argument('-t', '--target', choices=list(targets), required=True, help="Target that is to be flashed to the attached MCU.")

    list_targets = subparsers.add_parser('list', help="List all components of all available targets (specified in 'project_targets.py'). If '-t' is used, list all components of just the target specified after '-t'.")
    list_targets.add_argument('-t', '--target', nargs=1, choices=list(targets), default=list(targets), help="Target to be listed.")
    list_targets.add_argument('-s', '--sorted', dest="sorted", default=False, action='store_true', help="Sort the target fields (such as 'name' or 'c_flags') alphabetically if specified. Only works if json library is already installed.")

    start_debug_session = subparsers.add_parser('debug', help="Start a debug session in gdbgui with the specified target. After running, open a browser on the host machine and navigate to 'localhost:PORT' (default: {0}) to see the gdbgui instance.".format(default_debug_port_number))
    start_debug_session.add_argument('-n', '--name', default=default_docker_name, help="Docker image to be used; default is '{0}'.".format(default_docker_name))
    start_debug_session.add_argument('-t', '--target', choices=list(targets), required=True, help="Target that is to be debugged.")
    start_debug_session.add_argument('-p', '--port', default=default_debug_port_number, help="Port number to be used to connect to gdbgui; default is {0}.".format(default_debug_port_number))

    git_push = subparsers.add_parser('push', help="Execute 'git add . && git commit -m MESSAGE && git push'.")
    git_push.add_argument('-m', '--message', required=True, help="The commit message.")

    return parser.parse_args()

if __name__ == "__main__":
    main()
