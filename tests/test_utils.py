import os
from collections import OrderedDict

from coverage_checker.utils import get_all_path_combinations


def test_get_all_path_combinations():
    facets = OrderedDict([('a', ['1', '2']), ('b', ['3', '4']), ('c', ['5', '6'])])
    all_paths = get_all_path_combinations(facets)
    
    expected_result = ['1/3/5', '1/3/6', '1/4/5', '1/4/6', '2/3/5', '2/3/6', '2/4/5', '2/4/6']
    assert(all_paths == expected_result)
