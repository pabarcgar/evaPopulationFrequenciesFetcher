__author__ = 'parce'


class GenotypeCounts:
    def __init__(self, study, reference, alternative, total):
        self.study = study
        self.total = total
        self.alternative = alternative
        self.reference = reference

    def add(self, reference, alternative, total):
        self.total += total
        self.reference += reference
        self.alternative += alternative
