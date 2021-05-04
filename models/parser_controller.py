from .parser.sets import parse_sets_explicit
from .parser.indexes import *
from .parser.parameters import *
from .parser.variables import *
from .parser.constraints import *
from .parser.objective_functions import *


# Parse


def parse_sets(text, doc_type):
    if doc_type == LATEX:
        return parse_sets_explicit(text)


def parse_indexes(text, doc_type):
    if doc_type == LATEX:
        return parse_indexes_explicit(text)


def parse_parameters(text, doc_type):
    if doc_type == LATEX:
        return parse_parameters_explicit(text)


def parse_variables(text, doc_type):
    if doc_type == LATEX:
        return parse_variables_explicit(text)


def parse_constraints(text, doc_type):
    if doc_type == LATEX:
        return parse_constraints_nosums_noforalls(text)


def parse_objective_functions(text, doc_type):
    if doc_type == LATEX:
        return parse_objective_functions_explicit(text)


# Parse Pyomo results


def parse_sets_results(text):
    pass


def parse_indexes_results(text):
    pass


def parse_parameters_results(text):
    pass


def parse_variables_results(text):
    return parse_variables_results_explicit(text)


def parse_constraints_results(text):
    return parse_contraints_results_nosums_noforalls(text)


def parse_objective_functions_results(text):
    return parse_objective_results_explicit(text)
