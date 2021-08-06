from z3 import *
from utils import star
#constant z3 variables for giving true and false values
solver = Solver()


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