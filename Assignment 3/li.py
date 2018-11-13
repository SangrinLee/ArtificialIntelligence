# -*- coding: utf-8 -*-
from read import *
from fact import *
from rule import *
from inferpair import *
from kb import *
from copy import *
from enums import *
from bindings import *

#Helper functions
def varq(ele):
    if '?' in ele:
        return True
    return False


def printAListOfListsBindings(given):
    index=1
    for listofbindings in given:
        print "Binding List "+str(index)
#        for bindings in listofbindings:
#            print bindings
        prinListOfBindings(listofbindings)
        print ""

def prinListOfBindings(given):
    index=1
    
    for bindings in given:
        print "Binding "+str(index)
        print bindings
        index+=1
#        print ""

    
#print varq("ab")

# Match tests two elements against each the to see if they match.
# Constants match each other
# Unbound variables match constants and then are bound to them
# Bound variables match against a constant if they are bound to the same constant
def match(statement1, statement2, mybindings = None):
    if mybindings == None:
        mybindings = bindings()

#def match(statement1, statement2, bindings = bindings()):
    
    #Not same length
    if len(statement1) != len(statement2):
        return False
   #First statement is empty
    if len(statement1) == 0:
        return mybindings
    #Note: varq could be vars
    if varq(statement2[0]):    
        if not mybindings.test_and_bind(statement2[0], statement1[0]):
            return False
    elif statement1[0] != statement2[0]:
        return False
    return match(statement1[1:], statement2[1:], mybindings)

#print match(['isa', 'cube', 'block'],['isa', '?x', 'block'])


glb_kb=KnowledgeBase()

facts, rules= read_tokenize("statements.txt")


#Initial Stage
#Add all current facts
for fact in facts:
#    addFact(glb_kb,fact)
    glb_kb.addFact(fact,True)

#Add all current rules
for rule in rules:
#    addRule(glb_kb,rule)
    glb_kb.addRule(rule,True)

print glb_kb 

def ask(kb,statement):
    aListOfBindingLists=[]

    for fact in kb.getFacts():
        fact_statement=fact.getStatement()
        match_result=match(fact_statement,statement,bindings())
#        print fact
#        print match_result
        #Add only if it matches
        if not match_result:
#            print "No matchs for "+str(fact_statement)
            continue
        else:
            aListOfBindingLists.append(match_result)

    return aListOfBindingLists

#print ""
#print "Ask test 1"
#aStatement =   ['isa', '?X', 'block']
#aListofBindingLists=ask(glb_kb,aStatement)
#prinListOfBindings(aListofBindingLists)
#print ""


def instantiate(statement,aListOfBindings):
    statementCopy=deepcopy(statement)   

    for index, ele in enumerate(statement):
        if varq(ele):
            bindingVal=aListOfBindings.binding_value(ele)
            if bindingVal:
                statementCopy[index]=aListOfBindings.binding_value(ele)
    return statementCopy

#aStatement =   ['isa', '?X', 'block']
#
#print ""
#print ("Instantiate Testing 2")
#for binding in aListofBindingLists:
#    print instantiate(aStatement,binding)
#print ""



def askPlus(alistOfStatement):
    aListOfBindingList=[]
    #Case 1: If the list of statement if empty, return False
    if len(alistOfStatement)==0:
        return False
    
    #Case 2 :alistOfStatement only has one statement
    if len(alistOfStatement)==1:
        ask_rsts=ask(glb_kb,alistOfStatement[0])
        
        for rst in ask_rsts:
            aListOfBindingList.append([rst])
        return aListOfBindingList
    
    #Case 3: alistOfStatement has more than one statement
  
      
    aListOfMatchResult=[]
    
    for fact in glb_kb.getFacts(): #TODO: might revise glb_kb to kb
        fact_statement=fact.getStatement()
        match_result=match(fact_statement,alistOfStatement[0],bindings())
        if not match_result:
            continue
        else:
            aListOfMatchResult.append(match_result)
#    print aListOfMatchResult
   
    #If no matches
    if len(aListOfMatchResult)==0:
        return False
    
    for match_result in aListOfMatchResult: 
        bindingList=[]

        #If the first statement has match, we delete it and instantiate its bindings
        alistOfStatement_copy=deepcopy(alistOfStatement)
        
#        bindingList.append(instantiate(alistOfStatement_copy[0],match_result))
        bindingList.append(match_result)

#        print  bindingList[0]
        del alistOfStatement_copy[0]
#        print alistOfStatement_copy
        instantiate_list=[]
        
        #Instatitate the bindings with statements
        for statement in alistOfStatement_copy:
            instantiatedRst=instantiate(statement,match_result)
            instantiate_list.append(instantiatedRst)
        
#        print instantiate_list
        statementListLen=len(alistOfStatement_copy)
        #Construct instantitated list of statement
        for index in range(statementListLen):
            alistOfStatement_copy[index]=instantiate_list[index]
#        print alistOfStatement_copy
        
        rst=askPlus_bindinglist(alistOfStatement_copy,bindingList)    
        
        if not rst:
            continue
        else:
            aListOfBindingList.append(bindingList)
            
    
    return aListOfBindingList
            

def askPlus_bindinglist(alistOfStatement, bindinglist):
    
#    if len(alistOfStatement)==0:
#        return bindinglist
    
    aListOfMatchResult=[]
    for fact in glb_kb.getFacts(): #TODO: might revise glb_kb to kb
        fact_statement=fact.getStatement()
        match_result=match(fact_statement,alistOfStatement[0],bindings())
        if not match_result:
            continue
        else:
            aListOfMatchResult.append(match_result)
    
#    print aListOfMatchResult[0]
   
    #If no matches
    if len(aListOfMatchResult)==0:
        return False
    
    for match_result in aListOfMatchResult:       

        #If the first statement has match, we delete it and instantiate its bindings
        alistOfStatement_copy=deepcopy(alistOfStatement)
        
#        bindinglist.append(alistOfStatement_copy[0])
        bindinglist.append(match_result)
        
#        print bindinglist[1]
        del alistOfStatement_copy[0]
        
        instantiate_list=[]
        
        #Instatitate the bindings with statements
        for statement in alistOfStatement_copy:
            instantiatedRst=instantiate(statement,match_result)
            instantiate_list.append(instantiatedRst)
        
        statementListLen=len(alistOfStatement_copy)
        #Construct instantitated list of statement
        for index in range(statementListLen):
            alistOfStatement_copy[index]=instantiate_list[index]
        
        #If no more statement left return a list of binding list directly
        if len(alistOfStatement_copy)==0:
            return bindinglist
        
        #Else keep recrusive match
        rst=askPlus_bindinglist(alistOfStatement_copy,bindinglist)  
        
        if not rst:
            return False
    


        
#aLstState=[['inst', '?x', '?y'],['isa', '?y', '?z']]
#print ""
#print "Ask + testing 1:"
#askPlsRst= askPlus(aLstState)
#printAListOfListsBindings(askPlsRst)
#print ""
#
#aLstState=[aStatement]
#print ""
#print "Ask + testing 2:"
#askPlsRst= askPlus(aLstState)
#printAListOfListsBindings(askPlsRst)
#print ""

def findFact(statement):
    for theFact in glb_kb.facts:  
        if theFact.getStatement()==statement:
            return theFact
    return False


def findRule(statement):
    for theRule in glb_kb.rules:  
        if theRule.getStatement()==statement:
            return theRule
    return False

#
#aStatement=['isa', 'cube', 'block']
#findFact(aStatement).Asserted=True
#print findFact(aStatement).Asserted

def removeRuleFirstState(rule_info):
    rule_info_copy=deepcopy(rule_info)
    del rule_info_copy[0][0]
    return rule_info_copy

#print glb_kb.rules[0]
#print removeRuleFirstState(glb_kb.rules[0].info)

def instantiateRule(bindings,rule_info):
    rule_info_copy=deepcopy(rule_info)

    #Instantiate LHS
    for statement_index, statement in enumerate(rule_info[0]):
       rule_info_copy[0][statement_index]= instantiate(statement,bindings)
       
    #Instantiate RHS   
    #Since tuple is not immutable, need recontruct
    tuple_copy = list(rule_info_copy)
    tuple_copy[1] = instantiate(rule_info[1],bindings)
    updt_tuple = tuple(tuple_copy)
#    rule_info_copy[1]= instantiate(rule_info[1],bindings)
    return updt_tuple
    

#print "Instantiate Test 1"
#print glb_kb.rules[0]
#instan_bindings=match(['inst', 'A', 'B'],['inst', '?x', '?y'],bindings())

#print instan_bindings
##print bindings.binding_value('?x')
##print removeRuleFirstState(glb_kb.rules[0].info)
#print instantiateRule(instan_bindings,glb_kb.rules[0].info)        
#print ""


#Check if the give input is a rule
def isRule(given):
    return isinstance(given[0][0], list)

#print ""
#print "isRule test"
#print isRule(([['inst', '?x', '?y'], ['isa', '?y', '?z']], ['inst', '?x', '?z']))
#print isRule(['inst', '?x', '?y'])


def kb_assert(statement):

    if isRule(statement):
        assertRule(statement)
    else:
        assertFact(statement)
        
    #Infer new facts and rules
    for fact in glb_kb.facts:
        for rule in glb_kb.rules:
            infer(fact,rule)
    print glb_kb

def assertRule(rule_info):
    find_rule_rst=findRule(rule_info)

    #If not in KB, Add the give fact to KB
    if not find_rule_rst:
        glb_kb.addRule(find_rule_rst,True)
    #If in the KB, assert this fact
    else:
        find_rule_rst.Asserted=True
    #TODO: Need infer all new facts and rules  
    
    
    
def assertFact(fact_statement):
    find_fact_rst=findFact(fact_statement)

    #If not in KB, Add the give fact to KB
    if not find_fact_rst:
        glb_kb.addFact(fact_statement,True)
    #If in the KB, assert this fact
    else:
        find_fact_rst.Asserted=True
    #TODO: Need infer all new facts and rules



def why(fact_statement):
     print ("===== Inside why =====")
     print (fact_statement)
     find_fact_rst=findFact(fact_statement)
     
     # Fact is not existed in KB
     if not find_fact_rst:
         print "Fact is not found in KB"
         return False

     find_rule_rst = find_fact_rst.rules_supports     
     #Rule is not existed in KB
     if not find_rule_rst:
         print "Rule is not found in KB"
         return False

     #If the fact has no suported by
     if len(find_fact_rst.supportedBy)==0:
         #TODO: Check if it is necessary, as if a fact has no supported by
         #it must be asserted
         if find_fact_rst.Asserted:
             print "The fact : "+str(find_fact_rst)+" is asserted"

         else:
             print "The given fact is not asserted"
#         return 
     else:
         for supported_by in find_fact_rst.supportedBy:
             print supported_by
             print ""
             why(supported_by.fact.info)
             
     # print ("===== check 1 =====")
     # for i,j in enumerate(find_fact_rst):
     	# print (i)
     # print (fact_statement)
     # print (find_fact_rst.rules_supports)

     # print (find_fact_rst.rules_supports)
     # if find_fact_rst == False:
     # 	return
     # find_rule_rst = find_fact_rst.rules_supports
     # print ("===== check 2 =====\n")
     # find_rule_rst=findRule(find_fact_rst.rules_supports)

#      print (find_rule_rst)


     
     #If the rule has no suported by
     if len(find_rule_rst)==1:
         #TODO: Check if it is necessary, as if a rule has no supported by
         #it must be asserted
         if find_rule_rst:
             print "The rule : " + str(find_rule_rst) + " is asserted"

         else:
             print "The given rule is not asserted"
#         return 
     else:
         for index, support in enumerate(find_rule_rst):
             print support
             print ""
             # why(supported_by)




print ("-----")             
print glb_kb

print ""         

# print ""   
# print glb_kb
#Input: Fact (statement is an attribute of a Fact), Rule
#Here we keep the fact and rule original asserted status
def info_infer(fact_info, rule_info):
#    print fact_info
#    print rule_info
   
    find_fact_rst=findFact(fact_info)
    find_rule_rst=findRule(rule_info)


    #If not in KB, Add the give fact to KB
    if not find_fact_rst:
        glb_kb.addFact(fact_info,False)
    
    #If not in KB, Add the give rule to KB
    if not find_rule_rst:
         glb_kb.addRule(rule_info,False)


           
# =============================================================================
#     #If not in KB, Add the give fact to KB
#     if not find_fact_rst:
#         glb_kb.addFact(fact_info,True)
#     #If in the KB, assert this fact
#     else:
#         find_fact_rst.Asserted=True
#     
#     #If not in KB, Add the give rule to KB
#     if not find_rule_rst:
#          glb_kb.addRule(rule_info,True)
#     #If in the KB, assert this rule
#     else:
#         find_rule_rst.Asserted=True
# =============================================================================
    
#    print find_fact_rst
#    print find_rule_rst
    
    #Only check the first statement in LHS of rule
    bindings_=match(fact_info,rule_info[0][0], bindings())
    
    #If not match fisrt statement, return False
    if not bindings_:
        return False
    
    #If match
    #Check the length of LHS
    rule_LHS_len=len(rule_info[0])
    
    #LHS of rule only one statement,infer possible new fact
    if rule_LHS_len==1:
#        print "LHS length is 1"
        supported_by_fact=findFact(fact_info)
        supported_by_rule=findRule(rule_info)
        
        supported_by=InferPair(supported_by_fact,supported_by_rule)
        
        #Two cases for inferred fact
        
        #Instantiate RHS
        inferred_fact_statement= instantiate(rule_info[1],bindings_)
       
        #1. If inferred fact is NOT in KB yet, add the fact
        if not findFact(inferred_fact_statement):
#            glb_kb.addFactwithSupportedBy(inferred_fact_statement,supported_by)
            glb_kb.addFact(inferred_fact_statement,False)
              
        #2. If inferred fact is in KB, only add support  
        #Note: support is also necessary for new inferred
        supported_by.setName("InferPair "+str(glb_kb.ipIndx))
        inferredFact  =findFact(inferred_fact_statement)
        inferredFact.addSupportedBy(supported_by)
        glb_kb.ipIndx+=1
        
        supported_by_fact.addFactSupports(inferredFact)
        supported_by_rule.addFactSupports(inferredFact)     
        
    #LHS has more than one statement,  infer possible new rule
    else:
        rule_info_copy=deepcopy(rule_info)
        sliced_rule_info_copy= removeRuleFirstState(rule_info_copy)
         #Two cases for inferred fact
         
        instatiatedRule=instantiateRule(bindings_,sliced_rule_info_copy)
        
        supported_by_fact=findFact(fact_info)
        supported_by_rule=findRule(rule_info)
        
        supported_by=InferPair(supported_by_fact,supported_by_rule)
        
         #1. If inferred fact is NOT in KB yet, add the fact
        if not findRule(instatiatedRule):
#            glb_kb.addRulewithSupportedBy(instatiatedRule,supported_by)
            glb_kb.addRule(instatiatedRule,False)
        
        #2. If inferred fact is in KB, only add support  
        #Note: support is also necessary for new inferred     
#        inferredRule  =findRule(inferred_fact_statement)
        inferredRule  =findRule(instatiatedRule)
        supported_by.setName("InferPair "+str(glb_kb.ipIndx))
        inferredRule.addSupportedBy(supported_by)
        glb_kb.ipIndx+=1
        supported_by_fact.addRuleSupports(inferredRule)
        supported_by_rule.addRuleSupports(inferredRule)     
        

#The given fact and rule must have already existed in KB before infer others
def infer(fact, rule):
    info_infer(fact.info, rule.info)

print "Infer test 1"
aFact=glb_kb.facts[4]
aRule=glb_kb.rules[0]
print aFact
print aRule
#print aRule.info[0][0]
#print match(['inst', 'bigbox', 'box'],['inst', '?x', '?y'])
print infer(aFact,aRule)  
#
print glb_kb
print glb_kb.rules[5].printCompleteComp()
print ""
print glb_kb.rules[0].printCompleteComp()  
print ""
print glb_kb.facts[4].printCompleteComp() 


print ""
print "Infer test 2"
aFact=glb_kb.facts[22]
aRule=glb_kb.rules[1]
print aFact
print aRule
#print aRule.info[0][0]
#print match(['inst', 'bigbox', 'box'],['inst', '?x', '?y'])
print infer(aFact,aRule)  
#
print glb_kb
print glb_kb.facts[27].printCompleteComp()
print ""
print glb_kb.rules[1].printCompleteComp()  
print ""
print glb_kb.facts[22].printCompleteComp() 
print "Fact 27 is asserted:"
print glb_kb.facts[27].Asserted

print ""
print "Why test 2"
why(glb_kb.facts[27].info)
print "############### Why test 1 ###############"
why(['isa', 'cube', 'block'])
why(['isa', 'pyramid', 'block'])
why(['inst', 'bigbox', 'box'])
why(['inst', 'pyramid1', 'pyramid'])
why(['flat', '?x'])
why(['covered', '?y'])



#print ""
#print "kb_assert test 2: rule"
#print "Rule 6 is asserted: "+str(glb_kb.rules[5].Asserted)
#kb_assert(glb_kb.rules[5].info)
#print "After assert Rule 6 is asserted: "+str(glb_kb.rules[5].Asserted)
#
#
#
#print ""
#print "kb_assert test 3: fact"
#print "Fact 28 is asserted: "+str(glb_kb.facts[27].Asserted)
#kb_assert(glb_kb.facts[27].info)
#print "After assert Fact 28 is asserted: "+str(glb_kb.facts[27].Asserted)

#TODO: 1. Test retract rulE
#      2. Test the case where fact/rule is both inferred and asserted [IMPT]
def retract(statement):
    if isRule(statement):
        retractRule(statement)
    else:
        retractFact(statement)

#def removeCorrelatedIP(find_rule_rst.info,find_rule_rst.supportedBy,InfoType.RULE,supportedByRuleStatement,InfoType.RULE)
def removeCorrelatedIP(info, supportedBys, info_type, supportByInfo, suptbyino_type):
    if suptbyino_type ==InfoType.RULE:
         for supportBy in supportedBys:
             if supportBy.rule.info==supportByInfo:
                 #remove IP in coresponding fact
                 removeSupportInFact(info,info_type,supportBy.fact.info)
    elif suptbyino_type ==InfoType.FACT:
      for supportBy in supportedBys:
             if supportBy.fact.info==supportByInfo:
                 #remove IP in coresponding fact
                 removeSupportInRule(info,info_type,supportBy.rule.info)
    else:
      print "No such type"

def removeSupportInFact(info,info_type,fact_info):
    for fact in glb_kb.facts:
        if fact.info==fact_info:
            removed_index=[]
            if info_type==InfoType.RULE:
               for index, support in enumerate(fact.rules_supports):
                   if support.info==info:
                       removed_index.append(index)
               for index in removed_index:
                   del  fact.rules_supports[index] 
                    
            elif info_type ==InfoType.FACT:               
               for index, support in enumerate(fact.facts_supports):
                   if support.info==info:
                       removed_index.append(index)
               for index in removed_index:
                   del  fact.facts_supports[index]   
                            
def removeSupportInRule(info,info_type,rule_info):
     for rule in glb_kb.rules:
         if rule.info==rule_info:
             removed_index=[]
             if info_type==InfoType.RULE:
                for index, support in enumerate(rule.rules_supports):
                    if support.info==info:
                            removed_index.append(index)
                for index in removed_index:
                    del rule.rules_supports[index] 
                     
             elif info_type ==InfoType.FACT:               
                for index, support in enumerate(rule.facts_supports):
                    if support.info==info:
                        removed_index.append(index)
                for index in removed_index:
                    del rule.facts_supports[index]  
                             
        
        
def retractRule(rule_statment):
    
    find_rule_rst=findRule(rule_statment)
     
     #Fact is not existed in KB
    if not find_rule_rst:
         return False
    
    #Set asserted false
    if find_rule_rst.Asserted:
         print "Trying to retract the rule, but it is asserted"
         find_rule_rst.Asserted=False
#         return 
         
    #If still has supportedby, don't remove this fact
    if len(find_rule_rst.supportedBy)!=0:
        return
    
    #If not supported by anything, recrusively remove the support fact and rules
    for fact_support in find_rule_rst.facts_supports:
#         print supported_by
         retract_fact_support_by_rule(fact_support.info, rule_statment)
    
    
    #Remove support rules
    for rule_support in find_rule_rst.rules_supports:
        retract_rule_support_by_rule(rule_support.info, rule_statment)
    
   
    #Remove the rule itself
    glb_kb.remove_rule(find_rule_rst)       
    print glb_kb
        

def retractFact(fact_statment):
    
    find_fact_rst=findFact(fact_statment)
     
     #Fact is not existed in KB
    if not find_fact_rst:
         return False
    
    #Set asserted false
    if find_fact_rst.Asserted:
         print "Trying to retract the fact, but it is asserted"
         find_fact_rst.Asserted=False
#         return 
         
    #If still has supportedby, don't remove this fact
    if len(find_fact_rst.supportedBy)!=0:
        return
    
    #If not supported by anything, recrusively remove the support fact and rules
    for fact_support in find_fact_rst.facts_supports:
#         print supported_by
         retract_fact_support_by_fact(fact_support.info, fact_statment)
    
    
    #Remove support rules
    for rule_support in find_fact_rst.rules_supports:
        retract_rule_support_by_fact(rule_support.info, fact_statment)
        
    #Remove the fact itself
    glb_kb.remove_fact(find_fact_rst)
    
    
def retract_fact_support_by_fact(fact_statment,supportedByFactStatement):
    find_fact_rst=findFact(fact_statment)
     
     #If the KB is consistent, it should find the given fact
    if not find_fact_rst:
         return
     
    removed_ip_indexs=[]
    
     #Find the given supportedby
    for index, ip in enumerate(find_fact_rst.supportedBy):
        #Find the given supported by statement
        if ip.fact.info==supportedByFactStatement:
            removed_ip_indexs.append(index)
    
    saved_supportedBy=[]        
    #Remove the given supportedby        
    for index in removed_ip_indexs:  
        saved_supportedBy.append(find_fact_rst.supportedBy[index])
        del find_fact_rst.supportedBy[index]
    
    #Only fact has NO supportedby and is not asserted, retract it
    if len(find_fact_rst.supportedBy)==0:
        if find_fact_rst.Asserted==False:
             #Remove support facts
             for fact_support in find_fact_rst.facts_supports:
                 retract_fact_support_by_fact(fact_support.info, fact_statment)
             
             #Remove support rules
             for rule_support in find_fact_rst.rules_supports:
                 retract_rule_support_by_fact(rule_support.info, fact_statment)
             
             removeCorrelatedIP(find_fact_rst.info,saved_supportedBy,InfoType.FACT,supportedByFactStatement,InfoType.FACT)
             print "fact by fact"
             #Remove the fact itself
             glb_kb.remove_fact(find_fact_rst)
    
def retract_rule_support_by_fact(rule_statment,supportedByFactStatement):
    find_rule_rst=findRule(rule_statment)
     
     #If the KB is consistent, it should find the given rule
    if not find_rule_rst:
         return
     
    removed_ip_indexs=[]
    
     #Find the given supportedby
    for index, ip in enumerate(find_rule_rst.supportedBy):
        #Find the given supported by statement
        if ip.fact.info==supportedByFactStatement:
            removed_ip_indexs.append(index)
     
    saved_supportedBy=[]
    #Remove the given supportedby        
    for index in  removed_ip_indexs: 
        saved_supportedBy.append(find_rule_rst.supportedBy[index])
        del find_rule_rst.supportedBy[index]
    
    #Only fact has NO supportedby and is not asserted, retract it
    if len(find_rule_rst.supportedBy)==0:
        if find_rule_rst.Asserted==False:
             #Remove support facts
             for fact_support in find_rule_rst.facts_supports:
                 retract_fact_support_by_rule(fact_support.info, rule_statment)
             
             #Remove support rules
             for rule_support in find_rule_rst.rules_supports:
                 retract_rule_support_by_rule(rule_support.info, rule_statment)
             
             removeCorrelatedIP(find_rule_rst.info,saved_supportedBy,InfoType.RULE,supportedByFactStatement,InfoType.FACT)
#             removeCorrelatedIP(find_rule_rst.supportedBy,supportedByFactStatement,InfoType.RULE)
             #Remove the fact itself
             glb_kb.remove_rule(find_rule_rst)
        
    
def retract_fact_support_by_rule(fact_statment,supportedByRuleStatement):
    find_fact_rst=findFact(fact_statment)
     
     #If the KB is consistent, it should find the given fact
    if not find_fact_rst:
         return
     
    removed_ip_indexs=[]
    
     #Find the given supportedby
    for index, ip in enumerate(find_fact_rst.supportedBy):
        #Find the given supported by statement
        if ip.rule.info==supportedByRuleStatement:
            removed_ip_indexs.append(index)
    

    saved_supportedBy=[]   
    #Remove the given supportedby        
    for index in  removed_ip_indexs:   
        saved_supportedBy.append(find_fact_rst.supportedBy[index])
        del find_fact_rst.supportedBy[index]
    
    #Only fact has NO supportedby and is not asserted, retract it
    if len(find_fact_rst.supportedBy)==0:
        if find_fact_rst.Asserted==False:
             #Remove support facts
             for fact_support in find_fact_rst.facts_supports:
                 retract_fact_support_by_fact(fact_support.info, fact_statment)
             
             #Remove support rules
             for rule_support in find_fact_rst.rules_supports:
                 retract_rule_support_by_fact(rule_support.info, fact_statment)
            
             
             removeCorrelatedIP(find_fact_rst.info,saved_supportedBy,InfoType.FACT,supportedByRuleStatement,InfoType.RULE)
#             removeCorrelatedIP(find_fact_rst.supportedBy,supportedByRuleStatement,InfoType.FACT)
             #Remove the fact itself
             glb_kb.remove_fact(find_fact_rst)    
    
def retract_rule_support_by_rule(rule_statment,supportedByRuleStatement):
    find_rule_rst=findRule(rule_statment)
     
     #If the KB is consistent, it should find the given fact
    if not find_rule_rst:
         return
     
    removed_ip_indexs=[]
    
     #Find the given supportedby
    for index, ip in enumerate(find_rule_rst.supportedBy):
        #Find the given supported by statement
        if ip.rule.info==supportedByRuleStatement:
            removed_ip_indexs.append(index)
    
    saved_supportedBy=[]        
    #Remove the given supportedby        
    for index in  removed_ip_indexs:  
        saved_supportedBy.append(find_rule_rst.supportedBy[index])
        del find_rule_rst.supportedBy[index]
    
    #Only fact has NO supportedby and is not asserted, retract it
    if len(find_rule_rst.supportedBy)==0:
        if find_rule_rst.Asserted==False:
             #Remove support facts
             for fact_support in find_rule_rst.facts_supports:
                 retract_fact_support_by_rule(fact_support.info, rule_statment)
             
             #Remove support rules
             for rule_support in find_rule_rst.rules_supports:
                 retract_rule_support_by_rule(rule_support.info, rule_statment)
             
             removeCorrelatedIP(find_rule_rst.info,saved_supportedBy,InfoType.RULE,supportedByRuleStatement,InfoType.RULE)   
#             removeCorrelatedIP(find_rule_rst.supportedBy,supportedByRuleStatement,InfoType.FACT)
             #Remove the fact itself
             glb_kb.remove_rule(find_rule_rst)    
        
    
#print ""
#print "Retract test 1 for fact"
#print glb_kb
#retract(glb_kb.facts[22].info)   
#print glb_kb
#    
#print ""    
#print glb_kb.rules[1].printCompleteComp()      
#    
    










                                     
   
   