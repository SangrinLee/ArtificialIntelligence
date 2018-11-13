# -*- coding: utf-8 -*-
class InferPair:

    def __init__(self, ipFacts,ipRule):
            self.name = ""       
            self.fact = ipFacts
            self.rule = ipRule
            
    def setName(self, name):
        self.name=name
        
    def __repr__(self):
        """Returns a string representation of the Player."""
        return str(self.name)+" Rule: "+ str(self.rule)+" Fact: "+str(self.fact)