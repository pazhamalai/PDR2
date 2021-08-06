from z3 import *
#change made here
t_val , f_val = Bools('t_val f_val') #two variables representing true and false
def convert_clauses(clause, this_state, next_state):
    temp_clause = substitute(clause, (this_state[0], next_state[0]))
    for i in range(1, len(this_state)):
        temp_clause = substitute(temp_clause, (this_state[i], next_state[i]))

    return temp_clause


def get_all_satisfying_instances(solver, variables, *assumptions):
    sat_instances = []
    while solver.check(assumptions) != unsat:
        m = solver.model()
        sat_instance = get_satisfying_instance(variables, m)
        sat_instances.append(sat_instance)

        if assumptions is not None:
            solver.add(Implies(assumptions, Not(sat_instance)))
        else:
            solver.add(Not(sat_instance))

    return sat_instances


def get_satisfying_instance(variables, m):
    return [m.evaluate(variables[i], model_completion=True) == variables[i] for i in range(0, len(variables) + 1)]
