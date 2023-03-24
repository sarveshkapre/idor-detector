import importlib.util
import os
import re
import sys

import requests

from idor_detector.idor_techniques import PatternBasedTechnique

from .constants import EXTERNAL_IDOR_PATTERNS, HTTP_METHODS, USER_AGENT
from .idor_techniques import IDORTechnique


class IDORDetector:
    def __init__(self, scanner, techniques=None):
        self.scanner = scanner
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': USER_AGENT})
        self.techniques = techniques or [PatternBasedTechnique()]
        self.load_plugins()

    def load_plugins(self, plugin_dir="plugins"):
        sys.path.insert(0, os.path.abspath(plugin_dir))

        for file in os.listdir(plugin_dir):
            if file.endswith(".py"):
                module_name = file[:-3]
                spec = importlib.util.spec_from_file_location(
                    module_name, os.path.join(plugin_dir, file))
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type) and issubclass(attr, IDORTechnique) and attr is not IDORTechnique:
                        self.techniques.append(attr())

        sys.path.pop(0)

    def _identify_idor_patterns(self, links):
        idor_candidates = set()

        for technique in self.techniques:
            candidates = technique.detect(links)
            idor_candidates.update(candidates)

        return idor_candidates

    def _test_endpoint(self, endpoint, method):
        try:
            response = self.session.request(method, endpoint)
            if response.status_code == 200:
                return True
            elif response.status_code == 401:
                return False
            else:
                return None
        except requests.exceptions.RequestException:
            return None

    def _swap_parameters(self, url_tuple, idor_candidates):
        original_url, swapped_url = url_tuple

        for candidate in idor_candidates:
            match = re.search(candidate, original_url)
            if match:
                swapped_candidate = re.search(candidate, swapped_url)
                if swapped_candidate:
                    new_swapped_url = re.sub(swapped_candidate.group(
                        0), str(match.group(1)), swapped_url)
                    return (original_url, new_swapped_url)

        return None

    def _test_idor(self, original_url, swapped_url, method):
        original_response = self._test_endpoint(original_url, method)
        swapped_response = self._test_endpoint(swapped_url, method)

        if original_response is None or swapped_response is None:
            return None

        return original_response and not swapped_response

    def detect(self):
        links = self.scanner.crawl()
        idor_candidates = self._identify_idor_patterns(links)
        idor_issues = []

        for link in links:
            for method in HTTP_METHODS:
                swapped_url = self._swap_parameters(link, idor_candidates)
                if swapped_url:
                    is_idor = self._test_idor(link, swapped_url, method)
                    if is_idor is not None and is_idor:
                        idor_issues.append((link, method))

        return idor_issues
