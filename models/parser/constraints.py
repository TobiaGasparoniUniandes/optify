import re
import json

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


def parse_constraints_sums_foralls(restrictions):
    """
    REGEX doc: https://regex101.com/r/Iw4jYq/2
    '''WARNING! ONLY USE THIS LINK IF YOU WANT TO DELETE THIS DOC''':
        https://regex101.com/delete/E8f294yIn5SseFYNb5hw5eyz
    """
    regex = re.compile(r"\\\[(.*)(=|\\leq|\\geq)(.*),\\(forall\w)\\\]")
    matches = regex.findall(restrictions.replace(" ", ""))
    response = []
    for match in matches:
        left = match[0]
        sums_left = generate_sum(left)
        left = left.replace(parse_sums(left), "")
        """
        REGEX doc: https://regex101.com/r/3inpXa/1
        '''WARNING! ONLY USE THIS LINK IF YOU WANT TO DELETE THIS DOC''':
            https://regex101.com/delete/F9qi98b3bWgLgzitU9SLTHRj
        """

        right = match[2]
        sums_right = generate_sum(right)
        right = right.replace(parse_sums(right), "")

        operand = match[1]
        foralls = match[3]
        foralls = foralls.replace("forall", "")
        foralls = foralls.split(",")

        response.append({
            "right": {
                "sums": sums_right,
                "operation": right
            },
            "left": {
                "sums": sums_left,
                "operation": left
            },
            "operand": operand,
            "foralls": foralls
        })

    return response


def generate_sum(segment):
    if "\\sum_{" not in segment:
        return []
    sums = parse_sums(segment)
    sums = sums.split("\\sum_{")
    for i in range(len(sums)):
        sums[i] = sums[i].replace("}", "")
    return sums[1:]


def parse_sums(sums):
    """
    REGEX doc: https://regex101.com/r/htLfAo/2
    '''WARNING! ONLY USE THIS LINK IF YOU WANT TO DELETE THIS DOC''':
        https://regex101.com/delete/iJKk5TlLNHEoiFft3Iw1nbHa
    """
    if "\\sum_{" not in sums:
        return ""
    regex = re.compile(r"(?:\\sum\_{\w})+")
    matches = regex.findall(sums)[0]
    return matches


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
