class Project:
    def __init__(self, project_id, name, populations=None):
        self.id = project_id
        self.name = name
        self.populations = populations

    def get_super_population(self, population):
        super_population = None
        if self.populations is not None:
            super_population = self.populations[population]
        return super_population
