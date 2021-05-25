import re
import json

from models.utils.constants import *


def parse_parameters_explicit(parameters):
    """
    $profit\_a=6$\break
    $profit\_b=5$\break
    $tot\_units\_milk=5$\break
    $tot\_units\_choco=12$\break
    $choco\_a=3$\break
    $milk\_a=1$\break
    $choco\_b=2$\break
    $milk\_b=1$

    REGEX doc: https://regex101.com/r/K2PvT2/1
    '''WARNING! ONLY USE THIS LINK IF YOU WANT TO DELETE THIS DOC''':
       https://regex101.com/delete/uZ1G4CUJWzgHR3VivYMIHXJx
    """
    # \$(\w+(?:\\_\w+)*)=(\d+)
    regex = re.compile(r"{}({})=({})".format(DOLLAR, VARIABLE, NUMBER))
    return regex.findall(parameters.replace(" ", ""))


def parse_parameters_implicit(parameters):
    """
    \begin{center}
    Capacities of the plants\break\break
    \begin{tabular}{|c|c|}
    \hline
    \textbf{Plants}&\textbf{Capacity}\\
    \hline
    \textbf{LosAngeles}&1000&50\\
    \hline
    \textbf{Detroit}&1500\\
    \hline
    \textbf{NewOrleans}&1200\\
    \hline
    \end{tabular}
    \end{center}
    """

    response = []

    if 'multicolumn' in parameters:
        response += parse_parameters_implicit_multi(parameters)

    # tablas: https://regex101.com/r/q6E04y/6
    regex = re.compile(
        r"""\\begin\{center\}
(.*)\\break\\break
\\begin\{tabular\}\{\|((?:c\|)*)\}
\\hline
(?:\\textbf\{(\w+)\})(?:&\\textbf\{(\w+)\})*\\\\
\\hline
((?:\\textbf\{\w+\}(?:&\w+)+\\\\
\\hline
)+)\\end\{tabular}
\\end\{center\}""")
    matches = regex.findall(parameters)
    for match in matches:
        response.append(build_param_dict(match))
    return response


def parse_parameters_implicit_multi(parameters):
    # https://regex101.com/r/whwR3E/2
    regex = re.compile(
        r"""\\begin\{center\}
(.*)\\break\\break
\\begin\{tabular\}\{\|((?:c\|)*)\}
\\hline
\\multicolumn\{\d+\}\{\|c\|\}\{\\textbf\{(\w+)\}\}\\\\
\\hline
\&(?:\\textbf\{(\w+)\})(?:&\\textbf\{(\w+)\})*\\\\
\\hline
((?:\\textbf\{\w+\}(?:&\w+)+\\\\
\\hline
)+)\\end\{tabular}
\\end\{center\}"""
    )
    matches = regex.findall(parameters)
    param_objs = []
    for match in matches:
        param_objs.append(build_param_dict_multi(match))
    return param_objs


def build_param_dict_multi(match):
    num_col = len(match[1]) / 2 - 1

    data = clean_data(match[int(num_col) + 3])

    col_heads = []
    matrix = dict()
    i = 0
    while i < num_col:
        col_heads.append(match[3 + i])
        matrix[match[3 + i]] = dict()
        i += 1

    data = data.split(',')
    j = 0
    row_name = ''
    for i in range(0, len(data)):
        if j == 0:
            row_name = data[i]
        else:
            matrix[col_heads[j-1]][row_name] = data[i]

        j += 1
        if j == num_col + 1:
            j = 0

    param_obj = {
        'name': match[0],
        'unit': match[2],
        'data': matrix
    }

    return param_obj


def build_param_dict(match):
    num_col = len(match[1]) / 2

    data = clean_data(match[2 + int(num_col)])

    col_heads = []
    matrix = dict()
    i = 0
    while i < num_col:
        col_heads.append(match[2 + i])
        matrix[match[2 + i]] = []
        i += 1

    data = data.split(',')
    j = 0
    for i in range(0, len(data)):

        matrix[col_heads[j]].append(data[i])

        j += 1
        if j == num_col:
            j = 0

    param_obj = {
        'name': match[0],
        'data': matrix
    }

    return param_obj


def clean_data(data):
    data = data.replace('&', ',')
    data = data.replace('\\\\\n\\hline\n\\textbf{', ',')
    data = data.replace('}', '')
    data = data.replace('\\textbf{', '')
    data = data.replace('\\', '')
    data = data.replace('\nhline\n', '')
    return data
