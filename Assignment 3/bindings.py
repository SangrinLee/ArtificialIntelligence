# -*- coding: utf-8 -*-
# Binding
# A single binding is a pair of variable/value
# A set or list of bindings defines the constraints on match between two statements
# Once defined, you can add a new binding pair, get the value associated with a variable
# and test to see if a variable matches a constant. 
# If a variable is bound then it will only match the same constant
# If it is unbound, then it will match and the binding is added

class bindings:
	def __init__(self):
		self.bindings = {}
		self.pretty = []
	def add_binding(self, variable, value):
		self.bindings[variable] = value
		self.pretty.append((variable.upper(), value))
	def binding_value(self, variable):
		if variable in self.bindings.keys():
			return self.bindings[variable] 
		return False
	def test_and_bind(self, variable, value):
		if variable in self.bindings.keys():
			if value == self.bindings[variable]:
				return True
			else:
				return False 
		self.add_binding(variable, value)
		return True		
	def __str__(self):
		return str(self.pretty)