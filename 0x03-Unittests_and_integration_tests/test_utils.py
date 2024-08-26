#!/usr/bin/env python3
"""TestAccessNestedMap"""

import unittest
from parameterized import parameterized
from typing import Dict, Tuple, Type, Any
from utils import access_nested_map, get_json, memoize
from unittest.mock import patch, Mock


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


class TestGetJson(unittest.TestCase):
    """class"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url: str, test_payload: Dict, mock_get: Mock) -> None:
        """Test that get_json returns the expected result and requests.get is called with the correct URL"""
        # Mock the response object with a json method returning the test_payload
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        # Call the function under test
        result = get_json(test_url)

        # Assert that get_json returns the expected payload
        self.assertEqual(result, test_payload)

        # Assert that requests.get was called exactly once with the test_url
        mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """Tests the `memoize` function."""

    def test_memoize(self) -> None:
        """Tests `memoize`'s caching behavior."""
        class TestClass:
            """testclass"""

            def a_method(self) -> int:
                """method"""
                return 42

            @memoize
            def a_property(self) -> int:
                """method"""
                return self.a_method()

        # Patch `a_method` to return a fixed value of 42
        with patch.object(TestClass, 'a_method', return_value=42) as mock_a_method:
            test_class = TestClass()
            # Call `a_property` twice
            self.assertEqual(test_class.a_property(), 42)
            self.assertEqual(test_class.a_property(), 42)

            # Assert that `a_method` was only called once
            mock_a_method.assert_called_once()


if __name__ == '__main__':
    unittest.main()
