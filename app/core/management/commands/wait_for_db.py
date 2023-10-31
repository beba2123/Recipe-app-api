"""
Django command to wait for the database to be available.
"""
from psycopg2 import OperationalError as Psycopg20pError

from django.core.management.base import BaseCommand
import time
from django.db.utils import OperationalError

class Command(BaseCommand):
    """ Django command to wait for database."""

    def handle(self, *args, **options):
        """Entrypoint for command"""
        self.stdout.write('Waiting for database...') 
        db_up = False
        while db_up is False:
            try:
                self.check(databases = ['default'])
                db_up=True
            except(Psycopg20pError, OperationalError):
                self.stdout.write('Database not available, wait a second..')
                time.sleep(1)
        
        self.stdout.write(self.style.SUCCESS('Databases Available!!'))
        