import pytest
from flask import Flask, request
import mongomock
from flask_wtf.csrf import CSRFProtect
from blueprints.url_shortener import url_shortener
from blueprints.stats import stats


@pytest.fixture
def client():
    app = Flask(__name__, template_folder="../templates")
    app.config["SECRET_KEY"] = "test-secret-key"
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False  # Disable CSRF for tests

    # Initialize CSRF protection but disable for tests
    csrf = CSRFProtect(app)

    app.register_blueprint(url_shortener)
    app.register_blueprint(stats)

    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_db():
    # Create a mock database
    mock_db = mongomock.MongoClient().db
    return mock_db
