from project import Project

__author__ = 'parce'


class ThousandGenomesPhase1Project(Project):

    SUPER_POPULATIONS_G1k_PHASE1 = {'AMR': 'AMR',
                                    'ASN': 'ASN',
                                    'AFR': 'AFR',
                                    'EUR': 'EUR',
                                    'ALL': 'ALL'}

    def __init__(self):
        Project.__init__(self, '8616', '1000G_PHASE_1', populations=self.SUPER_POPULATIONS_G1k_PHASE1, populations_to_exclude=['ALL'])
        self.population_tags = self.SUPER_POPULATIONS_G1k_PHASE1.keys()

