class VariationFrequencies:
    def __init__(self):
        self.populationFrequencies = []

    def __str__(self):
        return ';'.join(str(freq) for freq in self.populationFrequencies)
