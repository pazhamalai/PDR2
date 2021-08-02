from z3 import *
import FrameManager

variables = []
next_state_variables = []

transition_formula = Or()
initial_state_formula = Or()
property_formula = And()

x, y, z = Bools("x y z")
FrameManager.add_clause_to_frames(0, Or(x, y))
FrameManager.add_clause_to_frames(0, Or(x, y, z))
FrameManager.add_clause_to_frames(0, Or(z, x, y))
FrameManager.print_frame_clauses()

