import re

from models.utils.constants import *
from models.utils.data_functions import convert_data


def parse_objective_functions_explicit(objective_function):
    """
    REGEX doc: https://regex101.com/r/YTKK6L/1
    '''WARNING! ONLY USE THIS LINK IF YOU WANT TO DELETE THIS DOC''':
       https://regex101.com/delete/LsuwhFh8M0C5dzRRlOhiWUu2
    """
    # (MIN|MAX)\$(\w+(?:\\_\w+)*)=(\w+(?:\\_\w+)*(?:[*+]\w+(?:\\_\w+)*)*)
    regex = re.compile(r"{}{}({})=({}({}{}{})*)".format(
        MIN_MAX, DOLLAR, VARIABLE, VARIABLE, NO_MATTER_GROUP, OPERANDS, VARIABLE))
    return regex.findall(objective_function.replace(" ", ""))


def parse_objective_results_explicit(result_objectives):
    """
    Objectives:
    obj : Size=1, Index=None, Active=True
        Key  : Active : Value
        None :   True :  27.0

    REGEX doc: https://regex101.com/r/BmvF43/1
    '''WARNING! ONLY USE THIS LINK IF YOU WANT TO DELETE THIS DOC''':
       https://regex101.com/delete/x7JBTEUYGuH7DbTGi1o2iYkl
    """

    # print('Result objectives: ' + result_objectives)
    regex = re.compile(r"(\w+(?:\\_\w+)*):Size=(\d+),Index=(\w+).+\n.+\n(\w+):(\w+):(\w+\.\w+)")

    """The results for the models's objective functions are extracted"""

    matches = regex.findall(result_objectives.replace(" ", "").replace("\t", ""))
    dicts_obj = []
    for obj in matches:
        dicts_obj.append(
            {
                NAME: convert_data(obj[0]),
                SIZE: convert_data(obj[1]),
                INDEX: convert_data(obj[2]),
                KEY: convert_data(obj[3]),
                ACTIVE: convert_data(obj[4]),
                VALUE: convert_data(obj[5])
            }
        )
    return dicts_obj
