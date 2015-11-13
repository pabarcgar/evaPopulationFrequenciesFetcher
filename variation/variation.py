import sys
from frequencies.populationFrequencies import PopulationFrequencies
from frequencies.attrVariationFrequencies import AttrVariationFrequencies
from frequencies.statVariationFrequencies import StatVariationFrequencies

__author__ = 'parce'


def add_1000g_population_frequencies(frequencies, attrs, output_tag, population_allele_frequency_tag):
    if population_allele_frequency_tag in attrs:
        alternate_allele_frequency = float(attrs[population_allele_frequency_tag])
        reference_allele_frequency = 1.0 - alternate_allele_frequency
        frequencies[output_tag + population_allele_frequency_tag] = PopulationFrequencies(reference_allele_frequency, alternate_allele_frequency)


class Variation:

    def __init__(self, variation):
        self.ids = variation['ids']
        self.chromosome = variation['chr']
        self.start = variation['start']
        self.end = variation['end']
        self.reference = variation['ref']
        self.alternate = variation['alt']
        self.files = variation['files']
        if 'st' in variation:
            self.stats = variation['st']
        else:
            self.stats = []
            sys.stderr.write('\nvariation ' + self.chromosome + ':' + str(self.start) + ' has no \'st\' field')
        self.frequencies = None
        self.variation_rs_ids = []
        self.get_rs_ids()

    def get_frequencies(self, counts_in_stats_projects, frequencies_in_attr_projects):
        if self.frequencies is None and len(self.variation_rs_ids) > 0:
            self.frequencies = StatVariationFrequencies(counts_in_stats_projects, self.stats)
            self.frequencies.add(AttrVariationFrequencies(frequencies_in_attr_projects, self.files))

    def get_rs_ids(self):
        for variation_id in self.ids:
            if variation_id != '' and variation_id[:2] == 'rs':
                self.variation_rs_ids.append(variation_id)

    def __str__(self):
        string_representation = []
        for variation_id in self.variation_rs_ids:
            string_representation.append('\t'.join([self.chromosome, str(self.start), str(self.end), self.reference, self.alternate, variation_id, str(self.frequencies)]))
        return '\n'.join(string_representation)
