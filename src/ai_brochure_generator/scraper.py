# from email.mime import text

import requests  # noqa: I001
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

HEADERS = {"User-Agent": "CompanyBrochureGenerator/1.0"}
KEYWORDS = [
    "brochure",
    "company",
    "product",
    "service",
    "solution",
    "career",
    "contact",
    "mission",
    "technology",
    "about",
    "portfolio",
    "catalog",
    "flyer",
    "leaflet",
]


def validate_url(url):
    """Validate a URL and return its parsed components."""
    parsed = urlparse(url)
    if parsed.scheme not in ["http", "https"]:
        raise ValueError("Only 'http' and 'https' are allowed.")
    if not parsed.hostname:
        raise ValueError("Invalid website URL.")
    return parsed


def is_allowed_by_robots(url):
    """Check whether the URL is allowed by the site's robots.txt file."""
    parsed = validate_url(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    try:
        response = requests.get(robots_url, headers=HEADERS, timeout=10)
        if response.status_code == 404:
            return True
        response.raise_for_status()

        parser = RobotFileParser()
        parser.set_url(robots_url)
        parser.parse(response.text.splitlines())
        return parser.can_fetch(HEADERS["User-Agent"], url)
    except requests.RequestException:
        return False


def get_page(url):
    if not is_allowed_by_robots(url):
        print(f"Skipping disallowed page: {url}")
        return None

    response = requests.get(url, headers=HEADERS, timeout=15, allow_redirects=True)
    response.raise_for_status()
    if len(response.content) > 2_000_000:
        raise ValueError("Page is too large to process.")
    if "text/html" not in response.headers.get("Content-Type", "").lower():
        return None
    return BeautifulSoup(response.content, "html.parser")


def discover_links(base_url, soup):
    base_domain = urlparse(base_url).netloc
    discovered = set()
    for link in soup.find_all("a", href=True):
        full_url = urljoin(base_url, link["href"])
        parsed_url = urlparse(full_url)
        if parsed_url.scheme not in ["http", "https"]:
            continue
        if parsed_url.netloc != base_domain:
            continue
        if parsed_url.path.lower().endswith(
            (
                ".jpg",
                ".jpeg",
                ".png",
                ".gif",
                ".pdf",
                ".doc",
                ".docx",
                ".xls",
                ".xlsx",
                ".zip",
            )
        ):
            continue

        text = link.get_text(strip=True).lower()
        url_text = parsed_url.path.lower()
        if any(word in text or word in url_text for word in KEYWORDS):
            discovered.add(full_url.split("#")[0].split("?")[0])
    return discovered


def extract_text(soup):
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
        tag.decompose()
    return soup.get_text(" ", strip=True)


def scrape_website(start_url, max_page=8):
    validate_url(start_url)
    start_url = start_url.rstrip("/")
    homepage = get_page(start_url)
    if homepage is None:
        raise ValueError("Could not read the homepage.")
    links_to_visit = discover_links(start_url, homepage)
    pages = {start_url: extract_text(homepage)}
    for link in sorted(links_to_visit)[: max_page - 1]:
        try:
            soup = get_page(link)
            if soup is None:
                continue
            text = extract_text(soup)
            if text:
                pages[link] = text
                print(f"Scraped {link} successfully.")
        except (requests.RequestException, ValueError) as error:
            print(f"Could not fetch {link}: {error}")

        return pages
