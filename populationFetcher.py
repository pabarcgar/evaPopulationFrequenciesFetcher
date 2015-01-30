#!/usr/bin/python

__author__ = 'parce'

from pymongo import MongoClient
import urllib


def connect():
    # mongodb://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]
    user = ''
    password = ''
    host = ''
    database = ''
    escaped_password = urllib.quote_plus(password)
    client = MongoClient('mongodb://' + user + ':' + escaped_password + '@' + host + '/' + database)
    return client


def format_frequency(frequency):
    return "{:.5f}".format(frequency)


def get_allele_frequencies_for_esp_allele_counts(allele_counts):
    counts = allele_counts.split(',')
    alternate_count = float(counts[0])
    reference_count = float(counts[1])
    total = reference_count + alternate_count
    if total != 0:
        alternate_frequency = alternate_count / total
        reference_frequency = reference_count / total
        return format_frequency(reference_frequency) + ',' + format_frequency(alternate_frequency)
    else:
        return ''


def get_allele_frequencies_for_esp(attrs):
    frequencies = []

    ea_allele_frequencies = get_allele_frequencies_for_esp_allele_counts(attrs['EA_AC'])
    if ea_allele_frequencies != '':
        frequencies.append('ESP_EA_AF:' + ea_allele_frequencies)
    aa_allele_frequencies = get_allele_frequencies_for_esp_allele_counts(attrs['AA_AC'])
    if aa_allele_frequencies != '':
        frequencies.append('ESP_AA_AF:' +aa_allele_frequencies)

    return ';'.join(frequencies)


def add_1000g_population_frequencies(frequencies, attrs, population_allele_frequency_tag):
    if population_allele_frequency_tag in attrs:
        alternate_allele_frequency = float(attrs[population_allele_frequency_tag])
        reference_allele_frequency = 1.0 - alternate_allele_frequency
        frequencies.append('1000G_' + population_allele_frequency_tag + ':' + str(reference_allele_frequency) + ',' + str(alternate_allele_frequency))


def get_allele_frequencies_for_1000g(attrs):
    frequencies = []
    add_1000g_population_frequencies(frequencies, attrs, 'AMR_AF')
    add_1000g_population_frequencies(frequencies, attrs, 'ASN_AF')
    add_1000g_population_frequencies(frequencies, attrs, 'AFR_AF')
    add_1000g_population_frequencies(frequencies, attrs, 'EUR_AF')
    if len(frequencies) == 0:
        frequencies.append('1000G_AMR_AF:1.0,0.0')
        frequencies.append('1000G_ASN_AF:1.0,0.0')
        frequencies.append('1000G_AFR_AF:1.0,0.0')
        frequencies.append('1000G_EUR_AF:1.0,0.0')
    add_1000g_population_frequencies(frequencies, attrs, 'AF')
    return ';'.join(frequencies)


def get_allele_frequencies(variation):
    frequencies = []
    for file in variation['files']:
        if file['sid'] == 'PRJEB5439':
            frequencies.append(get_allele_frequencies_for_esp(file['attrs']))
        elif file['sid'] == 'PRJEB4019':
            frequencies.append(get_allele_frequencies_for_1000g(file['attrs']))
    return ';'.join(frequencies)

client = connect()


def print_header():
    print 'chr\tstart\tend\trs\tfrequencies'


def find_variations(client):
    db = client.eva_hsapiens_grch37
    variants_collection = db.variants_0_9
    #for variation in variants_collection.find({"$and": [{"files.sid": "PRJEB4019"}, {"files.sid": "PRJEB5439"}]}, {"chr":1, "start": 1, "end":1, "id":1, "ref":1, "alt":1, "files.sid": 1, "files.attrs": 1}).limit(10):
    #for variation in variants_collection.find({"id":"rs375566"}, {"chr":1, "start": 1, "end":1, "id":1, "ref":1, "alt":1, "files.sid": 1, "files.attrs": 1}):
    for variation in variants_collection.find({"$or": [{"files.sid": "PRJEB4019"}, {"files.sid": "PRJEB5439"}]}, {"chr":1, "start": 1, "end":1, "id":1, "ref":1, "alt":1, "files.sid": 1, "files.attrs": 1}):

        yield variation


for variation in find_variations(client):
    id = variation['id']
    if id is not None:
        chromosome = variation['chr']
        start = str(variation['start'])
        end = str(variation['end'])
        frequencies = get_allele_frequencies(variation)
        print '\t'.join([chromosome, start, end, id, frequencies])

client.close()
