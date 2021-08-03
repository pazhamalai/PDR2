import FrameManager
from utils import convert_clauses
from z3 import *


def extend_frontier(model, k):
    FrameManager.add_clause_to_frames(k + 1, model.property_formula)
    solver = FrameManager.solver

    solver.push()
    Fk = FrameManager.frame_variables[k]
    temp_formula = Not(model.property_formula)
    temp_formula = convert_clauses(temp_formula, model.variables, model.next_state_variables)

    solver.add(Implies(Fk, model.transition_formula))
    solver.add(Implies(Fk, temp_formula))

    while solver.check(Fk) != unsat:
        m = solver.model()
        sat_instance = get_satisfying_instance(model.variables, m)
        # removeCTL(model, sat_instance, k)
        solver.add(Implies(Fk, Not(sat_instance)))

    solver.pop()


def get_satisfying_instance(variables, m):
    return [m.evaluate(variables[i], model_completion=True) == variables[i] for i in range(0, len(variables) + 1)]
