from variation.frequencies.populationFrequencies import PopulationFrequencies
from variation.frequencies.variationFrequencies import VariationFrequencies

__author__ = 'pagarcia'


class AttrVariationFrequencies(VariationFrequencies):
    def __init__(self, projects, files):
        VariationFrequencies.__init__(self)
        self.files = files
        for project in projects:
            self.attrs = self.get_attrs(project.id)
            if self.attrs is not None:
                self.get_frequencies_from_attrs(project.name, project.populations)

    def get_frequencies_from_attrs(self, project_name, population_tags):
        for tag in population_tags:
            freq_tag = tag + '_AF'
            if freq_tag in self.attrs:
                alternate_allele_frequency = float(self.attrs[freq_tag])
                reference_allele_frequency = 1.0 - alternate_allele_frequency
                self.population_frequencies_list.append(PopulationFrequencies(project_name + '_' + tag, reference_allele_frequency, alternate_allele_frequency))

    def get_attrs(self, project_id):
        for file in self.files:
            if file['sid'] == project_id:
                return file['attrs']

