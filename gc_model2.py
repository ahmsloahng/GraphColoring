# -*- coding: utf-8 -*-
"""
Created on Sun Jul 11 20:20:42 2021

@author: Amlan
"""

from ortools.sat.python import cp_model

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
    
    model = cp_model.CpModel()
    var_nodes = [model.NewIntVar(0,node_count-1,'node_'+str(i)) for i in range(node_count)]
    var_color = model.IntVar(0,node_count-1,'color')
    for edge in edges:
        model.Add(var_nodes[edge[0]] <= var_color)
        model.Add(var_nodes[edge[1]] <= var_color)
        model.AddAllDifferent([var_nodes[edge[0]], var_nodes[edge[1]]])
    model.Minimize(var_color)
    
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL:
        solution = [0]*node_count
        for i in range(node_count):
            solution[i] = solver.Value(var_nodes[i])
    
    output_data = str(max(solution)+1) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))
    
    return output_data

