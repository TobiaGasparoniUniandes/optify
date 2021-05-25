from __future__ import division
import sys
from io import StringIO

from models.parser_controller import *
from models.utils.constants import *

import pyutilib.subprocess.GlobalData


pyutilib.subprocess.GlobalData.DEFINE_SIGNAL_HANDLERS_DEFAULT = False


def parse_model(sets, indexes, parameters, variables, constraints, objective_functions):
    code = 'from pyomo.environ import *\n'
    code += 'from pyomo.opt import SolverFactory\n\n'

    '''Objective functions are parsed'''
    tuple_obj = objective_parsing(objective_functions)

    code += tuple_obj[0]
    sense = tuple_obj[1]
    model_var = tuple_obj[2]
    objective_function = tuple_obj[3]

    '''Sets are parsed'''
    if sets:
        sets_dict = process_sets(sets, model_var)
        code += sets_dict['code']
        sets = sets_dict['sets']

    '''Indexes are parsed'''
    indexes_dict = None
    if indexes:
        indexes_dict = process_indexes(indexes)

    '''Parameters are parsed'''
    variable_set = {"cost", "num_cars", "capacity", "demand"}
    code += process_parameters(parameters, variable_set, model_var, sets)

    '''Variables are parsed'''
    variable_set = {"cost", "num_cars", "capacity", "demand"}
    code += process_variables(variables, variable_set, model_var, indexes_dict)
    
    '''Constraints are parsed'''
    variable_set = {"cost", "num_cars", "capacity", "demand"}
    code += process_constraints(constraints, variable_set, model_var, indexes_dict=indexes_dict)

    '''Objective functions are parsed (continuation)'''
    variable_set = {"cost", "num_cars", "capacity", "demand"}
    code += generate_objective_function(objective_function, variable_set, model_var, sense, indexes_dict=indexes_dict)

    '''Final setup of code'''
    code += "SolverFactory('glpk').solve({})\n\n".format(model_var)
    code += '{}.display()'.format(model_var)

    print("\n\nCODE\n\n")
    print(code)

    # output = execute_code(code)
    # return generate_api_result(output)


def objective_parsing(objective_functions):
    matches = parse_objective_functions(objective_functions, LATEX)
    objective_function = matches
    sense = MINIMIZE

    if "sums" in matches:

        if objective_function['orientation'] == MAX:
            sense = MAXIMIZE

        prob_name = objective_function['model_var']

    else:
        # Assigns the sense of the objective function
        if objective_function[0] == MAX:
            sense = MAXIMIZE

        # Sets the name of the model
        prob_name = objective_function[1]

    # Formats the model's name from "Model Z" to "model_z"
    model_var = prob_name.lower().replace(" ", "_")

    # Sets up the declaration of the model in the following format: model_z = ConcreteModel('Model Z')
    return "{} = {}('{}')\n\n".format(model_var, CONCRETE_MODEL, prob_name), sense, model_var, objective_function


def process_sets(sets, model_var):
    matches = parse_sets(sets, LATEX)
    string_sets = ""

    for set_name in list(matches.keys()):
        string_sets += "{}.{} = ".format(model_var, set_name) + "{"
        for set_elem in matches[set_name]:
            string_sets += "'{}', ".format(set_elem)
        string_sets += "}\n"
    return {
        'code': string_sets,
        'sets': matches
    }


def process_indexes(indexes):
    matches = parse_indexes(indexes, LATEX)
    dict_indexes = {}
    # Key -> letter
    # Value -> set name
    for match in matches:
        dict_indexes[match[0]] = match[1]
    return dict_indexes


def process_parameters(parameters, variable_set, model_var, sets):
    matches = parse_parameters(parameters, LATEX)
    string_params = ""

    for param in matches:
        string_params += generate_parameter(param, variable_set, model_var, sets)

    return string_params


def process_variables(variables, variable_set, model_var, indexes_dict):
    # Variables' info is extracted from the input
    matches = parse_variables(variables, LATEX)
    string_vars = ""

    for var in matches:
        string_vars += generate_variable(var, variable_set, model_var, indexes_dict)

    return string_vars + "\n"


def process_constraints(constraints, variable_set, model_var, indexes_dict=None):
    string_restr = ""
    matches = parse_constraints(constraints, LATEX)
    i = 1

    if indexes_dict:
        for constraint in matches:
            string_restr += generate_constraint_indexes(constraint, variable_set, model_var, i, indexes_dict)
            i += 1
    else:
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


def generate_parameter(param, variable_set, model_var, sets):
    if "name" in param:
        return generate_parameter_dataset(param, model_var, sets)
    param_name = param[0].replace("\\\\_", "_").replace('\\', '')
    variable_set.add(param_name)
    param_value = int(param[1])

    return "{} = {}\n".format(param_name, param_value)


def generate_parameter_dataset(param, model_var, sets):
    code = ""
    data = param["data"]
    keys = list(data.keys())
    if "unit" in param:
        unit = param["unit"].lower()
        set1 = set()
        set2 = set()
        first = True
        for outer_key in data:
            if first:
                for inner_key in data[outer_key]:
                    set2.add(inner_key)
                first = False
            set1.add(outer_key)
        for set_name in list(sets.keys()):
            if sets[set_name] == set1:
                set1 = set_name
            elif sets[set_name] == set2:
                set2 = set_name

        code += "{}.{} = Param({}.{}, {}.{}, mutable=True)\n".format(model_var,
                                                                     unit,
                                                                     model_var,
                                                                     set2,
                                                                     model_var,
                                                                     set1)
        for outer_key in list(data.keys()):
            for inner_key in list(data[outer_key].keys()):
                code += "{}.{}['{}', '{}'] = {}\n".format(model_var,
                                                          unit,
                                                          inner_key,
                                                          outer_key,
                                                          data[outer_key][inner_key])
    else:
        param_key = keys[0].lower()
        param_value_name = keys[1].lower()
        code += "{}.{} = Param({}.{}, mutable=True)\n".format(model_var,
                                                              param_value_name,
                                                              model_var,
                                                              param_key)
        for i in range(len(data[keys[1]])):
            code += "{}.{}['{}'] = {}\n".format(model_var,
                                                param_value_name,
                                                data[keys[0]][i],
                                                data[keys[1]][i])
    code += "\n"
    return code


def generate_variable(var, variable_set, model_var, indexes_dict):
    var_name = ""
    # If len == 3, it comes with indexes
    if len(var) == 3:
        var_name = var[0].replace("_", "").replace("\\", "_")
        variable_set.add(var_name)
        variable = "{}.{} = Var(".format(model_var, var_name)
        for index in var[1].split(","):
            variable += "{}.{}, ".format(model_var, indexes_dict[index])
        var_domain = var[2]
        if var_domain == N:
            var_domain = POSITIVE_INTEGERS
        variable += "domain={})\n".format(var_domain)

        return variable

    else:
        var_name = var[0].replace("\\\\_", "_").replace('\\', '')

        var_domain = var[1]
        if var_domain == N:
            var_domain = POSITIVE_INTEGERS

        variable_set.add(var_name)

        return "{}.{} = Var(domain={})\n".format(model_var, var_name, var_domain)


def generate_constraint(constraint, variable_set, model_var, i):
    # Sets apart the left section of the operation
    left_part = constraint[0].replace("\\\\_", "_").replace('\\', '').replace("*", " * ").replace("+", " + ")
    left_part = add_prob_var(left_part, variable_set, model_var)

    # Sets apart the right section of the operation
    right_part = constraint[2].replace("\\\\_", "_").replace('\\', '').replace("*", " * ").replace("+", " + ")
    right_part = add_prob_var(right_part, variable_set, model_var)

    # Determines if the constraint is an equality or which inequality
    operand = "=="
    if constraint[1] == "\\leq":
        operand = "<="
    elif constraint[1] == "\\geq":
        operand = ">="

    return "{}.cons{} = Constraint(expr={} {} {})\n".format(model_var, i, left_part, operand, right_part)


def generate_constraint_indexes(constraint, variable_set, model_var, i, indexes_dict):
    # constraints = """\[ \sum_{p} num\_cars_{p,c} = capacity_c, \forall c \]"""
    # z.res1 = ConstraintList()
    # for p in z.plants:
    #     z.res1.add(sum(z.num_cars[p, c] for c in z.distribution_centers) == z.capacity[p])

    # Build the constraint list if there is a forall
    cons_string = "{}.res{} = ConstraintList()\n".format(model_var, i)

    # Build the fors for each forall (LOL)
    j = 0
    for cons_index in constraint["foralls"]:
        cons_string += "\t" * j
        cons_string += "for {} in {}.{}:\n".format(cons_index, model_var,
                                                   indexes_dict[cons_index])
        j += 1

    # Build the constraint
    cons_string += "\t" * j

    # z.num_cars[p, c] for c in z.distribution_centers)
    left_part = ""
    if len(constraint["left"]["sums"]) > 0:
        for j in range(len(constraint["left"]["sums"])):
            if j == 0:
                operation = constraint["left"]["operation"].replace("\\\\", "").replace("_{", "[").replace("}", "]")\
                    .replace("\\", "")

                left_part += "sum({} for {} in {}.{})".format(operation, constraint["left"]["sums"][j], model_var,
                                                              indexes_dict[constraint["left"]["sums"][j]])
            else:
                left_part = "sum({} for {} in {}.{})".format(left_part, constraint["left"]["sums"][j], model_var,
                                                             indexes_dict[constraint["left"]["sums"][j]])
    else:
        left_part += constraint["left"]["operation"].replace("\\\\", "").replace("_{", "[").replace("}", "]") \
            .replace("\\", "")

    for entity_name in list(variable_set):
        left_part = left_part.replace(entity_name, "{}.{}".format(model_var, entity_name))

    right_part = ""
    if len(constraint["right"]["sums"]) > 0:
        for j in range(len(constraint["right"]["sums"])):
            if j == 0:
                operation = constraint["right"]["operation"].replace("\\\\", "").replace("_{", "[").replace("}", "]") \
                    .replace("\\", "")
                right_part += "sum({} for {} in {}.{})".format(operation, constraint["right"]["sums"][j], model_var,
                                                               indexes_dict[constraint["right"]["sums"][j]])
            else:
                right_part = "sum({} for {} in {}.{})".format(right_part, constraint["right"]["sums"][j], model_var,
                                                              indexes_dict[constraint["right"]["sums"][j]])
    else:
        right_part += constraint["right"]["operation"].replace("\\\\", "").replace("_{", "[").replace("}", "]") \
            .replace("\\", "")

    for entity_name in list(variable_set):
        right_part = right_part.replace(entity_name, "{}.{}".format(model_var, entity_name))

    operand = "=="
    if constraint["operand"] == "\\leq":
        operand = "<="
    elif constraint["operand"] == "\\geq":
        operand = ">="

    cons_string += "{}.res{}.add({} {} {})\n".format(model_var, i, left_part, operand, right_part)

    return cons_string


def generate_objective_function(objective_function, variable_set, model_var, sense, indexes_dict=None):
    if "sums" in objective_function:
        part = ""
        for j in range(len(objective_function["sums"])):
            if j == 0:
                operation = objective_function["operation"].replace("\\\\", "").replace("_{", "[").replace("}", "]") \
                    .replace("\\", "")
                # TODO add model_var before every var
                part += "sum({} for {} in {}.{})".format(operation, objective_function["sums"][j], model_var,
                                                         indexes_dict[objective_function["sums"][j]])
            else:
                part = "sum({} for {} in {}.{})".format(part, objective_function["sums"][j], model_var,
                                                        indexes_dict[objective_function["sums"][j]])
        for entity_name in list(variable_set):
            part = part.replace(entity_name, "{}.{}".format(model_var, entity_name))
        return "{}.obj = Objective(expr={}, sense={})\n\n".format(model_var, part, sense)
    else:
        operation = objective_function[2].replace("\\_", "_").replace("*", " * ").replace("+", " + ")
        operation = add_prob_var(operation, variable_set, model_var)

    return "{}.obj = Objective(expr={}, sense={})\n\n".format(model_var, operation, sense)


def execute_code(code):
    # The models is ran in an internal environment
    old_stdout = sys.stdout
    # The printed output is captured for the current environment
    output = sys.stdout = StringIO()
    exec(code)
    sys.stdout = old_stdout
    print("\n\nRESULT OF EXECUTION\n\n" + output)
    return output


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


sets1 = """$plants = \\{Los Angeles, Detroit, New Orleans\\}$\\break\n
$centers = \\{Denver, Miami\\}$"""

indexes1 = """$p\\in plants$\\break\n
$c\\in centers$\\break"""

parameters1 = """\\begin{center}
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
\\textbf{Centers}&\\textbf{Demand}\\\\
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
\\end{center}"""

variables1 = """$num\\_cars_{p,c}\\in\\mathbb{N}$"""

constraints1 = """\\[ \\sum_{c} num\\_cars_{p,c} = capacity_{p}, \\forall p \\]
\\[ \\sum_{p} num\\_cars_{p,c} = demand_{c}, \\forall c \\]"""

objective_function1 = """MIN Z $ =  \\sum_{c} \\sum_{p} cost_{p,c} * num\\_cars_{p,c} $"""

parse_model(sets1, indexes1, parameters1, variables1, constraints1, objective_function1)
