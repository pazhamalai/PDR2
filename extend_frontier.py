import FrameManager
from utils import *
from z3 import *
from remove_cti import removeCTI


def extend_frontier(input_model, k):
    FrameManager.add_clause_to_frames(k + 1, input_model.property_formula)
    solver = FrameManager.solver
    print("\nExtending frontier (k = " + str(k) + ")")

    # Extract all instances that satisfy F_k ^ R ^ Not(p')
    solver.push()
    Fk = FrameManager.frame_variables[k]
    temp_formula = Not(input_model.property_formula)
    temp_formula = convert_clauses(temp_formula, input_model.variables, input_model.next_state_variables)
    solver.add(Implies(Fk, input_model.transition_formula))
    solver.add(Implies(Fk, temp_formula))
    check_sat = solver.check(Fk)
    sat_instances = []
    if check_sat == sat:
        solver.add(Fk)
        sat_instances = get_all_satisfying_instances(solver, input_model.variables + input_model.next_state_variables)
        print("SAT! Instances = " + str(sat_instances))
    else:
        print("UNSAT!")
    solver.pop()

    # print("Printing out sat_instances: ")
    for sat_instance in sat_instances:
        # print(sat_instance)
        removeCTI(input_model, sat_instance, k)
