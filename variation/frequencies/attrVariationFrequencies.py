from variation.frequencies.populationFrequencies import PopulationFrequencies
from variation.frequencies.variationFrequencies import VariationFrequencies

__author__ = 'pagarcia'


class AttrVariationFrequencies(VariationFrequencies):
    def __init__(self, variation, projects, files):
        VariationFrequencies.__init__(self, variation)
        self.files = files
        for project in projects:
            self.attrs = self.get_attrs(project)
            if self.attrs is not None:
                self.get_frequencies_from_attrs(project.name, project, project.populations)

    def get_frequencies_from_attrs(self, project_name, project, populations):
        if populations is not None:
            for population_tag in populations:
                population_freq_tag = project.get_frequency_tag(population_tag)
                self.get_frequencies_from_AF_TAG(population_freq_tag, project_name, population_tag)
        else:
            self.get_frequencies_from_AF_TAG('AF', project_name, 'ALL')

    def get_frequencies_from_AF_TAG(self, freq_tag, project_name, population_tag):
        if freq_tag in self.attrs:
            alternate_allele_frequency = float(self.attrs[freq_tag])
            reference_allele_frequency = 1.0 - alternate_allele_frequency
            self.population_frequencies_list.append(PopulationFrequencies(project_name, population_tag,
                                                                          self.variation.reference,
                                                                          self.variation.alternate,
                                                                          reference_allele_frequency,
                                                                          alternate_allele_frequency))

    def get_attrs(self, project):
        for file in self.files:
            if file['sid'] == project.id or file['sid'] == project.prj_id:
                return file['attrs']

