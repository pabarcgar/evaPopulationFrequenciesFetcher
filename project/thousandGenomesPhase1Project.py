from project import Project

__author__ = 'parce'


class ThousandGenomesPhase1Project(Project):

    SUPER_POPULATIONS_G1k_PHASE1 = {'AMR': 'AMR',
                                    'ASN': 'ASN',
                                    'AFR': 'AFR',
                                    'EUR': 'EUR',
                                    'ALL': 'ALL'}

    def __init__(self):
        Project.__init__(self, '8616', 'PRJEB4019', '1000GENOMES_phase_1', populations=self.SUPER_POPULATIONS_G1k_PHASE1, populations_to_exclude=['ALL'])

