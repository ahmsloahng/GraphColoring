# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 19:52:47 2021

@author: Amlan Ghosh

"""
import pulp as plp

solver = plp.get_solver('CPLEX_CMD')

def math_model(input_data):

    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])    

    nodes = [str(i) for i in range(node_count)]

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))
    
    color = plp.LpProblem('GraphColor', sense = plp.LpMinimize)
    
    var_color = plp.LpVariable.dicts('Node', ((i) for i in nodes), lowBound = 0, upBound = node_count, cat = plp.LpInteger)
    
    var_totalColor = plp.LpVariable('Total', lowBound = 0, upBound = node_count, cat = plp.LpInteger)
    
    var_bin = plp.LpVariable.dicts('Bin', (i for i in range(len(edges))), cat = plp.LpBinary)
    
    color_restriction_1 = {(i): color.addConstraint(plp.LpConstraint(e = var_color[str(edges[i][0])] - var_color[str(edges[i][1])] + 2*node_count*var_bin[i] + 1 - 2*node_count,
                                                                     sense = plp.LpConstraintLE,
                                                                     rhs = 0,
                                                                     name = 'Edge1_'+str(i))) for i in range(len(edges))}
    
    color_restriction_2 = {(i): color.addConstraint(plp.LpConstraint(e = var_color[str(edges[i][0])] - var_color[str(edges[i][1])] + 2*node_count*var_bin[i] - 1,
                                                                 sense = plp.LpConstraintGE,
                                                                 rhs = 0,
                                                                 name = 'Edge2_'+str(i))) for i in range(len(edges))}
    
    max_color = {i: color.addConstraint(plp.LpConstraint(e = var_totalColor - var_color[i], 
                                                      sense = plp.LpConstraintGE,
                                                      rhs = 0,
                                                      name = 'Color_'+i)) for i in nodes}
    
    color += var_totalColor
    
    color.solve(solver)
    
    print (plp.LpStatus[color.status])
    
    print (color)
    
    solution = [0]*node_count
    for i in color.variables():
        if str(i.name)[:4] == 'Node':
            solution[int(float((i.name)[5:]))] = int(round(float(i.varValue),1))
    
    print (plp.value(color.objective))
    
    output_data = str(max(solution)+1) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))
    
    return output_data


