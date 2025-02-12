import pytest
from unittest.mock import Mock, patch
from SonarqubeClient import SonarqubeClient
from Utilities import Utilities

# Test data
MOCK_BASE_URL = "http://localhost:9000"
MOCK_TOKEN = "mock_token"
MOCK_APP_IDS = ["test-project"]
MOCK_METRICS = ["coverage", "bugs"]

# Mock responses
MOCK_SEARCH_RESPONSE = {
    "components": [
        {
            "key": "test-project",
            "name": "Test Project"
        }
    ]
}

MOCK_MEASURES_RESPONSE = {
    "component": {
        "key": "test-project",
        "name": "Test Project",
        "measures": [
            {
                "metric": "coverage",
                "value": "80.0"
            },
            {
                "metric": "bugs",
                "value": "5"
            }
        ]
    }
}

@pytest.fixture
def sonarqube_client():
    return SonarqubeClient(MOCK_BASE_URL, MOCK_TOKEN)

def test_init():
    """Test client initialization"""
    client = SonarqubeClient(MOCK_BASE_URL, MOCK_TOKEN)
    assert client.base_url == MOCK_BASE_URL
    assert client.auth_token == MOCK_TOKEN

def test_token_to_base64():
    """Test token encoding"""
    encoded = Utilities.token_to_base64("test_token")
    assert isinstance(encoded, str)
    assert len(encoded) > 0

@patch('requests.get')
def test_get_sonarqube_metrics_success(mock_get, sonarqube_client):
    """Test successful metrics retrieval"""
    # Mock the API responses
    mock_get.side_effect = [
        Mock(
            status_code=200,
            json=lambda: MOCK_SEARCH_RESPONSE
        ),
        Mock(
            status_code=200,
            json=lambda: MOCK_MEASURES_RESPONSE
        )
    ]

    results = sonarqube_client.get_sonarqube_metrics(MOCK_APP_IDS, MOCK_METRICS)

    assert results
    assert MOCK_APP_IDS[0] in results
    project_metrics = results[MOCK_APP_IDS[0]]["Test Project"]
    assert "coverage" in project_metrics
    assert "bugs" in project_metrics
    assert project_metrics["coverage"] == "80.0"
    assert project_metrics["bugs"] == "5"

@patch('requests.get')
def test_get_sonarqube_metrics_empty_response(mock_get, sonarqube_client):
    """Test handling of empty response"""
    mock_get.return_value = Mock(
        status_code=200,
        json=lambda: {"components": []}
    )

    results = sonarqube_client.get_sonarqube_metrics(MOCK_APP_IDS, MOCK_METRICS)
    assert results[MOCK_APP_IDS[0]] == {}

@patch('requests.get')
def test_get_sonarqube_metrics_invalid_metrics(mock_get, sonarqube_client):
    """Test handling of invalid metrics"""
    mock_get.side_effect = [
        Mock(
            status_code=200,
            json=lambda: MOCK_SEARCH_RESPONSE
        ),
        Mock(
            status_code=200,
            json=lambda: {"component": {"measures": []}}
        )
    ]

    results = sonarqube_client.get_sonarqube_metrics(MOCK_APP_IDS, ["invalid_metric"])
    assert results[MOCK_APP_IDS[0]]["Test Project"] == {}

def test_invalid_base_url():
    """Test initialization with invalid URL"""
    with pytest.raises(ValueError):
        SonarqubeClient("", MOCK_TOKEN)

def test_invalid_token():
    """Test initialization with invalid token"""
    with pytest.raises(ValueError):
        SonarqubeClient(MOCK_BASE_URL, "")
