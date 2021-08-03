class Model:
    def __init__(self, variables, next_state_variables, transition_formula, initial_states_formula, property_formula):
        self.variables = variables
        self.next_state_variables = next_state_variables
        self.transition_formula = transition_formula
        self.initial_states_formula = initial_states_formula
        self.property_formula = property_formula
