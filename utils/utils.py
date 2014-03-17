#! /usr/bin/env python

__params = None
__genes  = None


def set_params(params):
    global __params
    __params = params

def read_list(path):
    return [line.rstrip() for line in open(path)]


def all_genes():
    global __genes
    if __genes is None :
        __genes = read_list(__params['resources']['genes'])
    return __genes

def filter_input(ipt):
    all = dict.fromkeys(all_genes())
    result = []
    for i in read_list(ipt):
        if all.has_key(i):
            result.append(i)
    return result