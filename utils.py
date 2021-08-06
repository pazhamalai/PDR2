from z3 import *

t_val, f_val = Bools('t_val f_val')  # two variables representing true and false


def convert_clauses(clause, this_state, next_state):
    temp_clause = substitute(clause, (this_state[0], next_state[0]))
    for i in range(1, len(this_state)):
        temp_clause = substitute(temp_clause, (this_state[i], next_state[i]))

    return temp_clause


# Returns all the satisfying instances in a list.
# Each element in the list will be an array representing a sat solution
# Each item in the array can be True or False or the variable itself [don't care variable]
def get_all_satisfying_instances(solver, variables, *assumptions):
    sat_instances = []
    while solver.check(assumptions) != unsat:
        m = solver.model()
        sat_instance = get_satisfying_instance(variables, m)
        sat_instances.append(sat_instance)

        clause_for_instance = get_clause_to_avoid_instance(variables, m)
        if len(assumptions) != 0:
            solver.add(Implies(assumptions, clause_for_instance))
        else:
            solver.add(clause_for_instance)

    return sat_instances


# Returns an array of size len(variables)
# Each element in array can be True, False or the variable itself
def get_satisfying_instance(variables, m):
    return [m.evaluate(variables[i]) for i in range(0, len(variables))]


# Returns a clause that you can add it to Z3, so it will avoid this particular sat instance
def get_clause_to_avoid_instance(variables, model):
    temp_clauses = [model.evaluate(variables[i]) == variables[i] for i in range(0, len(variables))]
    return Not(And(temp_clauses))
