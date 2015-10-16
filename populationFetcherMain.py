import sys

from eva.evaMongoAdaptor import EvaMongoAdaptor
from project.espProject import EspProject
from project.exacProject import ExacProject
from project.thousandGenomesPhase1Project import ThousandGenomesPhase1Project
from project.thousandGenomesPhase3Project import ThousandGenomesPhase3Project
from variation.frequencies.attrVariationFrequencies import AttrVariationFrequencies
from variation.frequencies.statVariationFrequencies import StatVariationFrequencies

# projects to extract frequencies
exac_project = ExacProject()
esp_project = EspProject()
thousand_genomes_phase1_project = ThousandGenomesPhase1Project() # TODO: phase 1 superpopulations
thousand_genomes_phase3_project = ThousandGenomesPhase3Project()
counts_in_stats_projects = [exac_project, esp_project, thousand_genomes_phase3_project, thousand_genomes_phase1_project]
frequencies_in_attrs_projects = [thousand_genomes_phase1_project]
project_ids = [project.id for project in counts_in_stats_projects + frequencies_in_attrs_projects]

variations_processed, serialized_lines = 0, 0
chromosome = None
if len(sys.argv) > 1:
    chromosome = sys.argv[1]
sys.stderr.write('Connecting to EVA Mongo ...\n')
eva_adaptor = EvaMongoAdaptor('database.config')
if chromosome is not None:
    sys.stderr.write('Extracting frequencies from chromosome ' + chromosome + ' ...')
else:
    sys.stderr.write('Extracting all frequencies ...')
for variation in eva_adaptor.find_variations(project_ids, chromosome):
    variations_processed += 1

    # frequencies = StatVariationFrequencies(counts_in_stats_projects, variation['st'])
    # frequencies.add(AttrVariationFrequencies(thousand_genomes_phase1_project.id, thousand_genomes_phase1_project.name, thousand_genomes_phase1_project.population_tags, variation['files']))
    variation.get_frequencies(counts_in_stats_projects, frequencies_in_attrs_projects)
    if variation.frequencies is not None:
        print variation
sys.stderr.write('\nDone. ' + serialized_lines + ' lines serialized for ' + variations_processed + ' variations')
