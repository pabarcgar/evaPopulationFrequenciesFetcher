class VariationFrequencies:
    def __init__(self):
        self.population_frequencies = []

    def __str__(self):
        return ';'.join(str(freq) for freq in self.population_frequencies)

    def add(self, variation_frequencies):
        if variation_frequencies.population_frequencies is not None:
            self.population_frequencies = self.population_frequencies + variation_frequencies.population_frequencies