from z3 import *
from InputModel import InputModel


def example_1():
    # example for testing(example done in slide PDR intro),unsat example
    s1, s2, s3 = Bools("s1 s2 s3")
    _s1, _s2, _s3 = Bools('_s1 _s2 _s3')
    variables = [s1, s2, s3]
    next_state_variables = [_s1, _s2, _s3]

    transition_formula = Or(And(Not(s1), Not(s2), s3, Not(_s1), _s2, Not(_s3)),
                            And(Not(s1), s2, Not(s3), Not(_s1), _s2, _s3),
                            And(Not(s1), s2, s3, Not(_s1), _s2, _s3),
                            And(Not(s1), s2, s3, _s1, Not(_s2), Not(_s3)),
                            And(s1, Not(s2), Not(s3), _s1, Not(_s2), _s3),
                            And(s1, Not(s2), s3, _s1, Not(_s2), _s3),
                            And(s1, Not(s2), s3, _s1, _s2, Not(_s3)),
                            And(s1, s2, Not(s3), _s1, _s2, Not(_s3)),
                            And(s1, s2, Not(s3), _s1, _s2, _s3),
                            And(s1, s2, s3, _s1, _s2, _s3),
                            And(Not(s1), Not(s2), Not(s3), Not(_s1), Not(_s2), Not(_s3)))
    initial_state_formula = And(Not(s1), Not(s2), s3)
    property_formula = And(Or(s1, s2, s3), Or(Not(s1), Not(s2), Not(s3)))
    model = InputModel(variables, next_state_variables, transition_formula, initial_state_formula, property_formula)
    return model


def example_2():

    s1, s2, s3 = Bools("s1 s2 s3")
    _s1, _s2, _s3 = Bools('_s1 _s2 _s3')
    variables = [s1, s2, s3]
    next_state_variables = [_s1, _s2, _s3]

    # (0, 0, 0) is the initial state
    initial_state_formula = And(Not(s1), Not(s2), Not(s3))

    # the initial state s0 will loop itself
    initial_loop = And(Not(s1), Not(s2), Not(s3), Not(_s1), Not(_s2), Not(_s3))

    # State s8 will loop itself
    final_loop = And(s1, s2, s3, _s1, _s2, _s3)

    # Every other state will have transition to s8
    remaining_transitions = And(Or(s1, s2, s3), Or(Not(s1), Not(s2), Not(s3)), And(_s1, _s2, _s3))

    transition_relation = Or(initial_loop, final_loop, remaining_transitions)

    # False only at s8
    property_formula = Or(Not(s1), Not(s2), Not(s3))
    model = InputModel(variables, next_state_variables, transition_relation, initial_state_formula, property_formula)
    return model


def get_example():
    return example_2()
