#!/usr/bin/env python3
"""TestAccessNestedMap"""

import unittest
from parameterized import parameterized
from utils import access_nested_map, nested_map_exception


class TestAccessNestedMap(unittest.TestCase):
    """ inherits from unittest.TestCase"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """ test that the method returns what it is supposed to"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_message):
        """test_access_nested_map_exception"""

        with self.assertRaises(Exception):
            access_nested_map(nested_map, path)


if __name__ == '__main__':
    unittest.main()
