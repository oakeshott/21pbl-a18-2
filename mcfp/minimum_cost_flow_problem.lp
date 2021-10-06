\* Minimum_cost_flow_problem *\
Minimize
OBJ: 3 x_0,1 + 7 x_0,2 + x_1,2 + 2 x_1,3 + 9 x_2,3 + x_2,4 + 7 x_3,4 + 8 x_3,5
 + 4 x_4,5
Subject To
capacity_constraint_of_link_0,1: x_0,1 <= 5
capacity_constraint_of_link_0,2: x_0,2 <= 2
capacity_constraint_of_link_1,2: x_1,2 <= 6
capacity_constraint_of_link_1,3: x_1,3 <= 4
capacity_constraint_of_link_2,3: x_2,3 <= 2
capacity_constraint_of_link_2,4: x_2,4 <= 3
capacity_constraint_of_link_3,4: x_3,4 <= 3
capacity_constraint_of_link_3,5: x_3,5 <= 1
capacity_constraint_of_link_4,5: x_4,5 <= 9
flow_constraint_of_node_0: x_0,1 + x_0,2 = 6
flow_constraint_of_node_1: - x_0,1 + x_1,2 + x_1,3 = 0
flow_constraint_of_node_2: - x_0,2 - x_1,2 + x_2,3 + x_2,4 = 0
flow_constraint_of_node_3: - x_1,3 - x_2,3 + x_3,4 + x_3,5 = 0
flow_constraint_of_node_4: - x_2,4 - x_3,4 + x_4,5 = 0
flow_constraint_of_node_5: - x_3,5 - x_4,5 = -6
End
