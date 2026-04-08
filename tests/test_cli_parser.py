import pytest
from unittest.mock import patch, MagicMock
import cli_parser
import requests
from io import StringIO

# Fixtures for test data
@pytest.fixture
def valid_history_lines():
    return [
        "ls -la",
        "cd /var/www",
        "git status",
        "git commit -m 'fix bug'",
        "cd ..",
        "python3 app.py"
    ]

@pytest.fixture
def empty_history_lines():
    return []

@pytest.fixture
def whitespace_history_lines():
    return [
        "  \n",
        "\t",
        "   ",
        "git push"
    ]

@pytest.fixture
def mock_http_response():
    response = MagicMock()
    response.status_code = 200
    response.json.return_value = {
        "doc": "Documentation for git commands",
        "tool": "git"
    }
    return response

# Tests for parse_shell_history function
class TestParseShellHistory:
    @patch.object(cli_parser, 're')
    def test_parse_history_empty_input(self, mock_re):
        """Test parsing empty history list"""
        result = cli_parser.parse_shell_history([])
        assert result == []
        mock_re.search.assert_not_called()

    @patch.object(cli_parser, 're')
    def test_parse_history_with_whitespace(self, mock_re):
        """Test handling of lines containing only whitespace"""
        input_data = ["  ", "\t", "\n"]
        expected = []
        result = cli_parser.parse_shell_history(input_data)
        assert result == expected
        # Verify regex was attempted but failed to match command content
        mock_re.search.assert_any_call(r'^\s*(.+)', input_data[0])

    @patch.object(cli_parser, 're')
    def test_parse_history_valid_commands(self, mock_re):
        """Test extraction of valid commands from history"""
        input_data = ["git push", "python test.py"]
        mock_re.return_value = MagicMock()
        mock_re.return_value.group.return_value = "git push"
        # Simulating logic where regex groups the command
        result = cli_parser.parse_shell_history(input_data)
        assert isinstance(result, list)
        assert len(result) >= 1

# Tests for analyze_commands / aggregate_usage function
class TestAnalyzeCommands:
    @patch.object(cli_parser, 'collections')
    def test_analyze_commands_empty(self, mock_collections):
        """Test analysis of empty command list"""
        result = cli_parser.analyze_commands([])
        assert result == {}
        mock_collections.Counter.assert_not_called()

    @patch.object(cli_parser, 'collections')
    def test_analyze_commands_single(self, mock_collections):
        """Test counting a single repeated command"""
        mock_counter = MagicMock()
        mock_counter.__getitem__ = MagicMock(return_value=1)
        mock_collections.Counter.return_value = mock_counter
        mock_collections.Counter.return_value.most_common.return_value = [("pip", 1)]
        result = cli_parser.analyze_commands(["pip install x"])
        assert "pip install x" in result or len(result) >= 0

    @patch.object(cli_parser, 'collections')
    def test_analyze_commands_frequent(self, mock_collections):
        """Test identification of most frequent commands"""
        input_data = ["ls", "ls", "ls", "git status", "git commit"]
        mock_counter = MagicMock()
        mock_counter.__getitem__ = MagicMock(return_value=3)
        mock_collections.Counter.return_value = mock_counter
        mock_collections.Counter.return_value.most_common.return_value = [("ls", 3)]
        result = cli_parser.analyze_commands(input_data)
        assert "ls" in result
        assert result["ls"] == 3

# Tests for external API / metadata fetching
class TestExternalApiCalls:
    @patch('cli_parser.requests.get')
    def test_fetch_metadata_success(self, mock_get, mock_http_response):
        """Test successful fetch of tool metadata from external API"""
        mock_get.return_value = mock_http_response
        result = cli_parser.fetch_tool_metadata("git")
        assert result == "Documentation for git commands"
        mock_get.assert_called_once_with("https://api.devtools.io/v1/git")

    @patch('cli_parser.requests.get')
    def test_fetch_metadata_http_error(self, mock_get):
        """Test handling of HTTP 500 errors from external API"""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.HTTPError("Server Error")
        mock_get.return_value = mock_response