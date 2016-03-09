import sys

from eva.evaMongoAdaptor import EvaMongoAdaptor
from project.espProject import EspProject
from project.exacProject import ExacProject
from project.thousandGenomesPhase1Project import ThousandGenomesPhase1Project
from project.thousandGenomesPhase3Project import ThousandGenomesPhase3Project
from project.gonlProject import GonlProject
from project.uk10kAlspacProject import Uk10kAlspacProject
from project.uk10kTwinsUKProject import Uk10kTwinsUKProject

# projects to extract frequencies
exac_project = ExacProject()
esp_project = EspProject()
thousand_genomes_phase1_project = ThousandGenomesPhase1Project()
thousand_genomes_phase3_project = ThousandGenomesPhase3Project()
gonl_project = GonlProject()
uk10k_alspac_project = Uk10kAlspacProject()
uk10k_twinsuk_project = Uk10kTwinsUKProject()
counts_in_stats_projects = [exac_project, esp_project, thousand_genomes_phase3_project, thousand_genomes_phase1_project]
frequencies_in_attrs_projects = [thousand_genomes_phase1_project, gonl_project, uk10k_alspac_project, uk10k_twinsuk_project]
project_ids = [project.id for project in counts_in_stats_projects + frequencies_in_attrs_projects]

# extract all variations with frequencies for those projects and and print them
variations_processed = 0
chromosome = None
variant_id = None
if len(sys.argv) > 1:
    if sys.argv[1].startswith('rs'):
        variant_id = sys.argv[1]
    else:
        chromosome = sys.argv[1]
sys.stderr.write('Connecting to EVA Mongo ...\n')
eva_adaptor = EvaMongoAdaptor('database.config')
if chromosome is not None:
    sys.stderr.write('Extracting frequencies from chromosome ' + chromosome + ' ...')
elif variant_id is not None:
    sys.stderr.write('Extracting frequencies for variant ' + variant_id + ' ...')
else:
    sys.stderr.write('Extracting all frequencies ...')
for variation in eva_adaptor.find_variations(project_ids, chromosome=chromosome, variant_id=variant_id):
    variations_processed += 1
    variation.get_frequencies(counts_in_stats_projects, frequencies_in_attrs_projects)
    variation.filter_invalid_frequencies()
    if variation.frequencies is not None and not variation.frequencies.is_empty():
        print variation
sys.stderr.write('\nDone. ' + str(variations_processed) + ' variations processed')
