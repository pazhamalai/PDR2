from z3 import *
from InputModel import InputModel
def get_example():
    # example for testing(example done in slide PDR intro),unsat example
    s1, s2, s3 = Bools("s1 s2 s3")
    _s1, _s2, _s3 = Bools('_s1 _s2 _s3')
    variables = [s1,s2,s3]
    next_state_variables = [_s1,_s2,_s3]

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


