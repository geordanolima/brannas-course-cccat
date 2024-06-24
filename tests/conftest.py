import os
import sys
from pathlib import Path

import pytest

from curso_brannas.settings import Settings
from database import Database


def _set_pythonpath():
    sys.path.append(str(Path(__file__).parent))


def pytest_sessionstart(session):
    _set_pythonpath()
    return session
 

@pytest.fixture(autouse=True, scope="session")
def envvars(tmpdir_factory, session_mocker):
    settings = Settings()
    settings.DATABASE_NAME = "app_test"
    return settings

@pytest.fixture(scope="session")
def db_connection(envvars):
    settings = envvars
    db = Database(
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT,
        db_name=settings.DATABASE_NAME,
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASS,
    )
    db.db_query(get_migrate(file_name="drop_tables"))
    db.db_query(get_migrate(file_name="create_tables"))
    yield db
    db.db_query(get_migrate(file_name="drop_tables"))
    return db

@pytest.fixture(scope="session")
def db_clear(envvars):
    settings = envvars
    db = Database(
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT,
        db_name=settings.DATABASE_NAME,
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASS,
    )
    db.db_query(get_migrate(file_name="drop_tables"))

def get_migrate(file_name) -> str:
    sql = ""
    file = open(f"curso_brannas/src/migrations/{file_name}.sql")
    for line in file:
        sql = sql + " " + line
    return sql


@pytest.fixture
def db_session(db_connection):
    cursor = db_connection.conexao.cursor()
    yield cursor
    cursor.close()



