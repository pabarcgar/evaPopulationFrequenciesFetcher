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

    def find_variations(self, projects, chromosome=None, variant_id=None):
        query_filter = self.get_query_filter(chromosome, projects, variant_id)
        fields_to_show = {"chr": 1, "start": 1, "end": 1, "ref": 1, "alt": 1, "files.sid": 1, "files.attrs": 1, "st": 1}
        for variation in self.variants_collection.find(query_filter, fields_to_show):
            yield Variation(variation)

    @staticmethod
    def get_query_filter(chromosome, projects, variant_id):
        proj = []
        for project in projects:
            proj.append({"files.sid": project})
        if variant_id is None:
            if chromosome is None:
                query_filter = {"$or": proj}
            else:
                query_filter = {"$and": [{"$or": proj}, {"chr": chromosome}]}
        else:
            query_filter = {"ids": variant_id}
        return query_filter

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
