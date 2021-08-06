from z3 import *
from FrameManager import frame_clauses, frame_variables, add_clause_to_frames, solver
from utils import convert_clauses


def propagate_clauses(input_model, k):
    for i in range(1, k+1):
        for c in frame_clauses[i]:
            n_c_prime = Not(convert_clauses(c, input_model.variables, input_model.next_state_variables))
            solver.push()
            solver.add(Implies(frame_variables[i], input_model.transition_formula))
            solver.add(Implies(frame_variables[i],n_c_prime))
            check_sat = solver.check(frame_variables[i])
            solver.pop()
            if check_sat == unsat:
                add_clause_to_frames(i+1, c)
