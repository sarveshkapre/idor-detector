import re

from idor_detector.idor_techniques import IDORTechnique


class SequenceBasedTechnique(IDORTechnique):
    """
    This plugin will look for numeric IDs in the URLs and create a new URL by adding or subtracting a specified value (default is 1) from the ID. 
    It returns a list of tuples containing the original URL and the new URL.
    """

    def __init__(self, delta=1):
        self.delta = delta

    def detect(self, links):
        idor_candidates = []

        for link in links:
            link_parts = re.split(r'(\d+)', link)
            for i, part in enumerate(link_parts):
                if part.isdigit():
                    new_part = str(int(part) + self.delta)
                    new_link = "".join(
                        link_parts[:i] + [new_part] + link_parts[i + 1:])
                    idor_candidates.append((link, new_link))

        return idor_candidates

    @property
    def name(self):
        return "sequence_based"
