# -*- coding: utf-8 -*-

from enum import Enum
from copy import deepcopy
import operator
import Queue

class PegType(Enum):
    LEFT = 1
    MIDDLE = 2
    RIGHT = 3
    def __eq__(self, other):
        return (self.value== other.value)
    def __lt__(self, other):
        return (self.value < other.value)
    
class SearchType(Enum):
    DFS = 1
    BFS = 2
    BSTFS = 3

class Node:
    def __init__(self):
        self.value = None
        self.parent = None

class Disk:
    def __init__(self):
        self.value = None
        self.bottom = None
        
    def __eq__(self, other):
        return (self.value== other.value)
    def __lt__(self, other):
        return (self.value < other.value)        
    
#Helper Functions

#Check if two status are equal
#Return True if equal, False otherwise
def isMatch(status1,status2):
    result=True
    for pegType, disks in status1.iteritems():
        result=result and (status2[pegType]==disks)
    return result

#Check if given peg is empty
def isEmpty(aPeg):
    return not aPeg

#Check if the current status is already tracked
def wasTracked(aStatus,traced_statuses):
    return aStatus in traced_statuses

#Return the top disk on the peg
def topDisk(aPeg):
    if isEmpty(aPeg):
        return -1
    else:
        return aPeg[len(aPeg)-1]
 
#Calculate the heuristic
def heuristicScore_deprecated(curStatus, goalStatus):
    score=0
     #Check the status of each peg
    for pegType, cur_disks in curStatus.iteritems():
        goal_disks=goalStatus[pegType]
        

        #Peg is empty
        if isEmpty(cur_disks):
            #Equal
            if isEmpty(goal_disks):
                score=score+100
            #Not equal
#            else:
##                score=score-len(goal_disks)
#                score=score-1
        #Peg is not empty
        else:
            #Equal
            if cur_disks==goal_disks:
                score=score+100
            else:
                cur_disks_num=len(cur_disks)
                goal_disk_num=len(goal_disks)
                if cur_disks_num < goal_disk_num:
                    for idx, val in enumerate(cur_disks):#TODO: Curt assuming all goal disks are on the rightmost pegs
                        if cur_disks[idx]==goal_disks[idx]:
                            score=score+1
                else:
                    for idx, val in enumerate(goal_disks):#TODO: Curt assuming all goal disks are on the rightmost pegs
                        if cur_disks[idx]==goal_disks[idx]:
                            score=score+1
                            
    return -score

#Calculate the heuristic
#Compute the number of the disk(s) that are not on
#top of the correct item, and used as heuristic score
def heuristicScore(curStatus, goalStatus):
    score=0
    
    curt_disks=[]
    goal_disks=[]
    
    #Check the status of each goal peg
    for pegType, goalDisks in goalStatus.iteritems():      
            #Check if peg is empty
            if len(goalDisks)!=0:
                #Save first disk (on the bottom of the peg)
                cur_disk=Disk()
                cur_disk.value=goalDisks[0]
                cur_disk.bottom=pegType
                goal_disks.append(cur_disk)
                
                #Save rest disks
                if len(goalDisks)>0:
                    disk_index=1
                    for disk in goalDisks[1:]:
                        cur_disk=Disk()
                        cur_disk.value=disk
                        cur_disk.bottom=goalDisks[disk_index-1]
                        goal_disks.append(cur_disk)  
                        disk_index=disk_index+1
        
    #Check the status of each current peg
    for pegType, curDisks in curStatus.iteritems():
            #Check if peg is empty
            if len(curDisks)!=0:
                #Save first disk (on the bottom)
                cur_disk=Disk()
                cur_disk.value=curDisks[0]
                cur_disk.bottom=pegType
                curt_disks.append(cur_disk)
                
                #Save rest disks
                if len(curDisks)>0:
                    disk_index=1
                    for disk in curDisks[1:]:
                        cur_disk=Disk()
                        cur_disk.value=disk
                        cur_disk.bottom=curDisks[disk_index-1]
                        curt_disks.append(cur_disk)  
                        disk_index=disk_index+1
    
    #Sort the status list to align the disk number/value
    #of goal and current status
    curt_disks.sort()
    goal_disks.sort()
    
#    for dsk in curt_disks:
#        print dsk.value
#        print dsk.bottom
#    
#    for dsk in goal_disks:
#        print dsk.value
#        print dsk.bottom
    
    #Get the difference
    for idx, goal_val in enumerate(goal_disks):
        if curt_disks[idx].bottom!=goal_val.bottom:
            score=score+1

                            
    return score    
    
#Print Status of each Peg
def printPegs(aStatus):
    print ""
    print "-----CURRENT PEGS------"
    for pegType, disks in aStatus.iteritems():
         print str(pegType)+" "+  ('[%s]' % ', '.join(map(str, disks)))
    print "-----END---------"
    print ""


#Print the path that reaches the goal
def printGoalPath(goalNode):
    goalPath = Queue.LifoQueue()
    goalPath.put(goalNode.value)
    itr_node=goalNode
    while itr_node.parent!=None:
        goalPath.put(itr_node.parent.value)
        itr_node=itr_node.parent
    
    stepIndex=0
    while not goalPath.empty():
        print "Step "+str(stepIndex)+":" +str(goalPath.get())
        stepIndex=stepIndex+1
        



def TowerOfHanoi(start_status,expect_status,searchType):

    #Init a list to store traced cases 
    traced_statuses=[]
    #Add initial status
    traced_statuses.append(deepcopy(start_status))
    
    #Stack for DFS
    if searchType==SearchType.DFS:     
        moves = Queue.LifoQueue()
    #Queue for BFS    
    elif searchType==SearchType.BFS:
        moves = Queue.Queue()
    #PriorityQueue for BSTFS    
    elif searchType==SearchType.BSTFS:        
        moves = Queue.PriorityQueue()
    #Unknown Search Type
    else:
        return NotImplemented
    
    
    def HanoiMove(cur_status_node, expect_status):
        #Complete the movement
        if isMatch(cur_status_node.value,expect_status):
            return True
        
        topDisks={}
        #Check the status of each peg
        for pegType, disks in cur_status_node.value.iteritems():
            #Peg is empty
            if isEmpty(disks):
                topDisks[pegType]=-1
            #Peg is not empty
            else:
                topDisks[pegType]=topDisk(disks)
        
        #Sort the top disk of each peg in ascending order      
        sorted_topDisks = sorted(topDisks.items(), key=operator.itemgetter(1)) 
        
        curt_peg_index=0
        #Make the possible move
        #Main idea:
        #For each peg, two possible moves:
        #1. The peg is empty, any other peg's top-disk could be placed here
        #2. The peg is not empty, its top-disk can be placed on top of 
        #   those top-disk(s) has larger size
        
        #Get current peg top-disk
        for disk in sorted_topDisks[:-1]: 
            #peg name
            peg_name=disk[0]
            
            #disk value
            disk_value=disk[1]
            
            #Get folowing peg top-disk according to disk size
            for swaped_peg_index in range(curt_peg_index+1,len(sorted_topDisks)):
                    status_copy=deepcopy(cur_status_node.value)
                    
                   
                    swaped_disk=sorted_topDisks[swaped_peg_index][1]    
                    swaped_peg =sorted_topDisks[swaped_peg_index][0]
                    
                    #Case: peg is empty
                    #The following top disks can be placed on this empty peg
                    if(disk_value==-1):
                        if swaped_disk!=-1: #If swaped disk is empty, no swap
                            status_copy[peg_name].append(swaped_disk) #Add disk to new peg
                            status_copy[swaped_peg].remove(swaped_disk)#Remove the disk from old peg
                                
                            #If the status has been traced, undo it
                            if wasTracked(status_copy,traced_statuses):
                                status_copy[peg_name].remove(swaped_disk)
                                status_copy[swaped_peg].append(swaped_disk)
                            #Else add the status to TODO moves
                            else:
                                traced_statuses.append(deepcopy(status_copy))#TODO: check if deepcopy necessary

                                tracedNode=Node()
                                tracedNode.value=deepcopy(status_copy)
                                tracedNode.parent=cur_status_node
                                
                                if searchType==SearchType.BSTFS:
                                    hrstc_score=heuristicScore(deepcopy(status_copy),expect_status)
                                    moves.put((hrstc_score,tracedNode))
                                else:
                                    moves.put(tracedNode)
                    
                    #Case: peg is NOT empty
                    #Current peg can be placed on the following top disks 
                    else:
                            status_copy[swaped_peg].append(disk_value) #Add disk to new peg
                            status_copy[peg_name].remove(disk_value)#Remove the disk from old peg
                                
                            #If the status has been traced, undo it
                            if wasTracked(status_copy,traced_statuses):
                                status_copy[swaped_peg].remove(disk_value)
                                status_copy[peg_name].append(disk_value)
                            #Else add the status to TODO moves
                            else:
                                traced_statuses.append(deepcopy(status_copy))#TODO: check if deepcopy necessary
                                tracedNode=Node()
                                tracedNode.value=deepcopy(status_copy)
                                tracedNode.parent=cur_status_node
                                
                                if searchType==SearchType.BSTFS:
                                    hrstc_score=heuristicScore(deepcopy(status_copy),expect_status)
                                    moves.put((hrstc_score,tracedNode))
                                else:
                                    moves.put(tracedNode)
                    
            curt_peg_index=curt_peg_index+1
        return False
    
    
    print "Initial Status is:"
    printPegs(start_status)
    
    start_status_node=Node()
    start_status_node.value=start_status
        
    HanoiMove(start_status_node, expect_status)   
    
    itr_index=2
    while not moves.empty():
        print ""
        print "Iteration: "+str(itr_index)
        itr_index=itr_index+1
        
        if searchType==SearchType.BSTFS:
            next_status= deepcopy(moves.get())[1]
        else:
            next_status= moves.get()
        
        printPegs(next_status.value)
        rst=HanoiMove(next_status, expect_status)
        if rst:
            print "Reach the goal"
            print "Total iteration is: " +str(itr_index)
            printGoalPath(next_status)
            return
    print "No Path Found"









#==============================================================================
# Main Function
#==============================================================================


#Initial Status
init_status={}
peg_left = []
peg_middle = []
peg_right = []

init_status[PegType.LEFT]=peg_left
init_status[PegType.MIDDLE]=peg_middle
init_status[PegType.RIGHT]=peg_right

#init_status[PegType.LEFT].append(11)
#init_status[PegType.LEFT].append(10)
#init_status[PegType.LEFT].append(9)
#init_status[PegType.LEFT].append(8)
#init_status[PegType.LEFT].append(7)
#init_status[PegType.LEFT].append(6)
init_status[PegType.LEFT].append(5)
init_status[PegType.LEFT].append(4)
init_status[PegType.LEFT].append(3)
init_status[PegType.LEFT].append(2)
init_status[PegType.LEFT].append(1)




#End Status
end_status={}
peg_left_end = []
peg_middle_end = []
peg_right_end = []

end_status[PegType.LEFT]=peg_left_end
end_status[PegType.MIDDLE]=peg_middle_end
end_status[PegType.RIGHT]=peg_right_end

#end_status[PegType.RIGHT].append(11)
#end_status[PegType.RIGHT].append(10)
#end_status[PegType.RIGHT].append(9)
#end_status[PegType.RIGHT].append(8)
#end_status[PegType.RIGHT].append(7)
#end_status[PegType.RIGHT].append(6)
end_status[PegType.RIGHT].append(5)
end_status[PegType.RIGHT].append(4)
end_status[PegType.RIGHT].append(3)
end_status[PegType.RIGHT].append(2)
end_status[PegType.RIGHT].append(1)



#==============================================================================
# Uncomment the code here accordingly for testing        
#==============================================================================

TowerOfHanoi(init_status,end_status,SearchType.DFS)    
#TowerOfHanoi(init_status,end_status,SearchType.BFS)  
# TowerOfHanoi(init_status,end_status,SearchType.BSTFS)  