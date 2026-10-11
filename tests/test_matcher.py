import pytest

from app.matcher import extract_keywords, match


def test_perfect_match():
    result = match("Python SQL Git", "Python SQL Git")
    assert result["missing_keywords"] == []
    assert result["score"] > 90


def test_no_match():
    result = match("Cooking and gardening", "Python SQL Docker")
    assert result["matched_keywords"] == []
    assert result["score"] < 10


def test_missing_keywords_listed():
    result = match("Python SQL", "Python SQL Docker AWS")
    assert "docker" in result["missing_keywords"]
    assert "aws" in result["missing_keywords"]


def test_case_insensitive():
    assert extract_keywords("PYTHON and Docker") == {"python", "docker"}


def test_aliases_map_to_canonical():
    assert extract_keywords("Experienced in JS and Postgres") == {
        "javascript",
        "postgresql",
    }


def test_no_partial_word_match():
    assert extract_keywords("I know javascript") == {"javascript"}


def test_empty_input_raises():
    with pytest.raises(ValueError):
        match("", "Python")
