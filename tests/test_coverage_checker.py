#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `coverage_checker` package."""

import pytest
import os

from click.testing import CliRunner

from coverage_checker.coverage_checker import check_coverage
from coverage_checker import cli


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'coverage_checker.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output


def test_check_coverage_success_1(tmpdir):
    top_dir = 'top_dir'
    base = tmpdir.mkdir(top_dir)
    paths = ('a/b/c/d/1.dat', 'a/b/c/d/2.dat')
    files = []

    for path in paths:
        files.append(base.join(path))
        files[-1].write('data', ensure=True)

    tmp_dir = str(files[0].realpath()).replace(os.path.join(top_dir, paths[0]), '')
    os.chdir(tmp_dir)
    resp = check_coverage(top_dir, depth=5)
    assert(resp == [0, 0, 0, ''])


def test_check_coverage_success_2(tmpdir):
    top_dir = 'top_dir'
    base = tmpdir.mkdir(top_dir)
    paths = ('a1/b/c/d/1.dat', 'a2/b/c/d/2.dat')
    files = []

    for path in paths:
        files.append(base.join(path))
        files[-1].write('data', ensure=True)

    tmp_dir = str(files[0].realpath()).replace(os.path.join(top_dir, paths[0]), '')
    os.chdir(tmp_dir)
    resp = check_coverage(top_dir, depth=4)
    assert(resp[0] == 2), resp


