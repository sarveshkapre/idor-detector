import re
from abc import ABC, abstractmethod

from .constants import EXTERNAL_IDOR_PATTERNS


class IDORTechnique(ABC):
    @abstractmethod
    def detect(self, links):
        pass

    @property
    @abstractmethod
    def name(self):
        pass


class PatternBasedTechnique(IDORTechnique):
    def __init__(self, patterns=None):
        self.patterns = patterns or EXTERNAL_IDOR_PATTERNS

    def detect(self, links):
        idor_candidates = []

        for link in links:
            for pattern in self.patterns:
                if re.search(pattern, link):
                    idor_candidates.append(link)
                    break

        return idor_candidates

    @property
    def name(self):
        return "pattern_based"


class MachineLearningBasedTechnique(IDORTechnique):
    def __init__(self, model):
        self.model = model

    def detect(self, links):
        idor_candidates = []

        for link in links:
            prediction = self.model.predict(link)
            if prediction == 1:
                idor_candidates.append(link)

        return idor_candidates

    @property
    def name(self):
        return "pattern_based"
