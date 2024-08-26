#!/usr/bin/env python3
"""TestGithubOrgClient"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """class"""

    @parameterized.expand([
        ("google", {"repos_url": "https://api.github.com/orgs/google/repos"}),
        ("abc", {"repos_url": "https://api.github.com/orgs/abc/repos"}),
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str, expected: dict, mock_get_json: Mock) -> None:
        """test_org"""

        mock_get_json.return_value = expected

        client = GithubOrgClient(org_name)

        result = client.org()

        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

        self.assertEqual(result, expected)

    @patch('client.GithubOrgClient.org')
    def test_public_repos_url(self, mock_org: Mock) -> None:
        """test_public_repos_url"""

        mock_org.return_value = {
            "repos_url": "https://api.github.com/orgs/test_org/repos"
        }

        client = GithubOrgClient("test_org")

        result = client._public_repos_url

        expected_url = "https://api.github.com/orgs/test_org/repos"
        self.assertEqual(result, expected_url)

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json: Mock) -> None:
        """test_public_repos"""

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

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo: dict, license_key: str, expected: bool) -> None:
        """Test the `has_license` method"""
        self.assertEqual(GithubOrgClient.has_license(
            repo, license_key), expected)


class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Set up the patcher for requests.get"""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        # Define what each URL should return
        def mock_get_side_effect(url, *args, **kwargs):
            if 'orgs/google' in url:
                return Mock(json=lambda: org_payload)
            elif 'orgs/google/repos' in url:
                return Mock(json=lambda: repos_payload)
            return Mock(json=lambda: {})

        cls.mock_get.side_effect = mock_get_side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns the expected repositories"""
        client = GithubOrgClient('google')
        self.assertEqual(client.public_repos(), expected_repos)


if __name__ == '__main__':
    unittest.main()
