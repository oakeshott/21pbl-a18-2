import networkx as nx
import pulp
import cplex

filename = "data/network.gml"
G = nx.read_gml(filename)

print("b_i:", nx.get_node_attributes(G, "b"))
print("u_{i,j}:", nx.get_edge_attributes(G, "u"))
print("c_{i,j}:", nx.get_edge_attributes(G, "c"))

# Formulation
problem = pulp.LpProblem("Minimum cost flow problem", pulp.LpMinimize)

x = {}
for i, j in G.edges():
    x[i,j] = pulp.LpVariable("x_{:},{:}".format(i, j), lowBound=0)
    # x[i,j] = pulp.LpVariable("x_{:},{:}".format(i, j), 0, 1, pulp.LpBinary) # in case of an ILP

# Objective function
problem += pulp.lpSum(G[i][j]["c"] * x[i,j] for i, j in G.edges())

# Subject to
for i, j in G.edges():
    u_ij = G[i][j]["u"]
    problem += x[i,j] <= u_ij, "capacity_constraint_of_link_{:},{:}".format(i,j)

for i in G.nodes():
    b_i = G.nodes()[i]["b"]
    problem += pulp.lpSum(x[i,j] for j in G.neighbors(i) if (i, j) in x.keys()) - pulp.lpSum(x[j,i] for j in G.neighbors(i) if (j, i) in x.keys()) == b_i, "flow_constraint_of_node_{:}".format(i)

print(pulp)

filename = "minimum_cost_flow_problem.lp"
# export LP file
problem.writeLP(filename)
# load LP file
cpx = cplex.Cplex(filename)

# CPLEX parameters
cpx.parameters.threads = 32
cpx.parameters.mip.tolerances.mipgap.set(0)
cpx.parameters.mip.tolerances.absmipgap.set(0)

# Solve Minimum cost flow problem
cpx.solve()

status = cpx.solution.get_status()
# Check whether the LP is solved or not
if status == 1: # status == 101 in case of ILP
    print("Status:", cpx.solution.status[status], "Objective value:", cpx.solution.get_objective_value())
    for name, value in zip(cpx.variables.get_names(), cpx.solution.get_values()):
        print(name, value)

