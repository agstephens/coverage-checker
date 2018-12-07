# -*- coding: utf-8 -*-

"""Main module."""

import os
import logging

from coverage_checker.utils import get_files_and_dirs


log = logging.getLogger(__file__)


def check_coverage(top_dir, depth, ignores=None, ignore_symlinks=False, ignore_files=False,
                   ignore_dirs=False, ignore_empty_dirs=False):
    files, end_dirs, empty_dirs = get_files_and_dirs(top_dir, ignores=ignores, ignore_symlinks=ignore_symlinks,
                                                     ignore_files=ignore_files, ignore_dirs=ignore_dirs,
                                                     ignore_empty_dirs=ignore_empty_dirs)

    dir_errors = []
    file_errors = []

    for dr in end_dirs:
        items = dr.strip(os.sep).split(os.sep)

        if len(items) != depth:
            dir_errors.append(dr)

    for fpath in files:
        log.warning('TODO: Not yet checking files here!!!')
        if 0:
            file_errors.append(fpath)

    report = ''

    resp = [0, 0, 0, '']

    if dir_errors:
        report += 'Directories found that do not match expected depth:\n'

        for dr in dir_errors:
            resp[0] += 1
            report += '\t{}\n'.format(dr)

    if file_errors:
        report += '\nNon-uniform files found:\n'

        for fpath in file_errors:
            resp[1] += 1
            report += '\t{}\n'.format(fpath)

    if empty_dirs:
        report += '\nThe following empty directories were found:\n'

        for empty in empty_dirs:
            resp[2] += 1
            report += '\t{}\n'.format(empty)

    resp[3] = report
    return resp




