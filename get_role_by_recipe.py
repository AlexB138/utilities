#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import subprocess

__author__ = 'alex barnes'


def get_role_by_recipe(target_recipe, verbose=False):
    results = []

    try:
        roles_result = subprocess.check_output("knife role list", shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        if verbose:
            print "Knife role list failed. Following error was returned: "
            print err.output
        return []
    else:
        if roles_result.strip():  # If results aren't an empty string
            # List comprehension that won't include empty strings.
            roles = [role for role in roles_result.split('\n') if role]
        else:
            if verbose:
                print("No values were returned for role list.")
            return []

    for role in roles:
        try:
            runlist_result = subprocess.check_output("knife role show {0} -a run_list".format(role), shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as err:
            if verbose:
                print "Knife role show failed. Following error was returned: "
                print err.output
        else:
            if runlist_result.strip():  # If results aren't an empty string
                parts = runlist_result.split(",")
                recipes = [part[part.find("[") + 1:part.find("]")] for part in parts if part]

                for recipe in recipes:
                    if recipe == target_recipe:
                        results.append(role)
                        break

    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("recipe", type=str, help="Recipe to look for in roles")
    parser.add_argument("-v", "--verbose", action="store_true", default=False, help="Enable verbose output")
    args = parser.parse_args()

    print get_role_by_recipe(args.recipe, args.verbose)


if __name__ == "__main__":
    main()