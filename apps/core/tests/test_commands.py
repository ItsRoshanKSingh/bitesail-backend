from unittest.mock import patch
from django.core.management import call_command
from django.db.utils import OperationalError
from psycopg import OperationalError as PsycopgError
from django.test import SimpleTestCase


class CommandTests(SimpleTestCase):
    """Test the management command."""

    @patch("apps.core.management.commands.wait_for_db.Command.check")
    def test_wait_for_db_ready(self, mock_check):
        """
        Test wait_for_db command when the database is ready.

        The command should execute the `check` method once and continue when
        the database connection is available.
        """
        mock_check.return_value = True  # Simulate database being ready

        call_command("wait_for_db")

        mock_check.assert_called_once_with(databases=["default"])

    @patch("apps.core.management.commands.wait_for_db.Command.check")
    @patch("time.sleep")  # Mock sleep to avoid delays in testing
    def test_wait_for_db_delay(self, mock_sleep, mock_check):
        """
        Test wait_for_db when the database is initially unavailable and becomes ready.

        Simulate the database being unavailable, then becoming available after retries.
        """
        mock_check.side_effect = [PsycopgError] * 2 + [OperationalError] * 3 + [True]

        call_command("wait_for_db")

        self.assertEqual(mock_check.call_count, 6)  # Ensure check was called 6 times

        mock_check.assert_called_with(
            databases=["default"]
        )  # Ensure the last call was with the correct args
        mock_sleep.assert_called_with(1)  # Ensure the sleep was called during retries
