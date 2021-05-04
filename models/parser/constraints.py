import re

from models.utils.constants import *
from models.utils.data_functions import convert_data


def parse_constraints_nosums_noforalls(restrictions):
    """
    REGEX doc: https://regex101.com/r/eRVtXL/1
    '''WARNING! ONLY USE THIS LINK IF YOU WANT TO DELETE THIS DOC''':
       https://regex101.com/delete/dqAiPOtB8Glu6PBdVxyK8oti
    """
    # \$(\w+(?:\\_\w+)*(?:[*+]\w+(?:\\_\w+))*)(\\leq)(\w+(\\_\w+)*([*+]\w+(\\_\w+))*)
    regex = re.compile(r"{}({}({}{}{})*)({})({}({}{})*)".format(
        DOLLAR, VARIABLE, NO_MATTER_GROUP, OPERANDS, VARIABLE, LEQ, VARIABLE, OPERANDS, VARIABLE))
    return regex.findall(restrictions.replace(" ", ""))


def parse_contraints_results_nosums_noforalls(result_constraints):
    """
    Constraints:
    res1 : Size=1
        Key  : Lower : Body : Upper
        None :  None :  5.0 :   5.0

    REGEX doc: https://regex101.com/r/UqhxJH/1
    '''WARNING! ONLY USE THIS LINK IF YOU WANT TO DELETE THIS DOC''':
       https://regex101.com/delete/ycG0R13h3dHqGmTECvI4hged
    """

    # print('Result constraints: ' + result_constraints)
    regex = re.compile(r"(\w+(?:\\_\w+)*):Size=(\d+)\n.+\n(\w+):(\w+):(\w+\.\w+):(\w+\.\w+)")

    """The results for the models's constraints are extracted"""

    matches = regex.findall(result_constraints.replace(" ", "").replace("\t", ""))
    dicts_res = []
    for cons in matches:
        dicts_res.append(
            {
                NAME: convert_data(cons[0]),
                SIZE: convert_data(cons[1]),
                KEY: convert_data(cons[2]),
                LOWER: convert_data(cons[3]),
                BODY: convert_data(cons[4]),
                UPPER: convert_data(cons[5])
            }
        )
    return dicts_res
