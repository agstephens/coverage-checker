import os
import re
from os import path as op
import itertools

from collections import OrderedDict


class DirScanner(object):

    def __init__(self, top_dir, ignores=None, ignore_symlinks=False, ignore_files=False,
                 ignore_dirs=False, ignore_empty_dirs=False):

        # Check top_dir is valid at start
        if not op.isdir(top_dir):
            raise Exception('Top-level item is not a valid directory: {}'.format(top_dir))

        if not ignores:
            ignores = []

        self.ignores = [re.compile(pattn) for pattn in ignores]
        self.ignore_symlinks = ignore_symlinks
        self.ignore_files = ignore_files
        self.ignore_dirs = ignore_dirs
        self.ignore_empty_dirs = ignore_empty_dirs

        self.files = []
        self.dirs = []
        self.empties = []

        self._scan(top_dir)
        self._sort_results()

    def _do_ignore(self, item):
        for pattn in self.ignores:
            if pattn.match(item):
                return True

    def _scan(self, dr):
        items = os.listdir(dr)

        # Test for empty directory
        if len(items) == 0:
            if not self.ignore_empty_dirs:
                self.empties.append(dr)
            return

        subdirs_found = False

        for item in items:
            if self._do_ignore(item):
                continue

            path = op.join(dr, item)

            if op.isdir(path):
                subdirs_found = True
                self._scan(path)

            elif op.islink(path) and self.ignore_symlinks:
                continue

            elif not self.ignore_files:
                self.files.append(path)

        if not subdirs_found and not self.ignore_dirs:
            self.dirs.append(dr)

    def _sort_results(self):
        self.files = sorted(self.files)
        self.dirs = sorted(self.dirs)
        self.empties = sorted(self.empties)


def get_files_and_dirs(top_dir, ignores=None, ignore_symlinks=False, ignore_files=False,
                       ignore_dirs=False, ignore_empty_dirs=False):

    scanner = DirScanner(top_dir, ignores=ignores, ignore_symlinks=ignore_symlinks,
                         ignore_files=ignore_files, ignore_dirs=ignore_dirs, ignore_empty_dirs=ignore_empty_dirs)

    return scanner.files, scanner.dirs, scanner.empties


def get_all_path_combinations(dct):
    assert(isinstance(dct, OrderedDict))

    paths = None

    for key, values in dct.items():

        # First time around - need to just add keys
        if not paths:
            paths = [value for value in values]
        # Subsequently, build list each time
        else:
            paths = [os.path.join(path, value) for path in paths
                     for value in values]

    return sorted(paths)




