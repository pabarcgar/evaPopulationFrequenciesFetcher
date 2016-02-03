__author__ = 'parce'


class PopulationFrequencies:

    def __init__(self, study, population, reference_allele, alternate_allele, reference_frequency, alternate_frequency):
        self.study = study
        self.population = population
        self.reference_allele = reference_allele
        self.alternate_allele = alternate_allele
        self.reference_frequency = reference_frequency
        self.alternate_frequency = alternate_frequency

    def __str__(self):
        return self.population + '_AF:' + self.format_frequency(self.reference_frequency) + ',' + self.format_frequency(self.alternate_frequency)

    def is_not_zero(self):
        return self.alternate_frequency != 0 or self.reference_frequency != 0

    @staticmethod
    def format_frequency(frequency):
        return '{:.5f}'.format(frequency).rstrip('0').rstrip('.')

    def to_dict(self):
        return {"study": self.study, "population": self.population, "refAllele": self.reference_allele,
                "altAllele": self.alternate_allele, "refAlleleFreq": self.format_frequency(self.reference_frequency),
                "altAlleleFreq": self.format_frequency(self.alternate_frequency)}
