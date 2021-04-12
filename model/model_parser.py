import re

'''
Constants
'''

# REGEX
NO_MATTER = r"?:"
VARIABLE = r"\w+(?:\\_\w+)*"
MIN_MAX = r"(MIN|MAX)"
DOLLAR = r"\$"
OPERANDS = r"[*+]"
NUMBER = r"\d+"
IN = r"\\in"
MATHBB = r"\\mathbb"
N = r"N"
OPEN_BRACKETS = r"\{"
CLOSE_BRACKETS = r"\}"
LEQ = r"\\leq"

# TEXT
MAXIMIZE = "maximize"
MIN = "MIN"
CONCRETE_MODEL = "ConcreteModel('name_model')"
POSITIVE_INTEGERS = "PositiveIntegers"


'''
Functions for parsing input model
'''


def parse_parameters(parameters):
    """
    REGEX doc: https://regex101.com/r/K2PvT2/1
    To delete: https://regex101.com/delete/uZ1G4CUJWzgHR3VivYMIHXJx
    """
    # \$(\w+(?:\\_\w+)*)=(\d+)
    regex = re.compile(r"{}({})=({})".format(DOLLAR, VARIABLE, NUMBER))
    return regex.findall(parameters.replace(" ", ""))


def parse_variables(variables):
    """
    REGEX doc: https://regex101.com/r/eKi5Dy/1
    To delete: https://regex101.com/delete/PStWctHwnR3IQINIIg1aHGoc
    """
    variable_set = set()
    # \$(\w+[\\_\w]*)\\in\\mathbb\{(N)\}\$
    regex = re.compile(r"{}({}){}{}{}({}){}\$".format(
        DOLLAR, VARIABLE, IN, MATHBB, OPEN_BRACKETS, N, CLOSE_BRACKETS))
    return regex.findall(variables.replace(" ", ""))


def parse_objective(objective_function):
    """
    REGEX doc: https://regex101.com/r/YTKK6L/1
    To delete: https://regex101.com/delete/LsuwhFh8M0C5dzRRlOhiWUu2
    """
    # (MIN|MAX)\$(\w+(?:\\_\w+)*)=(\w+(?:\\_\w+)*(?:[*+]\w+(?:\\_\w+)*)*)
    regex = re.compile(r"{}{}({})=({}({}{}{})*)".format(
        MIN_MAX, DOLLAR, VARIABLE, VARIABLE, NO_MATTER, OPERANDS, VARIABLE))
    return regex.findall(objective_function.replace(" ", ""))


def parse_restrictions(restrictions):
    """
    REGEX doc: https://regex101.com/r/eRVtXL/1
    To delete: https://regex101.com/delete/dqAiPOtB8Glu6PBdVxyK8oti
    """
    # \$(\w+(?:\\_\w+)*(?:[*+]\w+(?:\\_\w+))*)(\\leq)(\w+(\\_\w+)*([*+]\w+(\\_\w+))*)
    regex = re.compile(r"{}({}({}{}{})*)({})({}({}{})*)".format(
        DOLLAR, VARIABLE, NO_MATTER, OPERANDS, VARIABLE, LEQ, VARIABLE, OPERANDS, VARIABLE))
    return regex.findall(restrictions.replace(" ", ""))


'''
Functions for parsing model results
'''


def parse_variables_results(result_variables):
    """
    When result is captured:

    Variables:
    units_a : Size=1, Index=None
        Key  : Lower : Value : Upper : Fixed : Stale : Domain
        None :     1 :   2.0 :  None : False : False : PositiveIntegers
    units_b : Size=1, Index=None

    https://regex101.com/r/OBc1Ib/1
    https://regex101.com/delete/wIJH9tgLAQ3Kj7u4DepSiy4S
    """

    regex = re.compile(r"(\w+(?:\\_\w+)*):Size=\d+,Index=(\w+)\n.+\n(\w+):(\d+):(\w+\.\w+):(\w+):(\w+):(\w+):(\w+)")
    return regex.findall(result_variables.replace(" ", "").replace("\t", ""))


def parse_objective_results(result_objectives):
    """
    Objectives:
    obj : Size=1, Index=None, Active=True
        Key  : Active : Value
        None :   True :  27.0

    https://regex101.com/r/BmvF43/1
    https://regex101.com/delete/x7JBTEUYGuH7DbTGi1o2iYkl

    """

    # print('Result objectives: ' + result_objectives)
    regex = re.compile(r"(\w+(?:\\_\w+)*):Size=(\d+),Index=(\w+).+\n.+\n(\w+):(\w+):(\w+\.\w+)")
    return regex.findall(result_objectives.replace(" ", "").replace("\t", ""))


def parse_restrictions_results(result_constraints):
    """
    Constraints:
    res1 : Size=1
        Key  : Lower : Body : Upper
        None :  None :  5.0 :   5.0

    https://regex101.com/r/UqhxJH/1
    https://regex101.com/delete/ycG0R13h3dHqGmTECvI4hged
    """

    # print('Result constraints: ' + result_constraints)
    regex = re.compile(r"(\w+(?:\\_\w+)*):Size=(\d+)\n.+\n(\w+):(\w+):(\w+\.\w+):(\w+\.\w+)")
    return regex.findall(result_constraints.replace(" ", "").replace("\t", ""))
