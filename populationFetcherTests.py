from EvaMongoAdaptor import EvaMongoAdaptor
from project.espProject import EspProject
from project.exacProject import ExacProject
from project.project import Project
from project.thousandGenomesPhase1Project import ThousandGenomesPhase1Project
from project.thousandGenomesPhase3Project import ThousandGenomesPhase3Project
from variation.frequencies.statVariationFrequencies import StatVariationFrequencies

__author__ = 'parce'

import unittest


class PopulationFetcherTest(unittest.TestCase):

    def test_g1k_phase3_single_allele_variants(self):
        eva_adaptor = EvaMongoAdaptor('database.config')
        for variation in eva_adaptor.find_variation_by_id("rs4974648"):
            print variation.get_allele_frequencies_string()

    def test_one_variant(self):
        eva_adaptor = EvaMongoAdaptor('database.config')
        EXAC_PROJECT_ID = '130'
        THOUSAND_GENOMES_PHASE_1_PROJECT_ID = '8616'
        THOUSAND_GENOMES_PHASE_3_PROJECT_ID = '301'
        ESP_PROJECT_ID = '2'
        exac_project = ExacProject()
        esp_project = EspProject()
        thousand_genomes_phase1_project = ThousandGenomesPhase1Project() # TODO: phase 1 superpopulations
        thousand_genomes_phase3_project = ThousandGenomesPhase3Project()
        projects = [exac_project, esp_project, thousand_genomes_phase1_project, thousand_genomes_phase3_project]
        for variation in eva_adaptor.find_variations([EXAC_PROJECT_ID, THOUSAND_GENOMES_PHASE_1_PROJECT_ID, THOUSAND_GENOMES_PHASE_3_PROJECT_ID, ESP_PROJECT_ID], '9'):
            freq = StatVariationFrequencies(projects, variation['st'])
            print freq

if __name__ == '__main__':
    unittest.main()
