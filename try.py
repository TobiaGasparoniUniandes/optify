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
