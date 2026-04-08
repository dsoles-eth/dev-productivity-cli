import pytest
from unittest.mock import patch, MagicMock, mock_open, call
from datetime import datetime, timedelta
import json
import session_timer

# Fixtures

@pytest.fixture
def mock_time():
    """Fixes the current time to a static value for deterministic testing."""
    with patch('session_timer.datetime') as mock_dt:
        fixed_time = datetime(2023, 10, 27, 12, 0, 0)
        mock_dt.now.return_value = fixed_time
        mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw) if args else fixed_time
        yield mock_dt

@pytest.fixture
def mock_filesystem():
    """Mocks file system operations to prevent real I/O."""
    with patch('session_timer.open', mock_open()) as mock_open_func:
        mock_open_func.return_value.read.return_value = '{}'
        mock_open_func.return_value.__enter__ = lambda s: mock_open_func.return_value
        mock_open_func.return_value.__exit__ = lambda *args: None
        yield mock_open_func

@pytest.fixture
def mock_api_client():
    """Mocks the API client or requests to prevent network calls."""
    with patch('session_timer.requests') as mock_requests:
        mock_post = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'status': 'ok'}
        mock_post.return_value = mock_response
        mock_requests.post.return_value = mock_post
        yield mock_post

@pytest.fixture
def init_module_state():
    """Ensures module state is fresh before each test."""
    with patch.object(session_timer, '_session_log', {}, create=True):
        with patch.object(session_timer, '_state', {}, create=True):
            yield

# Tests for start_session

class TestStartSession:
    def test_start_session_creates_record(self, mock_time, init_module_state):
        """Happy path: starts a session and returns correct metadata."""
        result = session_timer.start_session("dev-001")
        assert result['session_id'] == "dev-001"
        assert result['status'] == 'active'
        assert 'start_time' in result
        assert result['paused_at'] is None

    def test_start_session_invalid_id_raises_error(self, init_module_state):
        """Error case: Invalid session ID format raises ValueError."""
        with pytest.raises(ValueError, match="Invalid session ID"):
            session_timer.start_session("")

    def test_start_session_overwrites_existing(self, mock_time, init_module_state, mock_filesystem):
        """Edge case: Overwriting an inactive session ID restores previous data."""
        # Simulate existing session in state
        init_module_state._state['dev-002'] = {'status': 'completed'}
        result = session_timer.start_session("dev-002")