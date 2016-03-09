class Project:
    def __init__(self, project_internal_id, prj_id, name, populations=None, populations_to_exclude=None):
        self.id = project_internal_id
        self.prj_id = prj_id
        self.name = name
        self.populations = populations
        self.populations_to_exclude = populations_to_exclude

    def get_super_population(self, population):
        super_population = None
        if self.populations is not None:
            super_population = self.populations[population]
        return super_population

    def exclude_population(self, population):
        return self.populations_to_exclude is not None and population in self.populations_to_exclude

    @staticmethod
    def get_frequency_tag(population_tag):
        return population_tag + '_AF'

