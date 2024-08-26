#!/usr/bin/env python3
"""TestAccessNestedMap"""

import unittest
from parameterized import parameterized
from typing import Dict, Tuple, Type, Any
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for access_nested_map function"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: Dict[str, Any], path: Tuple[str], expected: Any) -> None:
        """Test that the method returns what it is supposed to"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
    ])
    def test_access_nested_map_exception(self, nested_map: Dict[str, Any], path: Tuple[str], exception: Type[Exception]) -> None:
        """Test that access_nested_map raises the expected exception"""
        with self.assertRaises(exception):
            access_nested_map(nested_map, path)


if __name__ == '__main__':
    unittest.main()
