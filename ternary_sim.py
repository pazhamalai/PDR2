from z3 import *
from utils import convert_clauses, t_val, f_val

solver = Solver()
solver.add(t_val == True)
solver.add(f_val == False)


# solver.add((And(star,False)) == False)
# solver.add((And(star,True)) == star)
# solver.add((And(star,star)) == star)
# solver.add((Or(star,False)) == star)
# solver.add((Or(star,True)) == True)
# solver.add((Or(star,star)) == star)
# solver.add(Not(star) == star)

# gets two clauses s and t and returns a new clause t_prime after doing ternary sim on t
def ternary_sim(input_model, s, t):
    variables = input_model.variables.copy()
    trans_func = input_model.transition_formula
    new_vars = variables.copy()
    s_next_vars = convert_clauses(s, variables, input_model.next_state_variables)
    solver.push()
    solver.add(And(t, s_next_vars, trans_func))
    check_sat = solver.check()
    solver.pop()
    t_prime = t
    if check_sat == sat:
        for i in range(0, len(variables)):
            print("i:", i)
            solver.push()
            print(variables, new_vars)
            new_t = convert_clauses(t, variables, new_vars)
            solver.add(And(new_t, s_next_vars, trans_func))
            if solver.check() == sat:
                solver.pop()
                change_vars = new_vars.copy()
                change_vars[i] = Not(new_vars[i])
                temp_t = convert_clauses(t, variables, change_vars)
                solver.push()
                solver.add(And(temp_t, s_next_vars, trans_func))
                if (solver.check() == sat):
                    new_vars[i] = t_val
            solver.pop()
        t_prime = convert_clauses(t, variables, new_vars)
    return t_prime
