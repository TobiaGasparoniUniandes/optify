from pyomo.environ import *
from pyomo.opt import SolverFactory

z = ConcreteModel('name_model')

z.plants = {'Los Angeles', 'Detroit', 'New Orleans',}
z.centers = {'Denver', 'Miami'}

z.capacity = Param(z.plants, mutable=True)
z.capacity['Los Angeles'] = 1000
z.capacity['Detroit'] = 1500
z.capacity['New Orleans'] = 1200

z.demand = Param(z.centers, mutable=True)
z.demand['Denver'] = 2300
z.demand['Miami'] = 1400

z.cost = Param(z.plants, z.centers, mutable=True)
z.cost['Los Angeles', 'Denver'] = 80
z.cost['Detroit', 'Denver'] = 100
z.cost['New Orleans', 'Denver'] = 102
z.cost['Los Angeles', 'Miami'] = 215
z.cost['Detroit', 'Miami'] = 108
z.cost['New Orleans', 'Miami'] = 68

z.num_cars = Var(z.plants, z.centers, domain=NonNegativeIntegers)

z.res1 = ConstraintList()
for p in z.plants:
    z.res1.add(sum(z.num_cars[p, c] for c in z.centers) == z.capacity[p])

z.res2 = ConstraintList()
for c in z.centers:
    z.res2.add(sum(z.num_cars[p, c] for p in z.plants) == z.demand[c])

z.obj = Objective(expr=sum(sum(z.cost[p, c] * z.num_cars[p, c] for c in z.centers) for p in z.plants))

SolverFactory('glpk').solve(z)

z.display()
