#!/usr/bin/env python3
"""TestGithubOrgClient"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):

    @parameterized.expand([
        ("google", {"repos_url": "https://api.github.com/orgs/google/repos"}),
        ("abc", {"repos_url": "https://api.github.com/orgs/abc/repos"}),
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str, expected: dict, mock_get_json: Mock) -> None:
        mock_get_json.return_value = expected

        client = GithubOrgClient(org_name)

        result = client.org()

        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

        self.assertEqual(result, expected)

    @patch('client.GithubOrgClient.org')
    def test_public_repos_url(self, mock_org: Mock) -> None:
        mock_org.return_value = {
            "repos_url": "https://api.github.com/orgs/test_org/repos"
        }

        client = GithubOrgClient("test_org")

        result = client._public_repos_url

        expected_url = "https://api.github.com/orgs/test_org/repos"
        self.assertEqual(result, expected_url)

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json: Mock) -> None:
        mock_get_json.return_value = [
            {"name": "repo1", "license": {"key": "MIT"}},
            {"name": "repo2", "license": {"key": "Apache-2.0"}},
        ]

        with patch.object(
                GithubOrgClient,
                '_public_repos_url',
                return_value="https://api.github.com/orgs/test_org/repos") as mock_public_repos_url:

            client = GithubOrgClient("test_org")
            repos = client.public_repos()

            expected_repos = ["repo1", "repo2"]
            self.assertEqual(repos, expected_repos)

            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/test_org/repos")
            mock_public_repos_url.assert_called_once()


if __name__ == '__main__':
    unittest.main()
