from __future__ import division
import sys
from io import StringIO

from models.parser_controller import *
from models.utils.constants import *

import pyutilib.subprocess.GlobalData


pyutilib.subprocess.GlobalData.DEFINE_SIGNAL_HANDLERS_DEFAULT = False


def parse_model(parameters, variables, constraints, objective_functions):
    code = 'from pyomo.environ import *\n'
    code += 'from pyomo.opt import SolverFactory\n\n'

    '''Objective functions are parsed'''

    matches = parse_objective_functions(objective_functions, LATEX)
    objective_function = matches[0]

    # Assigns the sense of the objective function
    sense = MINIMIZE
    if objective_function[0] == MAX:
        sense = MAXIMIZE

    prob_name = objective_function[1]
    # Formats the model's name from "Model Z" to "model_z"
    model_var = prob_name.lower().replace(" ", "_")
    # Sets up the declaration of the model in the following format: model_z = ConcreteModel('Model Z')
    string_declaration = "{} = {}('{}')\n\n".format(model_var, CONCRETE_MODEL, prob_name)

    code += string_declaration
    
    '''Parameters are parsed'''

    code += process_parameters(parameters)

    '''Variables are parsed'''

    variable_set = set()
    code += process_variables(variables, variable_set, model_var)
    
    '''Constraints are parsed'''

    code += process_constraints(constraints, variable_set, model_var)

    '''Objective functions are parsed (continuation)'''

    operation = objective_function[2].replace("\\_", "_").replace("*", " * ").replace("+", " + ")
    operation = add_prob_var(operation, variable_set, model_var)
    string_objfunc = "{}.obj = Objective(expr = {}, sense={})\n".format(model_var, operation, sense)
    code += string_objfunc + "\n"

    '''Code is setup in the end'''

    code += "SolverFactory('glpk').solve({})\n\n".format(model_var)
    code += '{}.display()'.format(model_var)
    # print(r'{}'.format(code))

    # The models is ran in an internal environment
    old_stdout = sys.stdout
    # The printed output is captured for the current environment
    redirected_output = sys.stdout = StringIO()
    exec(code)
    sys.stdout = old_stdout

    return generate_api_result(redirected_output)


def process_parameters(parameters):
    matches = parse_parameters(parameters, LATEX)
    string_params = ""
    for param in matches:
        string_params += generate_parameter(param)
    return string_params + "\n"


def process_variables(variables, variable_set, model_var):
    # Variables' info is extracted from the input
    matches = parse_variables(variables, LATEX)
    string_vars = ""
    for var in matches:
        string_vars += generate_variable(var, variable_set, model_var)
    return string_vars + "\n"


def process_constraints(constraints, variable_set, model_var):
    matches = parse_constraints(constraints, LATEX)
    string_restr = ""
    i = 1
    for constraint in matches:
        string_restr += generate_constraint(constraint, variable_set, model_var, i)
        i += 1

    return string_restr + "\n"


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


def generate_parameter(param):
    param_name = param[0].replace("\\\\_", "_").replace('\\', '')
    param_value = int(param[1])
    return "{} = {}\n".format(param_name, param_value)


def generate_variable(var, variable_set, model_var):
    var_name = var[0].replace("\\\\_", "_").replace('\\', '')
    variable_set.add(var_name)

    var_set = var[1]
    if var_set == N:
        var_set = POSITIVE_INTEGERS

    return "{}.{} = Var(domain={})\n".format(model_var, var_name, var_set)


def generate_constraint(constraint, variable_set, model_var, i):
    # Sets apart the left section of the operation
    left_part = constraint[0].replace("\\\\_", "_").replace('\\', '').replace("*", " * ").replace("+", " + ")
    left_part = add_prob_var(left_part, variable_set, model_var)

    # Sets apart the right section of the operation
    right_part = constraint[2].replace("\\\\_", "_").replace('\\', '').replace("*", " * ").replace("+", " + ")
    right_part = add_prob_var(right_part, variable_set, model_var)

    # Determines if the constraint is an equality or which inequality
    operand = "="
    if constraint[1] == "\\leq":
        operand = "<="
    elif constraint[1] == "\\geq":
        operand = ">="

    return "{}.cons{} = Constraint(expr={} {} {})\n".format(model_var, i, left_part, operand, right_part)


def generate_api_result(output):
    # The global result is selectively separated into its different parts to be processed
    split_result = output.getvalue().split('\n\n')
    result_variables = split_result[1]
    result_objectives = split_result[2]
    result_constraints = split_result[3]

    # The models's results are extracted
    model_name = ' '.join(split_result[0].split(' ')[1:])
    dicts_var = parse_variables_results(result_variables)
    dicts_obj = parse_objective_functions_results(result_objectives)
    dicts_res = parse_constraints_results(result_constraints)

    # The final result to be returned is built
    result = {
        NAME: model_name,
        VARIABLES: dicts_var,
        OBJECTIVES: dicts_obj,
        CONSTRAINTS: dicts_res
    }

    return result
