from pyomo.environ import *
from pyomo.opt import SolverFactory

z = ConcreteModel('name_model')

profit_a = 6
profit_b = 5
tot_units_milk = 5
tot_units_choco = 12
choco_a = 3
milk_a = 1
choco_b = 2
milk_b = 1

z.units_a = Var(domain=PositiveIntegers)
z.units_b = Var(domain=PositiveIntegers)

z.res1 = Constraint(expr = z.units_a * milk_a + z.units_b * milk_b <= tot_units_milk)
z.res2 = Constraint(expr = z.units_a * choco_a + z.units_b * choco_b <= tot_units_choco)

z.obj = Objective(expr = z.units_a * profit_a + z.units_b * profit_b, sense=maximize)

SolverFactory('glpk').solve(z)

z.display()


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