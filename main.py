from z3 import *
import FrameManager
from InputModel import InputModel
from propagate_clauses import propagate_clauses
from utils import *
from ternary_sim import ternary_sim
#pdr algorithm
def pdr_algo(input_model):
    FrameManager.solver.push()
    FrameManager.solver.add(input_model.initial_state_formula)
    FrameManager.solver.add(Not(input_model.property_formula))
    check_sat = FrameManager.solver.check()
    FrameManager.solver.pop()
    if check_sat == sat:
        print("Model does not satisfy AG p")

    else:
        k = 0
        FrameManager.add_clause_to_frames(0, input_model.initial_state_formula)
        while True:
            extend_frontier(input_model, k)
            propagate_clauses(model, k)
            if FrameManager.check_frames_equality():
                print("Model satisfies AG p")
                break
            k = k + 1





