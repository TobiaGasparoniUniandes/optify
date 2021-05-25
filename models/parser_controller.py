from .parser.sets import *
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
        if '\\begin{tabular}' in text:
            return parse_parameters_implicit(text)
        else:
            return parse_parameters_explicit(text)


def parse_variables(text, doc_type):
    if doc_type == LATEX:
        if "_{" in text:
            return parse_variables_implicit(text)
        else:
            return parse_variables_explicit(text)


def parse_constraints(text, doc_type):
    if doc_type == LATEX:
        if "\\sum" in text:
            return parse_constraints_sums_foralls(text)
        else:
            return parse_constraints_nosums_noforalls(text)


def parse_objective_functions(text, doc_type):
    if doc_type == LATEX:
        if "\\sum" in text:
            return parse_objective_functions_implicit(text)
        else:
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


"""
print(json.dumps(parse_parameters('''\\begin{center}
Capacities of the plants\\break\\break
\\begin{tabular}{|c|c|}
\\hline
\\textbf{Plants}&\\textbf{Capacity}\\\\
\\hline
\\textbf{LosAngeles}&1000\\\\
\\hline
\\textbf{Detroit}&1500\\\\
\\hline
\\textbf{NewOrleans}&1200\\\\
\\hline
\\end{tabular}
\\end{center}

\\begin{center}
Demands of the distribution centers\\break\\break
\\begin{tabular}{|c|c|}
\\hline
\\textbf{Distributioncenters}&\\textbf{Demand}\\\\
\\hline
\\textbf{Denver}&2300\\\\
\\hline
\\textbf{Miami}&1400\\\\
\\hline
\\end{tabular}
\\end{center}

\\begin{center}
Transportation cost per car per route\\break\\break
\\begin{tabular}{|c|c|c|}
\\hline
\\multicolumn{3}{|c|}{\\textbf{Cost}}\\\\
\\hline
&\\textbf{Denver}&\\textbf{Miami}\\\\
\\hline
\\textbf{LosAngeles}&80&215\\\\
\\hline
\\textbf{Detroit}&100&108\\\\
\\hline
\\textbf{NewOrleans}&102&68\\\\
\\hline
\\end{tabular}
\\end{center}''', LATEX), indent=4))
"""
