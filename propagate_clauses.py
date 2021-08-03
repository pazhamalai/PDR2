from z3 import *
from FrameManager import frame_clauses,frame_variables,add_clause_to_frames,solver
from main import transition_formula,variables,next_state_variables


def convert_clauses(clause,this_state,next_state):
    temp_clause = substitute(clause, (this_state[0],next_state[0]))
    for i in range(1, len(this_state)):
        temp_clause = substitute(temp_clause, (this_state[i],next_state[i]))
    return temp_clause


def propagate_clauses(k):
    for i in range(1,k+1):
        for c in frame_clauses[i]:
            n_c_prime =Not(convert_clauses(c,variables,next_state_variables))
            temp = And(frame_variables[i],transition_formula,n_c_prime)
            solver.push()
            solver.add(temp)
            check_sat = solver.check()
            solver.pop()
            if check_sat == unsat:
                add_clause_to_frames(i+1,c)








