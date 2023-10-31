"""
Django command to wait for the database to be available.
"""
from psycopg2 import OperationalError as Psycopg2Error

from django.core.management.base import BaseCommand
import time
from django.db.utils import OperationalError

class Command(BaseCommand):
    """ Django command to wait for database."""

    def handle(self, *args, **options):
        pass