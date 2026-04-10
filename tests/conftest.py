"""Shared test fixtures for ticktick-mcp."""

import os
from typing import Any, Dict
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


@pytest.fixture
def mock_env(monkeypatch):
    """Mock environment variables for testing."""
    monkeypatch.setenv("TICKTICK_ACCESS_TOKEN", "test_access_token_123")
    monkeypatch.setenv("TICKTICK_USERNAME", "test_user")
    return {
        "TICKTICK_ACCESS_TOKEN": "test_access_token_123",
        "TICKTICK_USERNAME": "test_user",
    }


@pytest.fixture
def mock_ticktick_client():
    """Mock TickTickClient for API calls."""
    client = MagicMock()

    # Mock get_projects
    client.get_projects = MagicMock(
        return_value=[
            {"id": "proj1", "name": "Work", "color": "#ff0000"},
            {"id": "proj2", "name": "Personal", "color": "#00ff00"},
        ]
    )

    # Mock get_tasks
    client.get_tasks = MagicMock(
        return_value=[
            {
                "id": "task1",
                "title": "Test Task",
                "projectId": "proj1",
                "priority": 3,
                "status": 0,
                "content": "Task description",
            },
        ]
    )

    # Mock create_task
    client.create_task = MagicMock(
        return_value={
            "id": "new_task_1",
            "title": "New Task",
            "projectId": "proj1",
            "priority": 0,
            "status": 0,
        }
    )

    # Mock update_task
    client.update_task = MagicMock(
        return_value={
            "id": "task1",
            "title": "Updated Task",
            "projectId": "proj1",
            "status": 0,
        }
    )

    # Mock complete_task
    client.complete_task = MagicMock(
        return_value={"id": "task1", "title": "Test Task", "status": 2}
    )

    # Mock delete_task
    client.delete_task = MagicMock(return_value={"success": True})

    return client


@pytest.fixture
def mock_ticktick_api_error():
    """Mock TickTickClient that returns API errors."""
    client = MagicMock()

    client.get_projects = MagicMock(return_value={"error": "API Error: Unauthorized"})
    client.get_tasks = MagicMock(return_value={"error": "API Error: Not found"})
    client.create_task = MagicMock(return_value={"error": "API Error: Invalid request"})

    return client


@pytest.fixture
async def mcp_server(mock_env):
    """Create a test FastMCP server instance."""
    # Mock the client initialization
    with patch("ticktick_mcp.src.server.initialize_client", return_value=True):
        from ticktick_mcp.src.server import mcp

        return mcp


@pytest.fixture
def sample_task() -> Dict[str, Any]:
    """Sample task data for testing."""
    return {
        "id": "task123",
        "title": "Sample Task",
        "projectId": "proj1",
        "priority": 3,
        "status": 0,
        "content": "This is a sample task",
        "startDate": "2024-01-01T00:00:00.000+0000",
        "dueDate": "2024-01-31T00:00:00.000+0000",
        "items": [
            {"title": "Subtask 1", "status": 1},
            {"title": "Subtask 2", "status": 0},
        ],
    }


@pytest.fixture
def sample_project() -> Dict[str, Any]:
    """Sample project data for testing."""
    return {
        "id": "proj123",
        "name": "Sample Project",
        "color": "#ff0000",
        "viewMode": "list",
    }
