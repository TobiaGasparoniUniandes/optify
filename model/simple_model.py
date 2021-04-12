from __future__ import division
import re
import sys
from io import StringIO
from .model_parser import parse_variables, parse_parameters, parse_objective, parse_restrictions
from .model_parser import parse_variables_results, parse_objective_results, parse_restrictions_results

import pyutilib.subprocess.GlobalData
pyutilib.subprocess.GlobalData.DEFINE_SIGNAL_HANDLERS_DEFAULT = False

'''
Constants
'''

# REGEX

VARIABLE = r"\w+(?:\\_\w+)*"
N = r"N"

# TEXT

MAXIMIZE = "maximize"
MIN = "MIN"
CONCRETE_MODEL = "ConcreteModel('name_model')"
POSITIVE_INTEGERS = "PositiveIntegers"

# API RESULT KEYS

NAME = 'name'
VARIABLES = 'variables'
INDEX = 'index'
KEY = 'key'
LOWER = 'lower'
VALUE = 'value'
UPPER = 'upper'
FIXED = 'fixed'
STALE = 'stale'
DOMAIN = 'domain'
ACTIVE = 'active'
SIZE = 'size'
BODY = 'body'
CONSTRAINTS = 'constraints'
OBJECTIVES = 'objectives'

'''
Begin input


parameters = """$profit\_a=6$\break
$profit\_b=5$\break
$tot\_units\_milk=5$\break
$tot\_units\_choco=12$\break
$choco\_a=3$\break
$milk\_a=1$\break
$choco\_b=2$\break
$milk\_b=1$"""

variables = """$units\_a \in \mathbb{N}$\break
$units\_b \in \mathbb{N}$"""

restrictions = """$units\_a * milk\_a + units\_b * milk\_b \leq tot\_units\_milk$\break
$units\_a * choco\_a + units\_b * choco\_b \leq tot\_units\_choco$"""

objective_function = "MAX $Z = units\_a * profit\_a + units\_b * profit\_b$"


End input
'''


def parse_model(parameters, variables, restrictions, objective_functions):
    code = 'from pyomo.environ import *\n'

    code += 'from pyomo.opt import SolverFactory\n\n'

    # Objective functions are parsed

    matches = parse_objective(objective_functions)
    function = matches[0]
    func_type = MAXIMIZE
    if function[0] == MIN:
        func_type = "minimize"
    prob_name = function[1]
    prob_var = prob_name.lower().replace(" ", "_")
    string_declaration = "{} = {}\n\n".format(prob_var, CONCRETE_MODEL)
    code += string_declaration
    
    # Parameters are parsed

    matches = parse_parameters(parameters)
    string_params = ""
    for param in matches:
        param_name = param[0].replace("\\\\_", "_").replace('\\', '')
        param_value = int(param[1])
        string_params += ("{} = {}\n".format(param_name, param_value))
    code += string_params + "\n"
    
    # Variables are parsed

    matches = parse_variables(variables)
    variable_set = set()
    string_vars = ""
    for var in matches:
        var_name = var[0].replace("\\\\_", "_").replace('\\', '')
        variable_set.add(var_name)
        var_set = var[1]
        
        if var_set == N:
            var_set = POSITIVE_INTEGERS
        
        string_vars += "{}.{} = Var(domain={})\n".format(prob_var,
                                                         var_name,
                                                         var_set)
    code += string_vars + "\n"
    
    # Restrictions are parsed

    matches = parse_restrictions(restrictions)
    string_restr = ""
    i = 1
    for restriction in matches:
        left_part = restriction[0].replace("\\\\_", "_").replace('\\', '').replace("*", " * ").replace("+", " + ")
        right_part = restriction[2].replace("\\\\_", "_").replace('\\', '').replace("*", " * ").replace("+", " + ")
        
        left_part = add_prob_var(left_part, variable_set, prob_var)
        right_part = add_prob_var(right_part, variable_set, prob_var)
        
        operand = "="
        
        if restriction[1] == "\\leq":
            operand = "<="
        elif restriction[1] == "\\geq":
            operand = ">="
        
        string_restr += "{}.res{} = Constraint(expr = {} {} {})\n".format(prob_var, i, left_part, operand, right_part)
        i += 1
        
    code += string_restr + "\n"
    
    operation = function[2].replace("\\_", "_").replace("*", " * ").replace("+", " + ")
    operation = add_prob_var(operation, variable_set, prob_var)

    string_objfunc = "{}.obj = Objective(expr = {}, sense={})\n".format(prob_var, operation, func_type)

    code += string_objfunc + "\n"
    code += "SolverFactory('glpk').solve({})\n\n".format(prob_var)
    code += '{}.display()'.format(prob_var)
    print(r'{}'.format(code))

    # The model is ran in an internal environment
    # The printed output is captured in the current environment

    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    exec(code)
    sys.stdout = old_stdout
    split = redirected_output.getvalue().split('\n\n')

    # The global result is selectively separated into its different parts to be processed

    result_variables = split[1]
    result_objectives = split[2]
    result_constraints = split[3]

    # The model's results are extracted

    model_name = ' '.join(split[0].split(' ')[1:])
    dicts_var = extract_variables_result(result_variables)
    dicts_obj = extract_objectives_result(result_objectives)
    dicts_res = extract_restrictions_result(result_constraints)

    # The final result to be returned is built

    return {
        NAME: model_name,
        VARIABLES: dicts_var,
        OBJECTIVES: dicts_obj,
        CONSTRAINTS: dicts_res
    }


def add_prob_var(og_var, variable_set, prob_var):
    sub_regex = re.compile(r"({})".format(VARIABLE))
    sub_matches = sub_regex.findall(og_var.replace(" ", ""))
    sub_set = set()
    for res in sub_matches:
        if res in variable_set:
            sub_set.add(res)
    for res in sub_set:
        og_var = og_var.replace(res, "{}.{}".format(prob_var, res))
    return og_var


def extract_variables_result(result_variables):
    """The results for the model's variables are extracted"""

    matches = parse_variables_results(result_variables)
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


def extract_objectives_result(result_objectives):
    """The results for the model's objective functions are extracted"""

    matches = parse_objective_results(result_objectives)
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


def extract_restrictions_result(result_constraints):
    """The results for the model's restrictions are extracted"""

    matches = parse_restrictions_results(result_constraints)
    dicts_res = []
    for res in matches:
        dicts_res.append(
            {
                NAME: convert_data(res[0]),
                SIZE: convert_data(res[1]),
                KEY: convert_data(res[2]),
                LOWER: convert_data(res[3]),
                BODY: convert_data(res[4]),
                UPPER: convert_data(res[5])
            }
        )
    return dicts_res


def convert_data(string):
    """
    :param string: value in string format
    :return: the value in its original format
    """
    if string == 'None':
        return None
    elif string == 'True':
        return True
    elif string == 'False':
        return False
    elif isint(string):
        return int(float(string))
    elif isfloat(string):
        return float(string)
    else:
        return string


# Function adapted from
# https://stackoverflow.com/questions/15357422/python-determine-if-a-string-should-be-converted-into-int-or-float
def isfloat(x):
    try:
        float(x)
    except (TypeError, ValueError):
        return False
    else:
        return True


# Function taken from
# https://stackoverflow.com/questions/15357422/python-determine-if-a-string-should-be-converted-into-int-or-float
def isint(x):
    try:
        a = float(x)
        b = int(a)
    except (TypeError, ValueError):
        return False
    else:
        return a == b


# parse_model()

# from pulp import *

# from pyomo.environ import *

# from pyomo.opt import SolverFactory

# z = ConcreteModel()

# profit_a = 6
# profit_b = 5
# tot_units_milk = 5
# tot_units_choco = 12
# choco_a = 3
# milk_a = 1
# choco_b = 2
# milk_b = 1

# z.units_a = Var(domain=PositiveIntegers)
# z.units_b = Var(domain=PositiveIntegers)

# z.res1 = Constraint(expr = z.units_a * milk_a + z.units_b * milk_b <= tot_units_milk)
# z.res2 = Constraint(expr = z.units_a * choco_a + z.units_b * choco_b <= tot_units_choco)

# z.obj = Objective(expr = z.units_a * profit_a + z.units_b * profit_b, sense=maximize)

# SolverFactory('glpk').solve(z)

# z.display()
