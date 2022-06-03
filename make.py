#! /usr/bin/env python3

import os
import sys

# Allow Python to find 'project_settings.py'. Assumes 'project_settings.py' is in
# the folder one level higher than 'make.py'.
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from project_settings import (targets, default_path_to_docker_file, default_docker_name,
                                    default_debug_port_number)
except:
    print("Could not locate project_settings.py.")
    targets = {}
    default_path_to_docker_file = '.'
    default_docker_name = 'no-name'
    default_debug_port_number = '9999'

from helper import execute_shell_cmd
from ninja_generate import generate_build_dot_ninja_from_targets
import argparse

def main():
    args = get_command_line_args()
    if args.verbose:
        print(args)

    if args.action == 'build_docker':
        cmd = ['docker', 'build', '-t', args.name, args.path]
        execute_shell_cmd(cmd, args.verbose)
    
    elif args.action == 'build_ninja':
        generate_build_dot_ninja_from_targets(targets, sys.argv[0])
        #cmd = ['docker', 'run', '-it', '--rm', '-v', '{0}:/app'.format(os.getcwd()), \
        #        args.name, '/bin/bash', '-c', './ninja_generate.py']
        #execute_shell_cmd(cmd, args.verbose)
    
    elif args.action == 'list':
        for target in args.target:
            print(targets[target])
    
    elif args.action == 'build_target':
        cmd = ['docker', 'run', '-it', '--rm', '-v', '{0}:/app'.format(os.getcwd()), \
                args.name, '/bin/bash', '-c', 'ninja ' + ' '.join(args.target)]
        execute_shell_cmd(cmd, args.verbose)
    
    elif args.action == 'clean':
        cmd = ['docker', 'run', '-it', '--rm', '-v', '{0}:/app'.format(os.getcwd()), \
                args.name, '/bin/bash', '-c', 'ninja -t clean']
        execute_shell_cmd(cmd, args.verbose)
    
    elif args.action == 'clean_build':
        cmd = ['docker', 'run', '-it', '--rm', '-v', '{0}:/app'.format(os.getcwd()), \
                args.name, '/bin/bash', '-c', 'ninja -t clean']
        execute_shell_cmd(cmd, args.verbose)
        cmd = ['docker', 'run', '-it', '--rm', '-v', '{0}:/app'.format(os.getcwd()), \
                args.name, '/bin/bash', '-c', 'ninja ' + ' '.join(args.target)]
        execute_shell_cmd(cmd, args.verbose)
    
    elif args.action == 'debug':
        print("Open gdbgui by navigating a browser to 'localhost:PORT' (default: 5000).\n"
              "Connect to a gdbserver that's running on the host by entering the following\n"
              "at the gdb prompt:\n"
              "    - For Mac/Windows: 'target extended-remote host.docker.internal:SERVER_PORT'\n"
              "    - For Linux:       'target extended-remote 172.17.0.1:SERVER_PORT'")
        cmd = ['docker', 'run', '-it', '--rm', '-v', '{0}:/app'.format(os.getcwd()), \
                '-p', '{0}:{0}'.format(args.port), args.name, '/bin/bash', \
                '-c', "gdbgui -g {0} -r --port {1} --args {2}".format(targets[args.target].debugger, \
                args.port, targets[args.target].target_file_and_path)]
        execute_shell_cmd(cmd, args.verbose)
    
    elif args.action == 'docker_bash':
        cmd = ['docker', 'run', '-it', '--rm', '-v', '{0}:/app'.format(os.getcwd()), \
                args.name, '/bin/bash']
        execute_shell_cmd(cmd, args.verbose)
    
    elif args.action == 'run':
        cmd = ['docker', 'run', '-it', '--rm', '-v', '{0}:/app'.format(os.getcwd()), \
                args.name, '/bin/bash', '-c', args.command]
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
    parser = argparse.ArgumentParser(description="Helper script for interacting with an embedded systems project. Run 'make.py ACTION -h' for further help information about each action that can be run.")
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Verbose output. (Note: Errors are shown regardless of this setting.)')
    subparsers = parser.add_subparsers(dest='action', required=True)
    
    build_docker_container = subparsers.add_parser('build_docker', help="Builds the Docker container used to build and debug the project.")
    build_docker_container.add_argument('-p', '--path', default=default_path_to_docker_file, help="Path to Dockerfile to be used when building the Docker image; default is '{0}'.".format(default_path_to_docker_file))
    build_docker_container.add_argument('-n', '--name', default=default_docker_name, help="Name to be associated with the Docker image once built; default is '{0}'.".format(default_docker_name))

    build_ninja_file = subparsers.add_parser('build_ninja', help='''(Re)Build the file 'build.ninja' according to the project specifications defined in 'project_targets.py'. Once generated, used "make.py build_target" to use Docker to build all targets in the project.''')

    list_targets = subparsers.add_parser('list', help="List ALL components of ALL available targets (specified in 'project_targets.py'). If '-t' is used, list all components of JUST the target specified after '-t'.")
    list_targets.add_argument('-t', '--target', nargs=1, choices=list(targets), default=list(targets), help="Target to be listed.")

    build_target = subparsers.add_parser('build_target', help="Build all of the project targets. If '-t' is used, build just the target specified after '-t'.")
    build_target.add_argument('-n', '--name', default=default_docker_name, help="Docker image to be used; default is {0}.".format(default_docker_name))
    build_target.add_argument('-t', '--target', nargs=1, choices=list(targets), default=list(targets), help="Target to be built.")

    clean = subparsers.add_parser('clean', help="Run 'ninja -t clean'.")
    clean.add_argument('-n', '--name', default=default_docker_name, help="Docker image to be used; default is {0}.".format(default_docker_name))

    clean_and_build = subparsers.add_parser('clean_build', help="Run 'ninja -t clean' and then build all of the project targets. If '-t' is used, build just the target specified after '-t'.")
    clean_and_build.add_argument('-n', '--name', default=default_docker_name, help="Docker image to be used; default is {0}.".format(default_docker_name))
    clean_and_build.add_argument('-t', '--target', nargs=1, choices=list(targets), default=list(targets), help="Target to be built.")

    # TODO: Figure out how to clean up a specific target in ninja with my build.ninja file
    #clean = subparsers.add_parser('clean', help="Clean project files. Runs 'ninja -t clean' by default. To specify a target to be cleaned, use the -t option.")
    #clean.add_argument('-n', '--name', default=default_docker_name, help="Docker image to be used; default is {0}.".format(default_docker_name))
    #clean.add_argument('-t', '--target', nargs=1, choices=list(targets), default=list(targets), help="Target to be built.")

    start_debug_session = subparsers.add_parser('debug', help="Start a debug session in gdbgui with the specified target. After running, open a browser on the host machine and navigate to 'localhost:PORT' (default: {0}) to see the gdbgui instance. Start a gdb server on the host machine and connect to it using either (1) 'target extended-remote host.docker.internal:PORT' (for Windows/Mac) or (2) 'target extended-remote 172.17.0.1:PORT' (for Linux).".format(default_debug_port_number))
    start_debug_session.add_argument('-n', '--name', default=default_docker_name, help="Docker image to be used; default is '{0}'.".format(default_docker_name))
    start_debug_session.add_argument('-t', '--target', choices=list(targets), required=True, help="Target that is to be debugged.")
    start_debug_session.add_argument('-p', '--port', default=default_debug_port_number, help="Port number to be used to connect to gdbgui; default is {0}.".format(default_debug_port_number))

    docker_bash = subparsers.add_parser('docker_bash', help='''Open up Docker in interactive mode.''')
    docker_bash.add_argument('-n', '--name', default=default_docker_name, help="Name to be associated with the Docker image once built; default is '{0}'.".format(default_docker_name))

    run_docker_cmd = subparsers.add_parser('run', help="Run the specified command in Docker.")
    run_docker_cmd.add_argument('-n', '--name', default=default_docker_name, help="Docker image to be used; default is {0}.".format(default_docker_name))
    run_docker_cmd.add_argument('-c', '--command', required=True, help="The command to be run.")
    
    git_push = subparsers.add_parser('push', help="Execute 'git add . && git commit -m MESSAGE && git push'.")
    git_push.add_argument('-m', '--message', required=True, help="The commit message.")

    return parser.parse_args()

if __name__ == "__main__":
    main()
