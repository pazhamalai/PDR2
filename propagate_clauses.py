from z3 import *
from FrameManager import frame_clauses, frame_variables, add_clause_to_frames, solver
from utils import convert_clauses


def propagate_clauses(model, k):
    for i in range(1, k+1):
        for c in frame_clauses[i]:
            n_c_prime = Not(convert_clauses(c, model.variables, model.next_state_variables))
            temp = And(frame_variables[i], model.transition_formula, n_c_prime)
            solver.push()
            solver.add(temp)
            check_sat = solver.check()
            solver.pop()
            if check_sat == unsat:
                add_clause_to_frames(i+1, c)
