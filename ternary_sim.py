from z3 import *
from utils import convert_clauses,star

solver = Solver()
solver.add((And(star,False)) == False)
solver.add((And(star,True)) == star)
solver.add((And(star,star)) == star)
solver.add((Or(star,False)) == star)
solver.add((Or(star,True)) == True)
solver.add((Or(star,star)) == star)
# solver.add(Not(star) == star)

from Model import Model
#gets two clauses s and t and returns a new clause t_prime after doing ternary sim on t
def ternary_sim(model,s,t):
    print("init check:",solver.check())
    vars = model.variables.copy()
    var_length = len(vars)
    transition_func = model.transition_formula
    new_vars = model.variables.copy()
    #converting the clause s for checcking transition formula sat
    s_nxt_state = convert_clauses(s,vars,model.next_state_variables)
    #new t_prime
    solver.add(And(t,transition_func,s_nxt_state))
    for i in range(0,var_length):
        solver.push()
        solver.add(vars[i] == star)
        print(solver)
        print("Sat check 1:",solver.check())
        if solver.check() == sat:
            new_vars[i] = star
        else:
            solver.pop()


    print(new_vars)
    t_prime = convert_clauses(t,model.variables,new_vars)
    print(t_prime)
    return t_prime







