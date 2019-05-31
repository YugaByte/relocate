# -*- coding: utf-8 -*-

# Copyright (c) 2019 YugaByte, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied.  See the License for the specific language governing permissions and limitations under
# the License.

import argparse
import os
import sys
import subprocess
import fnmatch
import logging
import json


METADATA_FILE_NAME = 'relpack_metadata.json'


def remove_prefixes_of_others(values):
    """
    Removes strings that are prefixes of other strings and returns the result.
    """
    to_remove = set()

    for value in values:
        for other_value in values:
            if other_value != value and other_value.startswith(value):
                to_remove.add(value)
    return sorted(set(values) - set(to_remove))


class YPackTool():

    def __init__(self):
        self.args = None


    def parse_args(self, args):
        parser = argparse.ArgumentParser(description='ypack')
        subparsers = parser.add_subparsers(help='sub-command help')
        parser_for_create = subparsers.add_parser('create', help='create an archive')
        parser_for_create.add_argument(
            '--src',
            help='Source directory to package',
            required=True)
        parser_for_create.add_argument(
            '--dest',
            help='Directory to create the package in',
            required=True)
        parser_for_create.add_arguments(
            '--',
            help=
        )
        parser_for_create.add_argument(
            '--install_dir_pattern',
            help='Override the pattern corresponding to the installation directory that we will '
                 'search for in binary files. If this is not specified, the source directory '
                 'absolute path itself is used.')
        parser_for_create.set_defaults(func=self.create_archive)

        self.args = parser.parse_args(args)

    def run(self):
        self.args.func()

    def create_archive(self):
        src_dir = self.args.src_dir
        if not os.path.isdir(src_dir):
            raise IOError("Source directory '%s' does not exist" % src_dir)
        if not os.path.isdir(self.dest_parent_dir):
            raise IOError("Destination directory '%s' does not exist" % self.dest_parent_dir)

        # The directory that we'll be searching might be the link target of the specified source
        # directory (if the source directory is a symlink), while the pattern is always based on
        # the source directory path itself.
        default_install_dir_pattern = remove_prefixes_of_others([
            os.path.abspath(src_dir),
            os.path.realpath(src_dir)
        ])

        logging.info("self.args.install_dir_pattern=%s", self.args.install_dir_pattern)
        key_to_patterns = {
            'install_dir': [self.args.install_dir_pattern] or default_install_dir_pattern
        }
        for pattern_list in key_to_patterns.values():
            assert isinstance(pattern_list, list)
        logging.info("key_to_patterns=%s", key_to_patterns)

        dir_to_search = src_dir

        pattern_values = set()
        for pattern_key in key_to_patterns:
            pattern_values |= set(key_to_patterns[pattern_key])
        logging.info("pattern_values=%s", pattern_values)
        occurrences = {}
        for pattern_value in sorted(pattern_values):
            offsets_by_file = {}
            occurrences[pattern_value] = offsets_by_file
            logging.info("Searching for pattern %s in directory %s",
                         pattern_value, dir_to_search)
            find_process = subprocess.Popen(
                    ['find', dir_to_search, '-type', 'f',
                     '-exec', 'grep', '-Habo', pattern_value, '{}', ';'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)
            out, err = find_process.communicate()
            expected_suffix = ':' + pattern_value
            for line in out.decode('utf-8').split('\n'):
                line = line.strip()
                if not line:
                    continue
                if not line.endswith(expected_suffix):
                    raise ValueError("Line does not end with expected suffix '%s': %s" % (
                        expected_suffix, line))
                line = line[:-len(expected_suffix)]
                try:
                    file_path, byte_offset_str = line.rsplit(':')
                except ValueError as ex:
                    raise ValueError(str(ex) + " while processing line: " + line)
                rel_path = os.path.relpath(file_path, dir_to_search)
                if rel_path not in offsets_by_file:
                    offsets_by_file[rel_path] = []
                offsets_by_file[rel_path].append(int(byte_offset_str))
        package_metadata = {
            'patterns': key_to_patterns,
            'occurrences': occurrences
        }
        with open('/tmp/occurrences.json', 'w') as output_file:
            json.dump(package_metadata, output_file, indent=2)


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(filename)s:%(lineno)d] %(asctime)s %(levelname)s: %(message)s")
    tool = YPackTool()
    tool.parse_args(sys.argv[1:])
    tool.run()


if __name__ == '__main__':
    main()
