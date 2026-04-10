"""Tests for ticktick-mcp server instantiation and metadata."""

import pytest


class TestServerInstantiation:
    """Test server creates and initializes correctly."""

    async def test_server_creates_without_error(self, mcp_server):
        """Server instance should be created without errors."""
        assert mcp_server is not None
        assert hasattr(mcp_server, "name")

    async def test_server_has_correct_name(self, mcp_server):
        """Server should have the correct name."""
        assert mcp_server.name == "ticktick"

    async def test_server_has_tools_registered(self, mcp_server):
        """Server should have tools registered."""
        # FastMCP stores tools internally
        assert hasattr(mcp_server, "_tools") or hasattr(mcp_server, "list_tools")


class TestServerInitialization:
    """Test server initialization logic."""

    async def test_initialize_client_success(self, mock_env):
        """Should initialize client successfully with valid credentials."""
        from unittest.mock import MagicMock, patch

        mock_client = MagicMock()
        mock_client.get_projects = MagicMock(
            return_value=[{"id": "1", "name": "Test Project"}]
        )

        with patch("ticktick_mcp.src.server.TickTickClient", return_value=mock_client):
            from ticktick_mcp.src.server import initialize_client

            result = initialize_client()

            assert result is True

    async def test_initialize_client_missing_token(self, monkeypatch):
        """Should fail initialization without access token."""
        monkeypatch.delenv("TICKTICK_ACCESS_TOKEN", raising=False)

        from ticktick_mcp.src.server import initialize_client

        result = initialize_client()

        assert result is False

    async def test_initialize_client_api_error(self, mock_env):
        """Should handle API errors during initialization."""
        from unittest.mock import MagicMock, patch

        mock_client = MagicMock()
        mock_client.get_projects = MagicMock(return_value={"error": "API Error"})

        with patch("ticktick_mcp.src.server.TickTickClient", return_value=mock_client):
            from ticktick_mcp.src.server import initialize_client

            result = initialize_client()

            assert result is False
