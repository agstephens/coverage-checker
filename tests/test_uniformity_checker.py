#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `uniformity_checker` package."""

import pytest
import os


from coverage_checker.uniformity_checker import check_uniformity



TOP_DIR = 'top_dir'
SYMLINK_TARGET = '/tmp/test-symlink'


def setup():
    with open(SYMLINK_TARGET, 'w') as writer:
        writer.write('hi')


def teardown():
    os.remove(SYMLINK_TARGET)


def _create_paths_and_enter_dir(tmpdir, items):

    base = tmpdir.mkdir(TOP_DIR)
    paths = []

    for item in items:
        _ = base.join(item)

        # It is a file if '.' found in name
        if _.basename == 'symlink':
            _.mksymlinkto(SYMLINK_TARGET)
        elif '.' in _.basename:
            _.write('data', ensure=True)
        else:
            _.ensure(dir=True)

        paths.append(_)

    os.chdir(base.dirname)
    return paths


def test_check_coverage_success_1(tmpdir):
    paths = ('a/b/c/d/1.dat', 'a/b/c/d/2.dat')
    _create_paths_and_enter_dir(tmpdir, paths)

    resp = check_coverage(TOP_DIR, depth=5)
    assert(resp == [0, 0, 0, ''])

