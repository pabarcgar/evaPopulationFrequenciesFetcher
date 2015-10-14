__author__ = 'parce'


class PopulationFrequencies:

    def __init__(self, population, reference_frequency, alternate_frequency):
        self.population = population
        self.reference_frequency = reference_frequency
        self.alternate_frequency = alternate_frequency

    def __str__(self):
        return self.population + '_AF:' + self.format_frequency(self.reference_frequency) + ',' + self.format_frequency(self.alternate_frequency)

    @staticmethod
    def format_frequency(frequency):
        return "{:.5f}".format(frequency)
