"""
Unit tests for compliment generation.
"""

from __future__ import annotations

from typing import Dict, Union
from unittest.mock import patch

import pytest

from app.compliment import generate_compliment

FeatureMap = Dict[str, Union[float, bool]]


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
