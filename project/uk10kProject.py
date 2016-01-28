__author__ = 'parce'

from project import Project

UK10K_POPULATIONS = {'AMR': 'AMR',
                     'ASN': 'ASN',
                     'AFR': 'AFR',
                     'EUR': 'EUR'}


class Uk10kProject(Project):
    def __init__(self, project_id, name):
        Project.__init__(self, project_id, name, populations=UK10K_POPULATIONS)

    @staticmethod
    def get_frequency_tag(population_tag):
        return 'AF_' + population_tag
