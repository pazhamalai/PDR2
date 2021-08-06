from z3 import *
from utils import convert_clauses,star

solver = Solver()
# solver.add((And(star,False)) == False)
# solver.add((And(star,True)) == star)
# solver.add((And(star,star)) == star)
# solver.add((Or(star,False)) == star)
# solver.add((Or(star,True)) == True)
# solver.add((Or(star,star)) == star)
# solver.add(Not(star) == star)

from Model import Model
#gets two clauses s and t and returns a new clause t_prime after doing ternary sim on t
def ternary_sim(model,s,t):
    vars = model.variables.copy()
    trans_func = model.transition_formula
    new_vars = vars.copy
    s_next_vars = convert_clauses(s,vars,model.next_state_variables)
    solver.push()
    solver.add(And(t, s_next_vars, trans_func))
    check_sat = solver.check()
    solver.pop
    if check_sat == sat:
        for i in range(0,len(vars)):
            solver.push()
            solver.add(And(t,s_next_vars,trans_func))
            if solver.check() == sat:
                solver.pop()
                change_vars = new_vars.copy()
                change_vars[i] = Not(new_vars[i])
                temp_t = convert_clauses(t,new_vars,)

    return t_prime







