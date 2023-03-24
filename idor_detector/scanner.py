import requests
from bs4 import BeautifulSoup
from tldextract import extract
from .constants import USER_AGENT

class Scanner:
    def __init__(self, api_endpoints):
        self.api_endpoints = api_endpoints

    def _extract_links(self, response):
        # Extract links from the response
        pass

    def _is_api_link(self, link):
        # Check if the link is an API link
        pass

    def _normalize_link(self, link):
        # Normalize the link
        pass

    def crawl(self):
        # Crawl the API endpoints and collect relevant information
        pass
