# -*- coding: utf-8 -*-
class Fact:
    """ A basic AI (or human) player """
#    HUMAN = 0
#    RANDOM = 1
#    MINIMAX = 2
#    ABPRUNE = 3
#    CUSTOM = 4
    
    #    def __init__(self, factName, factInfo, factSupports, factSupportedBy, factAsserted=False):
    def __init__(self, factName, factInfo, factAsserted=False):
            """Initialize a Player with a playerNum (1 or 2), playerType (one of
            the constants such as HUMAN), and a ply (default is 0)."""
            self.name = factName
            self.info = factInfo
            self.Asserted=factAsserted
            
            self.facts_supports = []
            self.rules_supports = []
            self.supportedBy = []
            
            
    def __repr__(self):
        """Returns a string representation of the Player."""
        return str(self.name)+" "+ str(self.info)
    
    def printCompleteComp(self):
        m_fact_supports='[%s]' % ', '.join(map(str, self.facts_supports))
        m_rule_supports='[%s]' % ', '.join(map(str, self.rules_supports))
        m_supported_by='[%s]' % ', '.join(map(str, self.supportedBy))
        print str(self.name)+" "+ str(self.info)
        print "Fact supports: "+m_fact_supports
        print "Rule supports: "+m_rule_supports
        print "Supported by: "+m_supported_by
        
    def addFactSupports(self,fact):
        self.facts_supports.append(fact)
        
    def addRuleSupports(self,rule):
        self.rules_supports.append(rule)
        
    def addSupportedBy(self,InferPair):
        self.supportedBy.append(InferPair)
        
    def setAssert(self, status):
        self.Asserted=status
        
    def getAssert(self):
        return self.Asserted
    
    def getStatement(self):
        return self.info