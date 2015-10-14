import ConfigParser

from pymongo import MongoClient, ReadPreference
import sys
from variation.variation import Variation


class EvaMongoAdaptor:

    def __init__(self, database_config_file):
        config = ConfigParser.ConfigParser()
        config.read(database_config_file)
        hosts = [host for host in config.get('Connection', 'hosts').split(',')]
        user = config.get('Connection', 'user')
        password = config.get('Connection', 'password')
        self.client = self.connect(hosts, user, password)
        db = self.client.eva_hsapiens
        self.variants_collection = db.variants_1_0

    def find_variation_by_id(self, id):
        for variation in self.variants_collection.find({"ids":id}, {"chr":1, "start": 1, "end":1, "ids":1, "ref":1, "alt":1, "files.sid": 1, "files.attrs": 1, "st":1}):
            yield Variation(variation)

    def find_variations(self, projects, chromosome=None):
        proj = []
        for project in projects:
            proj.append({"files.sid": project})
        if chromosome is None:
            filter = {"$or": proj}
        else:
            filter = {"$and": [{"$or": proj}, {"chr": chromosome}]}
        # projects = [{"files.sid": "PRJEB4019"}, {"files.sid": "PRJEB5439"}, {"files.sid": "PRJEB6930"}]
        # TODO: attrs is not going to be needed
        # fields_to_show = {"chr": 1, "start": 1, "end": 1, "ids": 1, "ref": 1, "alt": 1, "files.sid": 1, "files.attrs": 1, "st": 1}
        fields_to_show = {"chr": 1, "start": 1, "end": 1, "ids": 1, "ref": 1, "alt": 1, "files.sid": 1, "st": 1}
        for variation in self.variants_collection.find(filter, fields_to_show):
            if variation['ids'] is not None:
                yield variation

    def find_exac_variations(self):
        for variation in self.variants_collection.find({"$or": [{"files.sid": "130"}]}, {"chr":1, "start": 1, "end":1, "ids":1, "ref":1, "alt":1, "files.sid": 1, "files.attrs": 1, "st":1}):
            if variation['ids'] is not None:
                yield variation

    @staticmethod
    def connect(hosts, user, password):
        try:
            client = MongoClient(hosts, read_preference = ReadPreference.SECONDARY_PREFERRED)
            client.admin.authenticate(user, password, mechanism='MONGODB-CR')
        except:
            e = sys.exc_info()[0]
            print "Error: %s" % e
        return client

    def close(self):
        self.client.close()
