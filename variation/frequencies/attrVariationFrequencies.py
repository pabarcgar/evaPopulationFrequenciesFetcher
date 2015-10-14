from variation.frequencies.populationFrequencies import PopulationFrequencies
from variation.frequencies.variationFrequencies import VariationFrequencies

__author__ = 'pagarcia'

class AttrVariationFrequencies(VariationFrequencies):
    def __init__(self, project_name, population_tags, attrs):
        VariationFrequencies.__init__(self)
        self.get_frequencies_from_attrs(project_name, population_tags, attrs)

    def get_frequencies_from_attrs(self, project_name, population_tags, attrs):
        for tag in population_tags:
            alternate_allele_frequency = float(attrs[tag])
            reference_allele_frequency = 1.0 - alternate_allele_frequency
            self.population_frequencies.append(PopulationFrequencies(project_name + '_' + tag, reference_allele_frequency, alternate_allele_frequency))

