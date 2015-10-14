class VariationFrequencies:
    def __init__(self):
        self.population_frequencies = []

    def __str__(self):
        return ';'.join(str(freq) for freq in self.population_frequencies)

    def add(self, variation_frequencies):
        self.population_frequencies.append(variation_frequencies.population_frequencies)