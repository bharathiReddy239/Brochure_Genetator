from ai_brochure_generator.scraper import validate_url, discover_links  # noqa: I001
from bs4 import BeautifulSoup
import pytest


def test_vali_url():
    # Test valid URL
    result = validate_url("https://toscrape.com")
    assert result.scheme == "https"


def test_invalid_url():
    with pytest.raises(ValueError):
        validate_url("not-a-url")


def test_discover_links():
    html = """<html><body>
    <a href="https://toscrape.com/about">About</a>
    <a href="/contact">Contact</a>
    <a href="https://other.com/about">External</a>
    <a href="https://toscrape.com/logo.png">Logo</a>
    </body></html>"""
    soup = BeautifulSoup(html, "html.parser")
    links = discover_links("https://toscrape.com", soup)
    # assert "https://toscrape.com/page1" in links
    # assert "https://toscrape.com/page2" in links
    assert not any("other.com" in link for link in links)
    assert not any(link.endswith(".png") for link in links)
