import FrameManager
from utils import *
import sys
from z3 import *
from ternary_sim import ternary_sim
from queue import PriorityQueue
tempSolver = Solver()

def removeCTI(input_model, sat_instance, k):
    print("\nInside RemoveCTI with k :", k)
    solver = FrameManager.solver

    # Add current satisfying instance to queue
    q = PriorityQueue()
    # We put -k since we want k to be higher priority while q is a min-priority queue
    q.put((-k, sat_instance))

    while not q.empty():
        (i, instance) = q.get()
        i = -i
        print("Removing i = " + str(i) + " instance = ")
        s = extractSatisfyingStates(instance, input_model)
        print(s)
        _s = convert_clauses(s, input_model.variables, input_model.next_state_variables)
        # Check if S_0 ^ s is SAT
        solver.push()
        solver.add(input_model.initial_states_formula)
        solver.add(s)
        check_sat = solver.check()
        solver.pop()
        if check_sat == sat:
            print("Model does not satisfy AG p")
            sys.exit()

        # Block s from all frames until i
        # solver.push()
        for l in range(0, i + 1):
            FrameManager.add_clause_to_frames(l, Not(s))

        # Check F_i ^ R ^ not(s) ^ s' is SAT
        solver.push()
        solver.add(Implies(FrameManager.frame_variables[i], input_model.transition_formula))
        solver.add(Implies(FrameManager.frame_variables[i], _s))
        check_sat = solver.check(FrameManager.frame_variables[i])

        if check_sat == sat:
            # print("sat yes 1")
            # Get sat instance and from that, get t
            m = solver.model()
            instanceT = get_satisfying_instance(input_model.variables + input_model.next_state_variables, m)
            t = extractSatisfyingStates(instanceT, input_model)
            t_prime = ternary_sim(input_model, s, t)

            tempSolver.push()
            tempSolver.add(t_val == True)
            tempSolver.add(f_val == False)
            tempSolver.add(t_prime)
            # print("Ternary sim formula = " + str(t_prime))
            # print("temp solver:" ,tempSolver)
            if (tempSolver.check() == sat):
                # print("sat yes 2")
                m = tempSolver.model()
                instanceTPrime = get_satisfying_instance(input_model.variables + input_model.next_state_variables, m)
                # Add t to Queue (equivalent to calling removeCTI with parameters t, (i-1))
                q.put((1 - i, instanceTPrime))
            tempSolver.pop()

        # else:
        #     solver.pop()
        #     solver.pop()
        #     solver.push()
        #     solver.add(Implies(FrameManager.frame_variables[i], input_model.transition_formula))
        #     solver.add(Implies(FrameManager.frame_variables[i],_s))
        #     solver.add(FrameManager.frame_variables[i])
        #     s_list = extractListOfClausesInFormula(instance, input_model)
        #     print("S_list = " + str(s_list))
        #     print(solver.check())
        #     print("unsat_core = ")
        #     k = solver.check(*s_list)
        #     print(solver.unsat_core())
        #     print(k)
        #     # solver.pop()

        solver.pop()
