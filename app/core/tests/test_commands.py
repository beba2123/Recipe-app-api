from unittest.mock import patch # used for isolate the code that are going to be tested
from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase

@patch('core.management.commands.wait_for_db.Command.check') #  like decorator calling the wait_for_db file, Command Class and check method.
class CommandTests(SimpleTestCase):
    """Test Commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default']) #called one time

    @patch('time.sleep') #becouse we don't have to check the database over and over again it has to have delay time.
    def test_wait_for_db_delay(self, patched_sleep, patched_check):

        """Test waiting for database delay time when getting Operational & psycopg2 Error."""
        patched_check.side_effect = [Psycopg2Error] * 2 + [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default']) # it has to be called multiple time.
