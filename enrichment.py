#!/usr/bin/env python

import os
from optparse import OptionParser
from yaml import load
from lib import bootstrap, ontology, db_acess
from utils import utils


def main():
    script_path = os.path.dirname(os.path.abspath(__file__))

    usage = "Use: %prog [options] gene-list"
    parser = OptionParser(usage)
    parser.add_option("-p", "--params", dest="params",
                      help="YAML parameters file path",
                      default=os.path.join(script_path, "config.yml"))
    parser.add_option("-g", "--genes", dest="genes",
                      help="Working genes complete list")
    parser.add_option("-i", "--interactions", dest="int",
                      help="The number of interactions")
    parser.add_option("-o", "--ontology", dest="ontology",
                      help="The ontology to be evaluated either: P - process; F - Function")
    parser.add_option("-s", "--sig", dest="sig",
                      help="The p-value bootstrap cutoff")
    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("Incorrect number of arguments")

    __params = load(open(options.params, 'r'))

    # Check parameter override
    if options.int is not None:
        __params['simulation']['interactions'] = int(options.int)
    if options.ontology is not None:
        __params['simulation']['ontology'] = options.ontology
    if options.sig is not None:
        __params['simulation']['significance'] = float(options.sig)
    if options.genes is not None:
        __params['resources']['genes'] = options.genes

    # Loading input file
    utils.set_params(__params)
    __input = utils.filter_input(args[0])

    # Openning Database connection
    db_acess.DBConnect.instance().open(__params['db'])

    # Running simulations
    simulation = bootstrap.BootstrapSM(__input,
                             __params['simulation']['ontology'],
                             __params['simulation']['interactions'],
                             __params['simulation']['significance'])
    simulation.execute()
    print(simulation)

    db_acess.DBConnect.instance().close()


if __name__ == "__main__":
    main()
