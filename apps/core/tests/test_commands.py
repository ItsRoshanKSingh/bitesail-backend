from unittest.mock import patch
from django.core.management import call_command
from django.db.utils import OperationalError
from psycopg import OperationalError as PsycopgError
from django.test import SimpleTestCase


class CommandTests(SimpleTestCase):
    """
    Test suite for the `wait_for_db` management command.

    This class includes tests for verifying the behavior of the `wait_for_db` command,
    which is designed to wait until the database is available. The tests simulate
    various scenarios, including the database being immediately available and
    the database becoming available after a delay.
    """

    @patch("apps.core.management.commands.wait_for_db.Command.check")
    def test_wait_for_db_ready(self, mock_check):
        """
        Test the `wait_for_db` command when the database is ready.

        This test simulates the scenario where the database is immediately available.
        It verifies that the `check` method is called once and the command completes
        without further retries.
        """
        mock_check.return_value = True  # Simulate the database being ready

        call_command("wait_for_db")

        mock_check.assert_called_once_with(databases=["default"])

    @patch("apps.core.management.commands.wait_for_db.Command.check")
    @patch("time.sleep")  # Mock sleep to avoid actual delays during testing
    def test_wait_for_db_delay(self, mock_sleep, mock_check):
        """
        Test the `wait_for_db` command when the database is initially unavailable and then becomes ready.

        This test simulates the scenario where the database is unavailable initially,
        but becomes available after several retries. It verifies that the `check` method
        is called multiple times and that the command waits between retries.
        """
        mock_check.side_effect = [PsycopgError] * 2 + [OperationalError] * 3 + [True]

        call_command("wait_for_db")

        self.assertEqual(mock_check.call_count, 6)  # Ensure `check` was called 6 times

        mock_check.assert_called_with(
            databases=["default"]
        )  # Ensure the last call had the correct arguments
        mock_sleep.assert_called_with(
            1
        )  # Ensure `sleep` was called with a 1-second delay during retries
