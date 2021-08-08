from z3 import *
from utils import *

solver = Solver()

frame_variables = []
frame_clauses = []

# constant z3 variables for giving true and false values
solver.add(f_val == False)
solver.add(t_val == True)

def add_clause_to_frames(i, clause):
    if i >= len(frame_variables):
        frame_variables.append(Bool(str(i)))
        frame_clauses.append([])

    if not clause_present_in_frame(i, clause):
        solver.add(Implies(frame_variables[i], clause))
        frame_clauses[i].append(clause)


def clause_present_in_frame(i, clause):
    for frame_clause in frame_clauses[i]:

        # if eq(simplify(clause), simplify(frame_clause)):
        #     return True

        if check_equality(frame_clause, clause):
            return True

    return False


def check_equality(clause_1, clause_2):
    temp = Solver()
    temp.add(Not(clause_1 == clause_2))
    r = temp.check()
    return r == unsat


def print_frame_clauses():
    for frame in frame_clauses:
        print(frame)

def print_frames():
    for frame in frame_variables:
        print(frame)

#Checks if there exists distinct i,i+1 such that Frame i = Frame i+1
def check_frames_equality():
    F = [True for i in range(len(frame_variables))]
    for i in range(len(frame_variables)):
        # Extract states satisfying F_i
        for clause in frame_clauses[i]:
            F[i] = And(F[i],clause)

    #Check equality of any two consecutive frames
    for i in range(len(frame_variables) - 1):
        if check_equality(F[i],F[i+1]):
            print("\nFrames " + str(i) + " and " + str(i+1) + " are equal!")
            print("\nFrames " + str(i) + " = " + str(F[i]))
            print("\nFrames " + str(i+1) + " = " + str(F[i+1]))
            return True

    return False