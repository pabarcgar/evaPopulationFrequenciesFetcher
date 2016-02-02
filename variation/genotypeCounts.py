__author__ = 'parce'


class GenotypeCounts:
    def __init__(self, study, reference, alternate, total):
        self.study = study
        self.total = total
        self.alternate = alternate
        self.reference = reference

    def add(self, reference, alternate, total):
        self.total += total
        self.reference += reference
        self.alternate += alternate
