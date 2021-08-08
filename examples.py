from main import pdr_algo
from InputModel import InputModel
#example for testing(example done in slide PDR intro),unsat example
variables = [Bool("s1"), Bool("s2"), Bool("s3")]
next_state_variables = [Bool("_s1"), Bool("_s2"), Bool("_s3")]
s1, s2, s3 = Bools("s1 s2 s3")
_s1, _s2, _s3 = Bools('_s1 _s2 _s3')
transition_formula = Or(And(Not(s1),Not(s2),s3,Not(_s1),_s2,Not(_s3)),
    And(Not(s1),s2,Not(s3),Not(_s1),_s2,_s3),
    And(Not(s1),s2,s3,Not(_s1),_s2,_s3),
    And(Not(s1),s2,s3,_s1,Not(_s2),Not(_s3)),
    And(s1,Not(s2),Not(s3),_s1,Not(_s2),_s3),
    And(s1,Not(s2),s3,_s1,Not(_s2),_s3),
    And(s1,Not(s2),s3,_s1,_s2,Not(_s3)),
    And(s1,s2,Not(s3),_s1,_s2,Not(_s3)),
    And(s1,s2,Not(s3),_s1,_s2,_s3),
    And(s1,s2,s3,_s1,_s2,_s3),
    And(Not(s1),Not(s2),Not(s3),Not(_s1),Not(_s2),Not(_s3)))
initial_state_formula = And(Not(s1),Not(s2),s3)
property_formula = And(Or(s1,s2,s3),Or(Not(s1),Not(s2),Not(s3)))
model = InputModel(variables, next_state_variables, transition_formula, initial_state_formula, property_formula)

pdr_algo(model)