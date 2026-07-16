from pathlib import Path

import pytest
from django.db import connection

SCHEMA_SQL = Path(__file__).resolve().parent / 'db' / 'sports_calendar.sql'


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    # events/models.py uses managed=False, so Django's normal test-DB migration
    # never creates these tables. Load the real schema (+ seed data) instead.
    with django_db_blocker.unblock():
        with connection.cursor() as cursor:
            cursor.execute(SCHEMA_SQL.read_text())
