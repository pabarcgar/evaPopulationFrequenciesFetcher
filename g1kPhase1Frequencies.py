__author__ = 'parce'

POPULATION_TAGS_IN_1000G_PHASE1 = ['AFR_AF', 'AMR_AF', 'ASN_AF', 'EUR_AF']


class G1kPhase1Frequencies:

    def __init__(self):
        pass

    def get_allele_frequencies_for_1000g(attrs, phase):
        output_tag = '1000G_PHASE_' + phase + '_'
        g1k_frequencies = []
        for population_tag in POPULATION_TAGS_IN_1000G_PHASE1:
            add_1000g_population_frequencies(g1k_frequencies, attrs, output_tag, population_tag)
        if len(g1k_frequencies) == 0:
            for population_tag in population_tags:
                g1k_frequencies.append(output_tag + population_tag + ':1.0,0.0')
        add_1000g_population_frequencies(g1k_frequencies, attrs, output_tag, 'AF')
        return ';'.join(g1k_frequencies)