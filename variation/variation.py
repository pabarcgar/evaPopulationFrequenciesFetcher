import sys
from frequencies.populationFrequencies import PopulationFrequencies

__author__ = 'parce'

ESP_6500_PROJECT_ID = 'PRJEB5439'
G1K_PHASE1_PROJECT_ID = 'PRJEB4019'
G1K_PHASE3_PROJECT_ID = 'PRJEB6930'
EXAC_PROJECT_ID = 'PRJEB8661'

POPULATION_TAGS_IN_1000G_PHASE1 = ['AFR', 'AMR', 'ASN', 'EUR']
POPULATION_TAGS_IN_1000G_PHASE3 = ['AFR', 'AMR', 'EAS', 'EUR', 'SAS']

SUPER_POPULATIONS_G1k_PHASE3 = {'ACB': 'AFR',
                                'ASW': 'AFR',
                                'ESN': 'AFR',
                                'LWK': 'AFR',
                                'MAG': 'AFR',
                                'GWD': 'AFR',
                                'MSL': 'AFR',
                                'YRI': 'AFR',
                                'CLM': 'AMR',
                                'MXL': 'AMR',
                                'PEL': 'AMR',
                                'PUR': 'AMR',
                                'CDX': 'EAS',
                                'CHB': 'EAS',
                                'CHD': 'EAS',
                                'CHS': 'EAS',
                                'JPT': 'EAS',
                                'KHV': 'EAS',
                                'CEU': 'EUR',
                                'FIN': 'EUR',
                                'GBR': 'EUR',
                                'IBS': 'EUR',
                                'TSI': 'EUR',
                                'BEB': 'SAS',
                                'GIH': 'SAS',
                                'ITU': 'SAS',
                                'PJL': 'SAS',
                                'STU': 'SAS',
                                'ALL': 'ALL'
                                }


def add_1000g_population_frequencies(frequencies, attrs, output_tag, population_allele_frequency_tag):
    if population_allele_frequency_tag in attrs:
        alternate_allele_frequency = float(attrs[population_allele_frequency_tag])
        reference_allele_frequency = 1.0 - alternate_allele_frequency
        frequencies[output_tag + population_allele_frequency_tag] = PopulationFrequencies(reference_allele_frequency, alternate_allele_frequency)
        # frequencies.append(output_tag + population_allele_frequency_tag + ':' + str(reference_allele_frequency) + ',' + str(alternate_allele_frequency))


class Variation:

    def __init__(self, variation):
        self.ids = variation['ids']
        self.chromosome = variation['chr']
        self.start = variation['start']
        self.end = variation['end']
        self.files = variation['files']
        self.stats = variation['st']
        self.population_frequencies = {}
        self.get_allele_frequencies()

    def get_allele_frequencies(self):
        for project in self.files:
            if project['sid'] == ESP_6500_PROJECT_ID:
                self.get_allele_frequencies_for_esp(project['attrs'])
            elif project['sid'] == G1K_PHASE1_PROJECT_ID:
                self.get_allele_frequencies_for_1000g(project['attrs'], '1', POPULATION_TAGS_IN_1000G_PHASE1)
            elif project['sid'] == G1K_PHASE3_PROJECT_ID:
                try:
                    self.get_allele_frequencies_from_stats_for_g1k_phase3(self.stats, self.ids)
                except KeyError as ex:
                    sys.stderr.write('\nKey error in variant ' + str(self.ids) + '. G1k Phase 3 stats not returned: ' + ex.message)
                # elif project['sid'] == EXAC_PROJECT_ID:
            #     variation_frequencies.append(get_allele_frequencies_for_exac(project['attrs']))
        #return ';'.join(variation_frequencies)

    def get_allele_frequencies_string(self):
        frequencies = []
        for frequency in self.population_frequencies:
            frequencies.append(frequency + '_AF:' + str(self.population_frequencies[frequency]))
        return ';'.join(frequencies)

    @staticmethod
    def get_allele_frequencies_for_esp_allele_counts(allele_counts):
        counts = allele_counts.split(',')
        alternate_count = float(counts[0])
        reference_count = float(counts[1])
        total = reference_count + alternate_count
        if total != 0:
            alternate_frequency = alternate_count / total
            reference_frequency = reference_count / total
            return PopulationFrequencies(reference_frequency, alternate_frequency)
        #     return self.format_frequency(reference_frequency) + ',' + self.format_frequency(alternate_frequency)
        # else:
        #     return ''

    def get_allele_frequencies_for_esp(self, attrs):
        # esp_frequencies = []

        ea_allele_frequencies = self.get_allele_frequencies_for_esp_allele_counts(attrs['EA_AC'])
        if ea_allele_frequencies is not None:
            self.population_frequencies['ESP_EA'] = ea_allele_frequencies
            # esp_frequencies.append('ESP_EA_AF:' + ea_allele_frequencies)
        aa_allele_frequencies = self.get_allele_frequencies_for_esp_allele_counts(attrs['AA_AC'])
        if aa_allele_frequencies is not None:
            self.population_frequencies['ESP_AA'] = aa_allele_frequencies
            # esp_frequencies.append('ESP_AA_AF:' + aa_allele_frequencies)
        # return ';'.join(esp_frequencies)

    def get_allele_frequencies_for_1000g(self, attrs, phase, population_tags):
        output_tag = '1000G_PHASE_' + phase + '_'
        g1k_frequencies = []
        for population_tag in population_tags:
            add_1000g_population_frequencies(g1k_frequencies, attrs, output_tag, population_tag)
        if len(g1k_frequencies) == 0:
            for population_tag in population_tags:
                self.population_frequencies[output_tag + population_tag] = PopulationFrequencies(1, 0)
                # g1k_frequencies.append(output_tag + population_tag + ':1.0,0.0')
        # TODO: this line is for ALL population?
        # add_1000g_population_frequencies(g1k_frequencies, attrs, output_tag, 'AF')
        # return ';'.join(g1k_frequencies)

    def get_allelecounts_from_gt_stats(self, genotype_counts):
        reference_count = 0
        alternate_count = 0
        total_count = 0
        for genotype in genotype_counts:
            genotype_count = genotype_counts[genotype]
            total_count += genotype_counts[genotype] * 2
            if genotype[0] == '0':
                reference_count += genotype_count
            elif genotype[0] == '1':
                alternate_count += genotype_count
            if genotype[2] == '0':
                reference_count += genotype_count
            elif genotype[2] == '1':
                alternate_count += genotype_count
        return reference_count, alternate_count, total_count

    def get_allele_frequencies_from_stats_for_g1k_phase3(self, stats, ids):
        super_populations_allele_counts = {}
        for stat in stats:
            population = stat['cid']
            # if population not in SUPER_POPULATIONS_G1k_PHASE3:
            #     print 'POPULATION QUE NO EXISTE: ' + population
            if stat['sid'] == G1K_PHASE3_PROJECT_ID and population in SUPER_POPULATIONS_G1k_PHASE3:
                ref_counts, alt_counts, total_counts = self.get_allelecounts_from_gt_stats(stat['numGt'])
                super_population = SUPER_POPULATIONS_G1k_PHASE3[population]
                if super_population in super_populations_allele_counts:
                    (acc_ref_counts, acc_alt_counts, acc_total_counts) = super_populations_allele_counts[super_population]
                    super_populations_allele_counts[super_population] = (ref_counts + acc_ref_counts, alt_counts + acc_alt_counts, total_counts + acc_total_counts)
                else:
                    super_populations_allele_counts[super_population] = (ref_counts, alt_counts, total_counts)
        frequencies = []
        for super_population in super_populations_allele_counts:
            super_population_allele_counts = super_populations_allele_counts[super_population]
            super_population_total_allele_count = super_population_allele_counts[0] + super_population_allele_counts[1]
            if super_population_total_allele_count != 0:
                super_population_ref_freq = float(super_population_allele_counts[0]) / super_population_total_allele_count
                super_population_alt_freq = float(super_population_allele_counts[1]) / super_population_total_allele_count
                self.population_frequencies['1000G_PHASE_3_' + super_population] = PopulationFrequencies(super_population_ref_freq, super_population_ref_freq)
                #frequencies.append('1000G_PHASE_3_' + super_population + '_AF:' + self.format_frequency(super_population_ref_freq) + ',' + self.format_frequency(super_population_alt_freq))
            else:
                sys.stderr.write('\nError: total allele count is 0 in super population ' + super_population + ' in variant ' + str(ids))
        # return ';'.join(frequencies)

    # @staticmethod
    # def format_frequency(frequency):
    #     return "{:.5f}".format(frequency)
