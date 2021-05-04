import re

from models.utils.constants import *
from models.utils.data_functions import convert_data


def parse_variables_explicit(variables):
    """
    REGEX doc: https://regex101.com/r/GujKW1/1
    '''WARNING! ONLY USE THIS LINK IF YOU WANT TO DELETE THIS DOC''':
       https://regex101.com/delete/uprDErQSIE5NXHPwzlONoS8o
    """
    # \$(\w+[\\_\w]*)\\in\\mathbb\{(N)\}\$
    regex = re.compile(r"{}({}){}{}{}({}){}\$".format(
        DOLLAR, VARIABLE, IN, MATHBB, OPEN_BRACKETS, N, CLOSE_BRACKETS))
    return regex.findall(variables.replace(" ", ""))


def parse_variables_results_explicit(result_variables):
    """
    When result is captured:

    Variables:
    units_a : Size=1, Index=None
        Key  : Lower : Value : Upper : Fixed : Stale : Domain
        None :     1 :   2.0 :  None : False : False : PositiveIntegers
    units_b : Size=1, Index=None

    REGEX doc: https://regex101.com/r/OBc1Ib/1
    '''WARNING! ONLY USE THIS LINK IF YOU WANT TO DELETE THIS DOC''':
       https://regex101.com/delete/wIJH9tgLAQ3Kj7u4DepSiy4S
    """

    regex = re.compile(r"(\w+(?:\\_\w+)*):Size=\d+,Index=(\w+)\n.+\n(\w+):(\d+):(\w+\.\w+):(\w+):(\w+):(\w+):(\w+)")

    matches = regex.findall(result_variables.replace(" ", "").replace("\t", ""))
    dicts_var = []
    for var in matches:
        dicts_var.append(
            {
                NAME: convert_data(var[0]),
                INDEX: convert_data(var[1]),
                KEY: convert_data(var[2]),
                LOWER: convert_data(var[3]),
                VALUE: convert_data(var[4]),
                UPPER: convert_data(var[5]),
                FIXED: convert_data(var[6]),
                STALE: convert_data(var[7]),
                DOMAIN: convert_data(var[8]),
            }
        )
    return dicts_var
