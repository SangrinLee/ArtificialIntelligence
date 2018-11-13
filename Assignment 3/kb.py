# -*- coding: utf-8 -*-
from fact import *
from rule import *
from inferpair import *

class KnowledgeBase:

    #    def __init__(self, factName, factInfo, factSupports, factSupportedBy, factAsserted=False):
    def __init__(self):
            self.facts = []
            self.rules = []
            self.factIndex=1
            self.ruleIndex=1
            self.ipIndx=1

    def __repr__(self):
        """Returns a string representation of the Player."""
        return str(self.facts)+" "+ str(self.rules)+" factIndex: "+str(self.factIndex-1)+" ruleIndex: "+str(self.ruleIndex-1)
    
    def addFact(self,fact_info, isAsserted):
        aFact=Fact("Fact"+str(self.factIndex),fact_info,isAsserted)
        self.facts.append(aFact)
        self.factIndex+=1
    
    def addFactwithSupportedBy(self,fact_info,ip):
        aFact=Fact("Fact"+str(self.factIndex),fact_info)
        ip.setName("InferPair "+str(self.ipIndx))
        aFact.addSupportedBy(ip)
        self.ipIndx+=1
        self.facts.append(aFact)
        self.factIndex+=1
#        return aFact
        
    def remove_fact(self, fact):
        self.facts.remove(fact)


    def addRule(self,rule, isAsserted):
        aRule=Rule("Rule"+str(self.ruleIndex),rule,isAsserted)
        self.rules.append(aRule)
        self.ruleIndex+=1
        
    def addRulewithSupportedBy(self,rule_info,ip):
        aRule=Rule("Rule"+str(self.ruleIndex),rule_info)
        ip.setName("InferPair "+str(self.ipIndx))
        aRule.addSupportedBy(ip)
        self.ipIndx+=1
        self.rules.append(aRule)
        self.ruleIndex+=1
#        return aRule    
    def remove_rule(self, rule):
        self.rules.remove(rule)
        
        
    def getFacts(self):
        return self.facts
    
    def getRules(self):
        return self.rules
    
    
    
