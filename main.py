from z3 import *
import FrameManager
from Model import Model
from propagate_clauses import propagate_clauses

variables = [Bool("x"), Bool("y"), Bool("z")]
next_state_variables = [Bool("_x"), Bool("_y"), Bool("_z")]

transition_formula = Or()
initial_state_formula = Or()
property_formula = And()

model = Model(variables, next_state_variables, transition_formula, initial_state_formula, property_formula)

x, y, z = Bools("x y z")
FrameManager.add_clause_to_frames(0, Or(x, y))
FrameManager.add_clause_to_frames(0, Or(x, y, z))
FrameManager.add_clause_to_frames(0, Or(z, x, y))
FrameManager.add_clause_to_frames(1, Or(x, y))
FrameManager.add_clause_to_frames(1, Or(x, y, z))
FrameManager.print_frame_clauses()

propagate_clauses(model, 1)
