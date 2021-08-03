from z3 import substitute


def convert_clauses(clause, this_state, next_state):
    temp_clause = substitute(clause, (this_state[0], next_state[0]))
    for i in range(1, len(this_state)):
        temp_clause = substitute(temp_clause, (this_state[i], next_state[i]))

    return temp_clause
