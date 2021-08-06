from z3 import *
import FrameManager
from Model import Model
from propagate_clauses import propagate_clauses


variables = [Bool("x"), Bool("y"), Bool("z")]
next_state_variables = [Bool("_x"), Bool("_y"), Bool("_z")]
x, y, z = Bools("x y z")
_x, _y, _z = Bools('_x _y _z')
transition_formula = And(x == _x, y == _y, z == _z)
initial_state_formula = And(x, y, z)
property_formula = And()

model = Model(variables, next_state_variables, transition_formula, initial_state_formula, property_formula)


# FrameManager.add_clause_to_frames(0, And(x, y))
FrameManager.add_clause_to_frames(0, And(x, y, z))
FrameManager.add_clause_to_frames(0, And(z, x, y))
# FrameManager.add_clause_to_frames(1, And(x, y))

FrameManager.add_clause_to_frames(1, And(Not(x), y, z))
FrameManager.print_frame_clauses()
print("After propagate clauses:")
propagate_clauses(model, 1)
FrameManager.print_frame_clauses()
FrameManager.print_frames()
#new code
#code for testing ternary sim
from ternary_sim import ternary_sim
transition_formula2 = And (x == _x)
model2 = Model(variables, next_state_variables, transition_formula2, initial_state_formula, property_formula)
s = And(x,y,Not(z))
t = And(x,y,z)
t_prime = ternary_sim(model2,s,t)
print(t_prime)
