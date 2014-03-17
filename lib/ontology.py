#!/usr/bin/env python
from lib.db_acess import DBConnect

# Ontology Analysis Methods

class OntologyTerm:
    def __init__(self, goid, term, ngene, genes):
        self.goid = goid
        self.term = term
        self.ngene= ngene
        self.genes= genes

    def __str__(self):
        return ("%s\t%05d\t(%s)\t%s" % (self.goid, self.ngene, self.genes, self.term))

def ontology_query(genes, ontology):
    query = "SELECT COUNT(DISTINCT gene), " \
            "  GROUP_CONCAT(DISTINCT gene), " \
            "  a.goid, term " \
            "FROM new_ontology_data as a, " \
            "  new_ontology_definition as b " \
            "WHERE a.goid = b.goid AND " \
            "  gene IN (%s) AND " \
            "  ontology=%s " \
            "GROUP BY a.goid" % (','.join(map(lambda x:'%s', genes)), '%s')
    result = {}

    for entry in DBConnect.instance().query(query, genes + [ontology]):
        result[entry[2]] = OntologyTerm(entry[2], entry[3], entry[0], entry[1])

    return result