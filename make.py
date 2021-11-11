#! /bin/python3

from helper import (get_command_line_args, target_was_specified,
                    valid_target_name, remove_from_dict_all_except)

from project_targets import targets

def main():
    # Start the CLI and parse any command line values/flags
    args = get_command_line_args()

    # Overwrite target dictionary if only one target was selected on the command line
    # (or raise a ValueError if the target that was specified is not one that was defined
    # in project_targets.py)
    if target_was_specified(args):
        if valid_target_name(targets, args.target):
            remove_from_dict_all_except(targets, args.target)
        else:
            raise ValueError("{0} not a valid target.".format(args.target))

    # For all targets in the target dictionary (either all targets or just the one specified),
    # execute the desired command (list, clean, purify, zip, or build)
    for target in targets:
        targets[target].execute(args.execute, args.verbose)
    
if __name__ == "__main__":
    main()
