import sys
from variation.frequencies.populationFrequencies import PopulationFrequencies
from variation.frequencies.variationFrequencies import VariationFrequencies
from variation.genotypeCounts import GenotypeCounts

__author__ = 'parce'


def get_allelecounts_from_gt_stats(genotype_counts):
    reference_count = 0
    alternate_count = 0
    total_count = 0
    for genotype in genotype_counts:
        genotype_count = genotype_counts[genotype]
        total_count += genotype_count * 2
        if genotype[0] == '0':
            reference_count += genotype_count
        elif genotype[0] == '1':
            alternate_count += genotype_count
        if genotype[2] == '0':
            reference_count += genotype_count
        elif genotype[2] == '1':
            alternate_count += genotype_count
    return reference_count, alternate_count, total_count


class StatVariationFrequencies(VariationFrequencies):
    def __init__(self, projects, stats):
        VariationFrequencies.__init__(self)
        self.super_population_counts = {}
        self.get_population_frequencies_from_stats(projects, stats)
        self.get_super_population_frequencies()

    def get_population_frequencies_from_stats(self, projects, stats):
        for stat in stats:
            frequencies = self.get_frequencies(projects, stat)
            if frequencies is not None:
                self.population_frequencies.append(frequencies)

    def get_frequencies(self, projects, stat):
        for project in projects:
            if stat['sid'] == project.id:
                population = stat['cid']
                population_complete_name = project.name + '_' + population
                try:
                    population_ref_freq, population_alt_freq = self.get_population_frequencies(project, population, stat['numGt'])
                    if not project.exclude_population(population):
                        return PopulationFrequencies(population_complete_name, population_ref_freq, population_alt_freq)
                    else:
                        return None
                except IndexError:
                    sys.stderr.write('\nError extracting sequencies from variant: ' + str(stat['numGt']))
                    return None

    def get_population_frequencies(self, project, population, genotype_counts):
        ref_counts, alt_counts, total_counts = get_allelecounts_from_gt_stats(genotype_counts)
        super_population = project.get_super_population(population)

        if super_population is not None:
            super_population_complete_name = project.name + '_' + super_population
            self.add_super_population_counts(super_population_complete_name, ref_counts, alt_counts, total_counts)
        if total_counts != 0:
            population_ref_freq = float(ref_counts) / total_counts
            population_alt_freq = float(alt_counts) / total_counts
        else:
            population_ref_freq = 0
            population_alt_freq = 0
        return population_ref_freq, population_alt_freq

    def add_super_population_counts(self, super_population, ref_counts, alt_counts, total_counts):
        if super_population not in self.super_population_counts:
            self.super_population_counts[super_population] = GenotypeCounts(ref_counts, alt_counts, total_counts)
        else:
            self.super_population_counts[super_population].add(ref_counts, alt_counts, total_counts)

    def get_super_population_frequencies(self):
        for super_population in self.super_population_counts:
            if self.super_population_counts[super_population].total != 0:
                super_population_ref_freq = float(self.super_population_counts[super_population].reference) / self.super_population_counts[super_population].total
                super_population_alt_freq = float(self.super_population_counts[super_population].alternative) / self.super_population_counts[super_population].total
            else:
                super_population_ref_freq = 0
                super_population_alt_freq = 0
            self.population_frequencies.append(PopulationFrequencies(super_population, super_population_ref_freq, super_population_alt_freq))

