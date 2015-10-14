import sys
from EvaMongoAdaptor import EvaMongoAdaptor
from project.espProject import EspProject
from project.exacProject import ExacProject
from project.thousandGenomesPhase1Project import ThousandGenomesPhase1Project
from project.thousandGenomesPhase3Project import ThousandGenomesPhase3Project
from variation.frequencies.statVariationFrequencies import StatVariationFrequencies

exac_project = ExacProject()
esp_project = EspProject()
thousand_genomes_phase1_project = ThousandGenomesPhase1Project() # TODO: phase 1 superpopulations
thousand_genomes_phase3_project = ThousandGenomesPhase3Project()
projects = [exac_project, esp_project, thousand_genomes_phase1_project, thousand_genomes_phase3_project]
project_ids = [project.id for project in projects]

total = 0
chr = sys.argv[1]
sys.stderr.write('Extracting frequencies from chromosome ' + chr + ' ...')
eva_adaptor = EvaMongoAdaptor('database.config')
for variation in eva_adaptor.find_variations(project_ids, chr):
    frequencies = StatVariationFrequencies(projects, variation['st'])
    for variation_id in variation['ids']:
        if variation_id != '':
            print '\t'.join([variation['chromosome'], variation['start'], variation['end'], variation_id, frequencies])

