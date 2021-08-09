import FrameManager
from utils import *
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
        verify_s_not_in_initial_state(input_model, s)

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

        else:
            # Most of the time s' is same as s, since Z3 itself does generalization.
            # So we dont' block s' here.
            get_s_prime_unsat_core(instance, input_model, i)

        solver.pop()


def get_s_prime_unsat_core(instance, input_model, frame_index):
    # Create new solver with Implies(Fi, frame_clauses(i))
    temp_vars = [Bool("temp" + str(i)) for i in range(0, len(input_model.variables))]
    temp_solver = Solver()
    for clause in FrameManager.frame_clauses[frame_index]:
        temp_solver.add(clause)

    temp_solver.add(input_model.transition_formula)

    # Make Implies(temp[i], variables[i])
    # Or Make Implies(temp[i], Not(variables[i]))
    for i in range(0, len(instance)//2):
        if instance[i] == True:
            temp_solver.add(Implies(temp_vars[i], input_model.variables[i]))
        elif instance[i] == False:
            temp_solver.add(Implies(temp_vars[i], Not(input_model.variables[i])))

    # solver.check(temp1, temp2, ...)
    temp_solver.check(*temp_vars)
    core = temp_solver.unsat_core()

    new_instance = []
    for i in range(0, len(temp_vars)):
        if temp_vars[i] in core:
            new_instance.append(instance[i])
        else:
            new_instance.append(input_model.variables[i])

    for i in range(len(temp_vars), len(instance)):
        new_instance.append(instance[i])

    return extractSatisfyingStates(new_instance, input_model)


def verify_s_not_in_initial_state(input_model, s):
    solver = FrameManager.solver
    solver.push()
    solver.add(input_model.initial_states_formula)
    solver.add(s)
    check_sat = solver.check()
    solver.pop()
    if check_sat == sat:
        print("Model does not satisfy AG p")
        sys.exit()
