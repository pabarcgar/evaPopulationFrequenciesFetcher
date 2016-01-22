class VariationFrequencies:
    def __init__(self, variation):
        self.population_frequencies_list = []
        self.variation = variation

    def __str__(self):
        return ';'.join(str(freq) for freq in self.population_frequencies_list if freq.is_not_zero())

    def add(self, variation_frequencies):
        if variation_frequencies.population_frequencies_list is not None:
            self.population_frequencies_list = self.population_frequencies_list + variation_frequencies.population_frequencies_list

    def is_empty(self):
        return len(self.population_frequencies_list) == 0

    def to_json_array(self):
        return [f.to_dict() for f in self.population_frequencies_list]
