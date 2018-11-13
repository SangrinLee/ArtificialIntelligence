# File: Players.py

from random import *
from decimal import *
from copy import *
from MancalaBoard import *

# a constant
INFINITY = 1.0e400

class Player:
    """ A basic AI (or human) player """
    HUMAN = 0
    RANDOM = 1
    MINIMAX = 2
    ABPRUNE = 3
    CUSTOM = 4
    
    def __init__(self, playerNum, playerType, ply=0):
        """Initialize a Player with a playerNum (1 or 2), playerType (one of
        the constants such as HUMAN), and a ply (default is 0)."""
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = playerType
        self.ply = ply
        self.score_step_pair=[]

    def __repr__(self):
        """Returns a string representation of the Player."""
        return str(self.num)
        
    def minimaxMove(self, board, ply):
        """ Choose the best minimax move.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minValue(nb, ply-1, turn)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move

    def maxValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.minValue(nextBoard, ply-1, turn)
            #print "s in maxValue is: " + str(s)
            if s > score:
                score = s
        return score
    
    def minValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maxValue(nextBoard, ply-1, turn)
            #print "s in minValue is: " + str(s)
            if s < score:
                score = s
        return score


    # The default player defines a very simple score function
    # You will write the score function in the MancalaPlayer below
    # to improve on this function.
    def score(self, board):
        """ Returns the score for this player given the state of the board """
        if board.hasWon(self.num):
            return 100.0
        elif board.hasWon(self.opp):
            return 0.0
        else:
            return 50.0

    # You should not modify anything before this point.
    # The code you will add to this file appears below this line.

    # You will write this function (and any helpers you need)
    # You should write the function here in its simplest form:
    #   1. Use ply to determine when to stop (when ply == 0)
    #   2. Search the moves in the order they are returned from the board's
    #       legalMoves function.
    # However, for your custom player, you may copy this function
    # and modify it so that it uses a different termination condition
    # and/or a different move search order.
    def alphaBetaMove(self, board, ply):
        """ Choose a move with alpha beta pruning.  Returns (score, move) """
        # Create a list to store a pair of score and move
        self.score_step_pair  =[]
        move = -1
        score = -INFINITY
        turn = self
        
        # Initially, alpha_value is negative infinity and beta_value is positive infinity
        alph=-INFINITY
        beta=INFINITY
        
        board_copy = deepcopy(board)
        bst_score=self.ab_maxValue(board_copy,ply,turn,alph,beta)
        # print "Best score is: "+str(bst_score)
        
        # check a score_step_pair list to see to retrieve the best move
        for score_move in self.score_step_pair:
            print score_move[0],score_move[1]
            if score_move[0]==bst_score:
                return bst_score, score_move[1]
        
        self.ply = 0
        if len(self.score_step_pair) == 0:
            return bst_score, board.legalMoves(self)[0]   
        #return the best score and move      
        return score,move
        
   
    def ab_maxValue(self, board, ply, turn, alph, beta):
        """ Find the best score for the next move for this player
        at a given board configuation. Returns score."""
        alph_copy=alph
        beta_copy=beta

        # Can't make a move, the game is over
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.ab_minValue(nextBoard, ply-1, turn,alph_copy,beta_copy)
            if s > score:
                #if the result is better than our best score so far, save that score
                #and store a pair of that score and move
                score = s
                self.score_step_pair.append((score,m))
           
            #if the score is not less than beta value, then return the score
            if not score<beta_copy:
                return score
            #if the score is greater than alpha value, then store that score into alpha value
            if score>alph_copy:
                alph_copy=score
        #return the best score
        return score
    
    def ab_minValue(self, board, ply, turn, alph, beta):
        """ Find the score for the next move for this player
            at a given board configuation. Returns score."""
        alph_copy=alph
        beta_copy=beta

        # Can't make a move, the game is over
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.ab_maxValue(nextBoard, ply-1, turn,alph_copy,beta_copy)
            if s < score:
                #if the result is lower than our best score so far, save that score
                score = s
            
            #if the score is not greater than alpha value, then return the score
            if not score>alph_copy:
                return score
            #if the score is less than beta value, then store that score into beta value
            if score<beta_copy:
                beta_copy=score
        #return the best score
        return score

    def greedyMove(self, board):
        """ Choose a move with greedy algorithm.  Returns (score, move) """
           
        move = -1
        best_score = -INFINITY
        turn = self
        
        for m in board.legalMoves(self):
            #for each legal move
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            v=turn.score(nb)
            
            if v>best_score:
                #if the result is better than our best score so far, save that move,score
                best_score=v
                move=m

        #return the best score and move so far
        return best_score,move
  
    

             
    def chooseMove(self, board):
        """ Returns the next move that this player wants to make """
        if self.type == self.HUMAN:
            move = input("Please enter your move:")
            while not board.legalMove(self, move):
                print move, "is not valid"
                move = input( "Please enter your move" )
            return move
        elif self.type == self.RANDOM:
            move = choice(board.legalMoves(self))
            print "chose move", move
            return move
        elif self.type == self.MINIMAX:
            val, move = self.minimaxMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.ABPRUNE:
            val, move = self.alphaBetaMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.CUSTOM:
            # TODO: Implement a custom player
            # You should fill this in with a call to your best move choosing
            # function.  You may use whatever search algorithm and scoring
            # algorithm you like.  Remember that your player must make
            # each move in about 10 seconds or less.

			# We have tried various parameters for self.ply, and noticed that ply with 9 values would be ideal.
            # So, we decided to set it as 9 for the game to run. 
            # Also, We also implemented another search algorithms named Greedy Algorithms.
            # For more checks commented code below.
            self.ply = 9
            val, move = self.alphaBetaMove(board, self.ply)
            # Comment below line out to use Greedy Algorithm
            # val,move=self.greedyMove(board)
            return move
        else:
            print "Unknown player type"
            return -1


# Note, you should change the name of this player to be your netid
class Players(Player):
    """ Defines a player that knows how to evaluate a Mancala gameboard
        intelligently """

    def score(self, board):
        """ Evaluate the Mancala board for this player """
        # Currently this function just calls Player's score
        # function.  You should replace the line below with your own code
        # for evaluating the board

        # We explored various combination or solo of pieces of my side, opponent's side. 
        # Also, considered the total number of my Mancala and opponent's Mancala, distance of attempted moves to opponent's and our Mancala.
        # We found below function works promising. So function below is selected.
        # Calculate my score by summing the number of pieces I currently have in my Mancala 
        # and total number of pieces on my side of the board
        my_score = board.scoreCups[self.num-1] + sum(board.P1Cups)
        # Calculate opponent's score by summing the number of pieces the opponent currently has in his Mancala 
        # and total number of pieces on his side of the board
        opponent_score = board.scoreCups[self.opp-1] + sum(board.P2Cups)
        # Evaluate the Mancala board by getting the difference between my score and the opponent's score
        eval_board = my_score - opponent_score
        return eval_board
        
        # return Player.score(self, board)