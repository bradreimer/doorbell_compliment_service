"""
Unit tests for compliment generation and endpoint.
"""

from __future__ import annotations

from io import BytesIO
from typing import Dict, Union
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from PIL import Image

from app.compliment import generate_compliment
from app.main import app

FeatureMap = Dict[str, Union[float, bool]]

client = TestClient(app)


@pytest.fixture(name="base_features")
def fixture_base_features() -> FeatureMap:
    """
    Provide a baseline feature map for tests.
    """
    return {
        "energy": 110.0,
        "brightness": 150.0,
        "colorfulness": 80.0,
        "has_face": True,
        "centered": True,
    }


def test_generate_compliment_returns_string(base_features: FeatureMap) -> None:
    """
    Ensure a compliment string is always returned.
    """
    result = generate_compliment(base_features)

    assert isinstance(result, str)
    assert result


@patch("app.compliment.random.choice", autospec=True)
def test_generate_compliment_is_deterministic(
    mock_choice, base_features: FeatureMap
) -> None:
    """
    Ensure compliment selection behaves predictably when randomness is controlled.
    """
    mock_choice.side_effect = lambda choices: choices[0]

    result = generate_compliment(base_features)

    assert "expression" in result or "friendly" in result
    assert "Thanks" in result or "Hope" in result


def test_generate_compliment_without_face() -> None:
    """
    Verify behavior when no face is detected.
    """
    features: FeatureMap = {
        "energy": 90.0,
        "brightness": 100.0,
        "colorfulness": 40.0,
        "has_face": False,
        "centered": False,
    }

    result = generate_compliment(features)

    assert isinstance(result, str)
    assert "presence" in result or "energy" in result


# ---- Endpoint Tests --------------------------------------------------------


def create_test_image() -> bytes:
    """Create a simple test image as bytes."""
    img = Image.new("RGB", (224, 224), color=(73, 109, 137))
    img_bytes = BytesIO()
    img.save(img_bytes, format="JPEG")
    img_bytes.seek(0)
    return img_bytes.getvalue()


@patch("app.main.urllib.request.urlopen")
@patch("app.main.extract_features")
@patch("app.main.generate_compliment")
def test_doorbell_endpoint_success(
    mock_generate, mock_extract, mock_urlopen
) -> None:
    """
    Test successful doorbell endpoint request with image URL.
    """
    # Setup mocks
    mock_response = MagicMock()
    mock_response.read.return_value = create_test_image()
    mock_urlopen.return_value.__enter__.return_value = mock_response

    mock_extract.return_value = {
        "energy": 110.0,
        "brightness": 150.0,
        "colorfulness": 80.0,
        "has_face": True,
        "centered": True,
    }
    mock_generate.return_value = "You look great today!"

    # Make request
    response = client.post(
        "/doorbell",
        json={"image_url": "http://example.com/test.jpg"},
    )

    # Assertions
    assert response.status_code == 200
    assert response.json() == {"compliment": "You look great today!"}
    mock_urlopen.assert_called_once()
    mock_extract.assert_called_once()
    mock_generate.assert_called_once()


@patch("app.main.urllib.request.urlopen")
def test_doorbell_endpoint_invalid_image(mock_urlopen) -> None:
    """
    Test doorbell endpoint with invalid image data.
    """
    # Setup mock to return invalid image data
    mock_response = MagicMock()
    mock_response.read.return_value = b"not_an_image"
    mock_urlopen.return_value.__enter__.return_value = mock_response

    # Make request
    response = client.post(
        "/doorbell",
        json={"image_url": "http://example.com/test.jpg"},
    )

    # Assertions
    assert response.status_code == 400
    assert "Invalid image file" in response.json()["detail"]


@patch("app.main.urllib.request.urlopen")
def test_doorbell_endpoint_download_failure(mock_urlopen) -> None:
    """
    Test doorbell endpoint when image download fails.
    """
    # Setup mock to raise exception
    mock_urlopen.side_effect = Exception("Connection timeout")

    # Make request
    response = client.post(
        "/doorbell",
        json={"image_url": "http://example.com/nonexistent.jpg"},
    )

    # Assertions
    assert response.status_code == 400
    assert "Failed to download image" in response.json()["detail"]


def test_doorbell_endpoint_missing_image_url() -> None:
    """
    Test doorbell endpoint with missing image_url field.
    """
    # Make request with missing image_url
    response = client.post("/doorbell", json={})

    # Assertions
    assert response.status_code == 422  # Validation error
