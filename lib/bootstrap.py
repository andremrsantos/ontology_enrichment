#!/usr/bin/env python

from random import shuffle
from lib.ontology import ontology_query
from utils.utils import all_genes

# Bootstrap simulation implementation
class BootstrapSM:

    def __init__(self, genes,
                 ontology = 'P',
                 interactions = 1000,
                 significance=0.1):
        self.__genes = genes
        self.__ngene = len(genes)
        self.__genes_ontology = ontology_query(genes, ontology)
        self.__enrichment = dict.fromkeys(self.__genes_ontology.keys(), 0)
        self.__ontology = ontology
        self.__interactions = interactions
        self.__significance=significance

    def execute(self):
        self.__simulate()
        for key in self.__enrichment.keys():
            self.__enrichment[key] /= float(self.__interactions)
        return self

    def __str__(self):
        keys = self.__genes_ontology
        header = "## GO Gene Enrichment Evaluation\n" \
                 "## Number of Genes Evaluated: %5d\n" \
                 "## Number of ontologies: %5d\n" \
                 "## P-value\tGOID\tN_Genes\tGenes\tTerm\n" % (self.__ngene, len(keys))
        ontology = '\n'.join([
            ("%1.4f\t%s" % (self.__enrichment[k], self.__genes_ontology[k])) for k in keys if self.__enrichment[k] <= self.__significance
        ])
        return header + ontology

    def __simulate(self):
        allgenes = all_genes()
        for i in range(self.__interactions):
            shuffle(allgenes)
            set = allgenes[:self.__ngene]
            ontology = ontology_query(set, self.__ontology)
            self.__compute(ontology)

    def __compute(self, obs):
        for key in self.__enrichment.keys():
            if obs.has_key(key) and obs[key].ngene >= self.__genes_ontology[key].ngene:
                self.__enrichment[key] += 1
