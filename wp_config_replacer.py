#!/usr/bin/env python3
"""
Replaces the random/crypto variable definitions in a wp-config.php file.
Usage is `wp_config_replacer.py path/to/wp-config-sample.php > path/to/wp-config.php`
"""

from io import open
import random
import re
import string
import sys
try:
    from urllib2 import urlopen  # Python 2
except ImportError:
    from urllib.request import urlopen  # Python 3

# WP_SALT_API = "https://api.wordpress.org/secret-key/1.1/salt/"  # Unused. We generate our own strings.

"""
Regular expression to find PHP define functions
"""
DEFINE_REGEX = re.compile(
    r"""define\s*\(\s*['"](?P<name>[A-Z_]+)['"]\s*,\s*['"](?P<value>[^'"]*)['"]\s*\)\s*;"""
)

"""
These characters are in string.punctuation but can't be in our random strings.
"""
DISALLOWED_CHARS_REGEX = re.compile(r"""['"\\]""")  # characters that can't be in our secure strings

"""
These are the variables we are interested in setting a value forin wp-config.php
"""
SALT_CONSTANTS = (
    "AUTH_KEY",
    "SECURE_AUTH_KEY",
    "LOGGED_IN_KEY",
    "NONCE_KEY",
    "AUTH_SALT",
    "SECURE_AUTH_SALT",
    "LOGGED_IN_SALT",
    "NONCE_SALT",
)


def set_random_strings_in_wpconfig(wpconfig):
    """
    Read in the file given the path to a wp-config.php file and return its contents with secure, random strings
    filled in for the

    :param wpconfig:
    :return:
    """
    with open(wpconfig, "r") as infile:
        content = infile.read()
    result = DEFINE_REGEX.sub(find_and_replace, content)
    return result


def find_and_replace(matchobj):
    """
    Passed into a re.sub function for its repl value, checks to see if this is
    one of the SALT_CONSTANTS to replace and then generates a random string to
    set its value to. Leaves other constants untouched.

    :param matchobj: the Match object passed in from a re.sub
    :return: the define with a new random string value (or the same value if this isn't one of SALT/KEY values)
    """
    constant = matchobj.group("name")
    if constant not in SALT_CONSTANTS:
        return matchobj.group()
    constr = "'%s'," % constant
    random_string = generate_random_string(64)
    result = "define(%-19s '%s');" % (constr, random_string)
    return result


def generate_random_string(length=64):
    """
    Generates a secure, random string of a given length that is compatible with PHP KEY/SALT defines
    in the wp-config.php file.
    Uses the method described here: https://stackoverflow.com/a/23728630/489667
    The random strings returned from https://api.wordpress.org/secret-key/1.1/salt/ are 64 characters long.

    :param length: the length of the string to generate (defaults to 64, same as Wordpress seems to use)
    :return: a secure, random string of the requested length that is compatible with a PHP define
    """

    punctuation = DISALLOWED_CHARS_REGEX.sub("", string.punctuation)  # remove \, ", and '
    chars = string.ascii_letters + string.digits + punctuation + " "

    # https://stackoverflow.com/a/23728630/489667
    randstr = ''.join(
        random.SystemRandom().choice(chars) for _ in range(length))
    return randstr


if __name__ == "__main__":
    try:
        path_to_wpconfig = sys.argv[1]
    except IndexError as ex:
        print("Usage: wp_config_replacer.py path/to/wp-config-sample.php > path/to/wp-config.php", file=sys.stderr)
        exit(-1)
        raise ex  # never gets here but gets rid of an inspection warning
    newcontents = set_random_strings_in_wpconfig(path_to_wpconfig)
    print(newcontents)
