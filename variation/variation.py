import json
import sys
from frequencies.populationFrequencies import PopulationFrequencies
from frequencies.attrVariationFrequencies import AttrVariationFrequencies
from frequencies.statVariationFrequencies import StatVariationFrequencies

__author__ = 'parce'


class Variation:

    def __init__(self, variation):
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

    def get_frequencies(self, counts_in_stats_projects, frequencies_in_attr_projects):
        # TODO: why self.frequencies needs to be None?
        if self.frequencies is None:
            self.frequencies = StatVariationFrequencies(self, counts_in_stats_projects, self.stats)
            self.frequencies.add(AttrVariationFrequencies(self, frequencies_in_attr_projects, self.files))

    def __str__(self):
        return self.to_json_string()

    def tab_separated_string(self):
        return '\t'.join([self.chromosome, str(self.start), str(self.end), self.reference, self.alternate,
                          str(self.frequencies)])

    def filter_invalid_frequencies(self):
        self.frequencies.filter_invalid_frequencies()

    def to_json_string(self):
        dict = {'chromosome': self.chromosome, 'start': self.start, 'end': self.end, 'reference': self.reference,
                'alternate': self.alternate, 'annotation': {'populationFrequencies': self.frequencies.to_json_array()}}
        return json.dumps(dict)
