"""Tests for ticktick-mcp tools."""

import pytest
from unittest.mock import patch, MagicMock


class TestGetProjects:
    """Test get_projects tool."""

    async def test_get_projects_success(self, mcp_server, mock_ticktick_client):
        """Should return list of projects."""
        with patch("ticktick_mcp.src.server.ticktick", mock_ticktick_client):
            from ticktick_mcp.src.server import get_projects

            result = await get_projects()

            assert "Found 2 projects" in result
            assert "Work" in result or "Personal" in result

    async def test_get_projects_empty(self, mcp_server):
        """Should handle empty project list."""
        mock_client = MagicMock()
        mock_client.get_projects = MagicMock(return_value=[])

        with patch("ticktick_mcp.src.server.ticktick", mock_client):
            from ticktick_mcp.src.server import get_projects

            result = await get_projects()

            assert "No projects found" in result

    async def test_get_projects_api_error(self, mcp_server, mock_ticktick_api_error):
        """Should handle API errors."""
        with patch("ticktick_mcp.src.server.ticktick", mock_ticktick_api_error):
            from ticktick_mcp.src.server import get_projects

            result = await get_projects()

            assert "Error" in result


class TestGetProject:
    """Test get_project tool."""

    async def test_get_project_success(self, mcp_server, sample_project):
        """Should return project details."""
        mock_client = MagicMock()
        mock_client.get_project = MagicMock(return_value=sample_project)

        with patch("ticktick_mcp.src.server.ticktick", mock_client):
            from ticktick_mcp.src.server import get_project

            result = await get_project("proj123")

            assert "Sample Project" in result
            mock_client.get_project.assert_called_once_with("proj123")

    async def test_get_project_not_found(self, mcp_server):
        """Should handle project not found."""
        mock_client = MagicMock()
        mock_client.get_project = MagicMock(return_value={"error": "Not found"})

        with patch("ticktick_mcp.src.server.ticktick", mock_client):
            from ticktick_mcp.src.server import get_project

            result = await get_project("invalid_id")

            assert "Error" in result


class TestGetProjectTasks:
    """Test get_project_tasks tool."""

    async def test_get_project_tasks_success(self, mcp_server, sample_task):
        """Should return tasks in project."""
        mock_client = MagicMock()
        mock_client.get_project_with_data = MagicMock(
            return_value={
                "project": {"name": "Test Project"},
                "tasks": [sample_task],
            }
        )

        with patch("ticktick_mcp.src.server.ticktick", mock_client):
            from ticktick_mcp.src.server import get_project_tasks

            result = await get_project_tasks("proj123")

            assert "Found 1 tasks" in result
            assert "Sample Task" in result

    async def test_get_project_tasks_empty(self, mcp_server):
        """Should handle project with no tasks."""
        mock_client = MagicMock()
        mock_client.get_project_with_data = MagicMock(
            return_value={"project": {"name": "Empty Project"}, "tasks": []}
        )

        with patch("ticktick_mcp.src.server.ticktick", mock_client):
            from ticktick_mcp.src.server import get_project_tasks

            result = await get_project_tasks("proj123")

            assert "No tasks found" in result


class TestGetTask:
    """Test get_task tool."""

    async def test_get_task_success(self, mcp_server, sample_task):
        """Should return task details."""
        mock_client = MagicMock()
        mock_client.get_task = MagicMock(return_value=sample_task)

        with patch("ticktick_mcp.src.server.ticktick", mock_client):
            from ticktick_mcp.src.server import get_task

            result = await get_task("proj123", "task123")

            assert "Sample Task" in result
            mock_client.get_task.assert_called_once_with("proj123", "task123")

    async def test_get_task_not_found(self, mcp_server):
        """Should handle task not found."""
        mock_client = MagicMock()
        mock_client.get_task = MagicMock(return_value={"error": "Not found"})

        with patch("ticktick_mcp.src.server.ticktick", mock_client):
            from ticktick_mcp.src.server import get_task

            result = await get_task("proj123", "invalid_task")

            assert "Error" in result


class TestCreateTask:
    """Test create_task tool."""

    async def test_create_task_success(self, mcp_server, mock_ticktick_client):
        """Should create task successfully."""
        with patch("ticktick_mcp.src.server.ticktick", mock_ticktick_client):
            from ticktick_mcp.src.server import create_task

            result = await create_task(
                title="New Task",
                project_id="proj1",
                content="Task content",
                priority=3,
            )

            assert "created" in result.lower() or "New Task" in result
            mock_ticktick_client.create_task.assert_called_once()

    async def test_create_task_invalid_priority(self, mcp_server, mock_ticktick_client):
        """Should reject invalid priority."""
        with patch("ticktick_mcp.src.server.ticktick", mock_ticktick_client):
            from ticktick_mcp.src.server import create_task

            result = await create_task(title="Task", project_id="proj1", priority=10)

            assert "Invalid priority" in result

    async def test_create_task_with_dates(self, mcp_server, mock_ticktick_client):
        """Should create task with dates."""
        with patch("ticktick_mcp.src.server.ticktick", mock_ticktick_client):
            from ticktick_mcp.src.server import create_task

            result = await create_task(
                title="Task with dates",
                project_id="proj1",
                start_date="2024-01-01T00:00:00+0000",
                due_date="2024-01-31T00:00:00+0000",
            )

            assert "created" in result.lower() or "Task with dates" in result


class TestUpdateTask:
    """Test update_task tool."""

    async def test_update_task_success(self, mcp_server, mock_ticktick_client):
        """Should update task successfully."""
        with patch("ticktick_mcp.src.server.ticktick", mock_ticktick_client):
            from ticktick_mcp.src.server import update_task

            result = await update_task(
                project_id="proj1",
                task_id="task1",
                title="Updated Title",
            )

            assert "updated" in result.lower() or "Updated" in result
            mock_ticktick_client.update_task.assert_called_once()


class TestCompleteTask:
    """Test complete_task tool."""

    async def test_complete_task_success(self, mcp_server, mock_ticktick_client):
        """Should complete task successfully."""
        with patch("ticktick_mcp.src.server.ticktick", mock_ticktick_client):
            from ticktick_mcp.src.server import complete_task

            result = await complete_task(project_id="proj1", task_id="task1")

            assert "completed" in result.lower() or "✓" in result
            mock_ticktick_client.complete_task.assert_called_once_with("proj1", "task1")


class TestDeleteTask:
    """Test delete_task tool."""

    async def test_delete_task_success(self, mcp_server, mock_ticktick_client):
        """Should delete task successfully."""
        with patch("ticktick_mcp.src.server.ticktick", mock_ticktick_client):
            from ticktick_mcp.src.server import delete_task

            result = await delete_task(project_id="proj1", task_id="task1")

            assert "deleted" in result.lower() or "removed" in result.lower()
            mock_ticktick_client.delete_task.assert_called_once_with("proj1", "task1")


class TestFormatTask:
    """Test format_task helper function."""

    async def test_format_task_with_full_data(self, sample_task):
        """Should format task with all fields."""
        from ticktick_mcp.src.server import format_task

        result = format_task(sample_task)

        assert "task123" in result
        assert "Sample Task" in result
        assert "proj1" in result
        assert "Medium" in result  # priority 3
        assert "Subtask 1" in result
        assert "Subtask 2" in result

    async def test_format_task_minimal_data(self):
        """Should format task with minimal data."""
        from ticktick_mcp.src.server import format_task

        minimal_task = {"id": "task1", "title": "Minimal"}

        result = format_task(minimal_task)

        assert "task1" in result
        assert "Minimal" in result


class TestFormatProject:
    """Test format_project helper function."""

    async def test_format_project(self, sample_project):
        """Should format project data."""
        from ticktick_mcp.src.server import format_project

        result = format_project(sample_project)

        assert "proj123" in result
        assert "Sample Project" in result
        assert "#ff0000" in result
