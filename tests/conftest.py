import pytest
from flask import Flask


@pytest.fixture()
def app():
    from tests.repo.server import app
    # app = Flask('app')
    return app
