# -*- coding: utf-8 -*-
class Rule:
    
    #    def __init__(self, factName, factInfo, factSupports, factSupportedBy, factAsserted=False):
    def __init__(self, ruleName, ruleInfo, ruleAsserted=False):
            self.name = ruleName
            self.info = ruleInfo
            self.LHS = ruleInfo[0]
            self.RHS = ruleInfo[1]
            
            self.Asserted=ruleAsserted
            
            self.facts_supports = []
            self.rules_supports = []
            self.supportedBy = []
            
            
    def __repr__(self):       
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
   
    #Note: predIndex start from 1     
    def getPredicate(self, predIndex):
        LHS_len=len(self.info[0])
        
        if predIndex>LHS_len:
            return False
        #Get LHS of rule=> get coresponding element => get predicate 
        return self.info[0][predIndex-1][0]
        
#        if len(self.info[0])>0:
#            #Get LHS of rule=> get first element => getpredicate 
#            return self.info[0][0][0]
#        else:
#            return False
    
    #Check if the assumption has three elements
    def isThreeEleAssump(self,assump):
        if len(assump)==3:
            return True
        else:
            return False
        
    #Note: assumIndex start from 1         
    def getAssumption(self, assumIndex):
        LHS_len=len(self.info[0])
        if assumIndex>LHS_len:
            return False
        assump=self.info[0][assumIndex-1]
#        is3Assum=
        return assump,self.isThreeEleAssump(assump)
    def getStatement(self):
        return self.info
       
        