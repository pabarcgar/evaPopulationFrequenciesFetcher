from project import Project

SUPER_POPULATIONS_G1k_PHASE3 = {'ACB': 'AFR',
                                'ASW': 'AFR',
                                'ESN': 'AFR',
                                'LWK': 'AFR',
                                'MAG': 'AFR',
                                'GWD': 'AFR',
                                'MSL': 'AFR',
                                'YRI': 'AFR',
                                'CLM': 'AMR',
                                'MXL': 'AMR',
                                'PEL': 'AMR',
                                'PUR': 'AMR',
                                'CDX': 'EAS',
                                'CHB': 'EAS',
                                'CHD': 'EAS',
                                'CHS': 'EAS',
                                'JPT': 'EAS',
                                'KHV': 'EAS',
                                'CEU': 'EUR',
                                'FIN': 'EUR',
                                'GBR': 'EUR',
                                'IBS': 'EUR',
                                'TSI': 'EUR',
                                'BEB': 'SAS',
                                'GIH': 'SAS',
                                'ITU': 'SAS',
                                'PJL': 'SAS',
                                'STU': 'SAS',
                                'ALL': 'ALL'
                                }


class ThousandGenomesPhase3Project(Project):
    def __init__(self):
        Project.__init__(self, '301', 'PRJEB6930', '1000GENOMES_phase_3', SUPER_POPULATIONS_G1k_PHASE3, SUPER_POPULATIONS_G1k_PHASE3.keys())
