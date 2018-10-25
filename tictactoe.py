
from copy import deepcopy
from math import sqrt, log

class tictactoe(object):
 	"""
	This class implements the rules and dynamic of TicTacToe (3x3 grid)
		args     - list representing game state (3x3 reshaped into a single line)
		complete - If True game is finished
		winner   - Winner of the game ('X' or 'O')
 	"""
 	def __init__(self, arg = ['-','-','-','-','-','-','-','-','-'] ):
 		self.args = list(arg)
 		self.complete = False
 		self.winner = ''

 	def MissingTiles(self):
 		"""
 		Returns list of tiles not yet filled
 		"""
 		missing = [i for i in range(9) if self.args[i] == '-']
		return missing

 	def CheckRowComplete(self,row):
 		"""
		Checks if a certain row is won by any player
		Inputs:
			row - 1,2 or 3
		Outputs:
			bool - True if completed
 		"""
 		if self.args[3*row] == 'X' and self.args[3*row+1] == 'X' and self[3*row+2] == 'X':
 			self.winner = 'X'
 			return True
 		if self.args[3*row] == 'O' and self.args[3*row+1] == 'O' and self[3*row+2] == 'O':
 			self.winner = 'O'
 			return True
 		else:
 			return False

 	def CheckColumnComplete(self,column):
		"""
		Checks if a certain column is won by any player
		Inputs:
			row - 1,2 or 3
		Outputs:
			bool - True if completed
 		"""
 		if self.args[column] == 'X' and self.args[column+3] == 'X' and self[column+6] == 'X':
 			self.winner = 'X'
 			return True
 		elif self.args[column] == 'O' and self.args[column+3] == 'O' and self[column+6] == 'O':
 			self.winner = 'O'
 			return True
 		else:
 			return False

 	def CheckDiagonalComplete(self):
 		"""
		Checks if any diagonal is won by any player
		Inputs:
			None
		Outputs:
			bool - True if completed
 		"""
 		if ((self.args[0] == 'X' and self.args[4] == 'X' and self.args[8] == 'X') 
	  		or (self.args[2] == 'X' and self.args[4] == 'X' and self.args[6] == 'X')):
 			self.winner = 'X'
 			return True

	  	elif ((self.args[0] == 'O' and self.args[4] == 'O' and self.args[8] == 'O') 
	  		or (self.args[2] == 'O' and self.args[4] == 'O' and self.args[6] == 'O')):
	  		self.winner = 'O'
 			return True
 		
 		else:
 			return False

	def CheckComplete(self):
		"""
		Checks if game is won by any player
 		"""
		if self.complete:
			return True

		else:
			for i in range(3):
				if self.CheckRowComplete(i) or self.CheckColumnComplete(i):
					self.complete = True
					return True

			if self.CheckDiagonalComplete():
				self.complete = True
				return True

			if len(self.MissingTiles()) == 0:
				self.complete = True
				self.winner ='D'
				return True

			return False

	def PossibleCenter(self):
		"""
		Checks if it is possible to play in the center square
		"""
		if self.args[4] == '-':
			return True
		else:
			return False

	def PossibleSide(self):
		"""
		Checks if it is possible to play in any side square
		"""
		if self.args[1] == '-':
			return 1
		elif self.args[3] == '-':
			return 3
		elif self.args[5] == '-':
			return 5
		elif self.args[7] == '-':
			return 7
		else:
			return None

	def PossibleCorner(self):
		"""
		Checks if it is possible to play in any corner
		"""
		if self.args[0] == '-':
			return 0
		elif self.args[2] == '-':
			return 2
		elif self.args[6] == '-':
			return 6
		elif self.args[8] == '-':
			return 8
		else:
			return None

	def PossibleOppositeCorner(self,value):
		if self.args[0] == value and self.args[8] == '-':
			return 8
		elif self.args[8] == value and self.args[0] == '-':
			return 0
		elif self.args[2] == value and self.args[6] == '-':
			return 6
		elif self.args[6] == value and self.args[2] == '-':
			return 2
		else:
			return None

	def PossibleRowWin(self,value):
		"""
		Check if it is possible to win any row with the next play
		Inputs:
			value - 'X' or 'O'
		Outputs:
			square - play which leads to winning the row (None if it is not possible)
		"""
		for row in range(3):
			if self.args[3*row] == value and self.args[3*row+1] == value and self.args[3*row+2] == '-':
				return 3*row+2
			elif self.args[3*row] == value and self.args[3*row+1] == '-' and self.args[3*row+2] == value:
				return 3*row+1
			elif self.args[3*row] == '-' and self.args[3*row+1] == value and self.args[3*row+2] == value:
				return 3*row

		return None

	def PossibleColumnWin(self,value):
		"""
		Check if it is possible to win any column with the next play
		Inputs:
			value - 'X' or 'O' 
		Outputs:
			square - play which leads to winning the column (None if it is not possible)
		"""
		for column in range(3):
			if self.args[column] == value and self.args[column+3] ==  value and self.args[column+6] == '-':
				return column+6
			elif self.args[column] == value and self.args[column+3] ==  '-' and self.args[column+6] == value:
				return column+3
			elif self.args[column] == '-' and self.args[column+3] ==  value and self.args[column+6] == value:
				return column

		return None

	def PossibleDiagonalWin(self,value):
		"""
		Check if it is possible to win any diagonal with the next play
		Inputs:
			value - 'X' or 'O' 
		Outputs:
			square - play which leads to winning the column (None if it is not possible)
		"""
		if self.args[0] == value and self.args[4] == value and self.args[8] == '-':
			return 8
		elif self.args[0] == value and self.args[8] == value and self.args[4] == '-':
			return 4
		elif self.args[4] == value and self.args[8] == value and self.args[0] == '-':
			return 0
		elif self.args[2] == value and self.args[4] == value and self.args[6] == '-':
			return 6
		elif self.args[2] == value and self.args[4] == '-' and self.args[6] == value:
			return 4
		elif self.args[2] == '-' and self.args[4] == value and self.args[6] == value:
			return 2
		return None

	def CheckPossibleWin(self,value):
		"""
		Check if there is any play from the current player or its opponent that 
		might lead him to win the game 
		Inputs:
			value - 'X' or 'O' 
		Outputs:
			square - play which leads to winning condition (None if it is not possible)
		"""
		possible_win = self.PossibleRowWin(value)
		if possible_win!= None:
			return possible_win		
		
		possible_win = self.PossibleColumnWin(value)
		if possible_win!= None:
			return possible_win
		
		possible_win = self.PossibleDiagonalWin(value)
		if possible_win!= None:
			return possible_win

		return None

	def PossibleDiagonalFork(self,value):
		"""
		Check if it is possible to perform a diagonal fork
		Inputs:
			value - 'X' or 'O'
		Outputs:
			square - action that leads to fork (or stops a possible fork if 'value' represents the opponent)
		"""
		if self.args[0] == value and self.args[8] == value:
			if self.args[2] == '-' and self.args[1] == '-' and self.args[5] == '-':
				return 2
			elif self.args[6] == '-' and self.args[3] == '-' and self.args[7] == '-':
				return 6

		if self.args[2] == value and self.args[6] == value :
			if self.args[0] == '-' and self.args[1] == '-' and self.args[3] == '-':
				return 0
			elif self.args[8] == '-' and self.args[7] == '-' and self.args[5] == '-':
				return 8

		return None

	def PossibleCFork(self,value):
		"""
		Check if it is possible to perform a C fork
		Inputs:
			value - 'X' or 'O'
		Outputs:
			square - action that leads to fork (or stops a possible fork if 'value' represents the opponent)
		"""
		if self.args[6] == value and self.args[5] == value:
			if self.args[3] == '-' and self.args[4] == '-' and self.args[0] == '-':
				return 3
			elif self.args[4] == '-' and self.args[3] == '-' and self.args[2] == '-':
				return 4
			elif self.args[8] == '-' and self.args[7] == '-' and self.args[2] == '-':
				return 8
			elif self.args[2] == '-' and self.args[4] == '-' and self.args[8] == '-':
				return 2

		if self.args[0] == value and self.args[7] == value:
			if self.args[1] == '-' and self.args[2] == '-' and self.args[4] == '-':
				return 1
			elif self.args[4] == '-' and self.args[2] == '-' and self.args[8] == '-':
				return 4
			elif self.args[6] == '-' and self.args[3] == '-' and self.args[8] == '-':
				return 6
			elif self.args[8] == '-' and self.args[6] == '-' and self.args[4] == '-':
				return 8

		if self.args[2] == value and self.args[3] == value:
			if self.args[0] == '-' and self.args[1] == '-' and self.args[6] == '-':
				return 0
			elif self.args[4] == '-' and self.args[5] == '-' and self.args[6] == '-':
				return 4
			elif self.args[5] == '-' and self.args[8] == '-' and self.args[4] == '-':
				return 5
			elif self.args[6] == '-' and self.args[4] == '-' and self.args[0] == '-':
				return 6

		if self.args[1] == value and self.args[8] == value:
			if self.args[2] == '-' and self.args[0] == '-' and self.args[5] == '-':
				return 2
			elif self.args[4] == '-' and self.args[7] == '-' and self.args[0] == '-':
				return 4
			elif self.args[7] == '-' and self.args[6] == '-' and self.args[4] == '-':
				return 7
			elif self.args[0] == '-' and self.args[4] == '-' and self.args[2] == '-':
				return 0

		if self.args[0] == value and self.args[5] == value:
			if self.args[2] == '-' and self.args[1] == '-' and self.args[8] == '-':
				return 2
			elif self.args[3] == '-' and self.args[7] == '-' and self.args[0] == '-':
				return 3
			elif self.args[7] == '-' and self.args[6] == '-' and self.args[4] == '-':
				return 7
			elif self.args[8] == '-' and self.args[4] == '-' and self.args[2] == '-':
				return 8

		if self.args[2] == value and self.args[7] == value:
			if self.args[1] == '-' and self.args[0] == '-' and self.args[4] == '-':
				return 1
			elif self.args[4] == '-' and self.args[6] == '-' and self.args[1] == '-':
				return 4
			elif self.args[8] == '-' and self.args[6] == '-' and self.args[5] == '-':
				return 8
			elif self.args[6] == '-' and self.args[4] == '-' and self.args[8] == '-':
				return 6

		if self.args[3] == value and self.args[8] == value:
			if self.args[6] == '-' and self.args[7] == '-' and self.args[0] == '-':
				return 6
			elif self.args[4] == '-' and self.args[5] == '-' and self.args[0] == '-':
				return 4
			elif self.args[5] == '-' and self.args[4] == '-' and self.args[2] == '-':
				return 5
			elif self.args[0] == '-' and self.args[4] == '-' and self.args[6] == '-':
				return 0

		if self.args[1] == value and self.args[6] == value:
			if self.args[0] == '-' and self.args[2] == '-' and self.args[3] == '-':
				return 0
			elif self.args[4] == '-' and self.args[7] == '-' and self.args[2] == '-':
				return 4
			elif self.args[7] == '-' and self.args[4] == '-' and self.args[8] == '-':
				return 7
			elif self.args[2] == '-' and self.args[4] == '-' and self.args[0] == '-':
				return 2

		return None

	def CheckPossibleFork(self,value):
		"""
		Check if there is any play from the current player or its opponent that 
		might create a fork
		Inputs:
			value - 'X' or 'O' 
		Outputs:
			square - play which leads to fork (None if it is not possible)
		"""
		fork = self.PossibleDiagonalFork(value)
		if fork:
			return fork
		fork = self.PossibleCFork(value)
		if fork:
			return fork
		return None				

	def __getitem__(self,index):
		return self.args[index]

	def __setitem__(self,index,value):
		self.args[index] = value

	def __repr__(self):
		out = ''
		for i in range(3):
			out = out + str(self.args[3*i:3*i+3]) + '\n'
		return out


class ultimate_tictactoe(object):

	"""
	This class implements the rules and dynamic of  Ultimate TicTacToe (3x3 grid of TicTacToe games where each subgame is also 3x3)
		ttt      		- list containing the 9 tictactoe objects representing the subgames
		args     		- list containing the winners of each of the 9 subgames
		complete 		- If True game is finished
		win   			- int representing the winner of the game ('X'=-1, 'O'=+1, draw = 0)
		subgame_to_play - subgame where next play should occur (supposes it is still possible to play in that subgame)
		turn			- next player to play ('X' or 'O')
		move 			- last move ([subgame_played, square_selected])
		score 			- current score of this state (used for UCB) 
		ni 				- stores number of times this state was visited
 	"""	

	def __init__(self, ttt = None, subgame_to_play = 0, args = ['-','-','-','-','-','-','-','-','-'], complete = False,\
				win = 0, turn = 'X', move = None, score = 0, ni = 0):
 		if ttt == None:
 			lista = [tictactoe() for i in range(9)]
 			self.ttt = list(lista)
 		else :
 			self.ttt = ttt
 		self.args = list(args)
 		self.complete = complete
 		self.win = win
		self.subgame_to_play = subgame_to_play
		self.turn = turn
		self.move = move
		self.score = score
		self.ni = ni

	def Copy(self):
		return deepcopy(self)

 	def Set(self,index1,index2,value):
 		self.ttt[index1].args[index2] = value

 	def CheckRowComplete(self,row):
 		"""
		Checks if a certain row of the main game is won by any player
		Inputs:
			row - 1,2 or 3
		Outputs:
			bool - True if completed
 		"""
 		if self.args[3*row] == 'X' and self.args[3*row+1] == 'X' and self.args[3*row+2] == 'X':
 			self.win = -1
 			return True
 		if self.args[3*row] == 'O' and self.args[3*row+1] == 'O' and self.args[3*row+2] == 'O':
 			self.win = 1
 			return True
 		else:
 			return False

 	def CheckColumnComplete(self,column):
 		"""
		Checks if a certain column of the main game is won by any player
		Inputs:
			row - 1,2 or 3
		Outputs:
			bool - True if completed
 		"""
 		if self.args[column] == 'X' and self.args[column+3] == 'X' and self.args[column+6] == 'X':
 			self.win = -1
 			return True
 		elif self.args[column] == 'O' and self.args[column+3] == 'O' and self.args[column+6] == 'O':
 			self.win = 1
 			return True
 		else:
 			return False

 	def CheckDiagonalComplete(self):
 		"""
		Checks if any diagonal of the main game is won by any player
		Inputs:
			None
		Outputs:
			bool - True if completed
 		"""
 		if ((self.args[0] == 'X' and self.args[4] == 'X' and self.args[8] == 'X') 
 			or (self.args[2] == 'X' and self.args[4] == 'X' and self.args[6] == 'X')):
 				self.win = -1
 				return True
	 	elif ((self.args[0] == 'O' and self.args[4] == 'O' and self.args[8] == 'O')
	  		or (self.args[2] == 'O' and self.args[4] == 'O' and self.args[6] == 'O')):
	 			self.win = 1
	 			return True		
 		else:
 			return False

 	def CheckComplete(self):
 		"""
		Checks if game is completed, either because it was won 
		by a player or if a draw occurred
		Inputs:
			None
		Outputs:
			bool - True if game ended
		"""
 		if self.complete:
 			return True
	
		else:
			for i in range(9):
				if self.args[i]!= '-':
					pass
				elif self.ttt[i].CheckComplete():
					self.args[i] = self.ttt[i].winner

			for i in range(3):
				if self.CheckRowComplete(i) or self.CheckColumnComplete(i):
					self.complete = True
					return True
		
			if self.CheckDiagonalComplete():
				self.complete = True
				return True

			if not('-' in self.args):
				self.complete = True
				return True

			return False

 	def PossibleMoves(self):
 		"""
		Returns possible moves from current game state
		Inputs:
			None
		Outputs:
			list_moves - list of possible moves (each move is given by [subgame_played, square_selected])
		"""
		list_moves = []

		# check if game ended
 		if self.CheckComplete():
 			return []

 		# case where we were supposed to play in a subgame
 		# has already been completed
 		elif self.ttt[self.subgame_to_play].CheckComplete():
 			# in this case all moves in any subgame that has not
 			# yet been finished are possible	
 			for i in range(9):
 				if i!= self.subgame_to_play:
 					if not(self.ttt[i].CheckComplete()):
 						missing_tiles = self.ttt[i].MissingTiles()
 						for missing_tile in missing_tiles:
 							list_moves.append([i,missing_tile])
 		
 		# case where it is possible to play in the current subgame
 		else :
 			for tile in self.ttt[self.subgame_to_play].MissingTiles():
 				list_moves.append([self.subgame_to_play,tile])
 		
 		return list_moves
 		
 	def Expand(self):
 		"""
 		Generate all possible successors of the current game
 		Inputs:
 			None
 		Outputs
 			list_sons - list of ultimate_tic_tac_toe objects representing
 						all possible successors of the current game
 		"""
 		possible_moves = self.PossibleMoves()
 		list_sons = [self.DoMove(move) for move in possible_moves]
 		return list_sons

 	def DoMove(self,move):
 		"""
 		Generates a successor based on current state and the chosen move
 		Inputs:
 			move - [subgame_to_play, square_play]
 		Outputs:
 			succesor - succesor state as ultimate_tictactoe object
 		"""
	 	if self.turn == 'X':
			successor = deepcopy(ultimate_tictactoe(ttt = self.ttt, subgame_to_play = move[1], turn = 'O', move = move))
		else:
			successor = deepcopy(ultimate_tictactoe(ttt = self.ttt, subgame_to_play = move[1], turn = 'X', move = move))
		successor.Set(move[0],move[1],self.turn)

		return successor

	def DoMove2(self,move):
		"""
 		Performs a certain move in the current ultimate_tictactoe object 
 		and no successor is created
 		Inputs:
 			move - [subgame_to_play, square_play]
 		"""
		self.Set(move[0],move[1],self.turn)
		self.move = move
		self.subgame_to_play = move[1]
		if self.turn == 'X':
			self.turn = 'O'
		else:
			self.turn = 'X'


	def UCB1(self, parent_ni):
		"""
		Calculates UCB1 score for current game state
		Inputs:
			parent_ni - number of times the parent of this game state was visited
		Outputs
			UCB1 - UCB1 value
		"""
		if(self.ni == 0):
			return 100000000000
		else:
			return float(self.score)/self.ni + .04*2*sqrt(2*log(parent_ni)/self.ni)

	def Score(self):
		"""
		Calculates overal score of the current game state
		Inputs:
			None
		Outputs:
			score - overal score
		"""
		if self.ni == 0:
			return -1000000000000
		else:
			return float(self.score)/self.ni


 	def __getitem__(self,index):
		return self.ttt[index]

	def __repr__(self):
		out = ''
		for i in range(3):
			for j in range(3):
				out = out + str(self.ttt[3*i].args[3*j:3*j+3]) + '|' \
				+ str(self.ttt[3*i+1].args[3*j:3*j+3]) + '|' \
				+ str(self.ttt[3*i+2].args[3*j:3*j+3]) + '\n'
			out = out + '_______________________________________________\n'
		
		out = out + 'Player turn :' + self.turn + '\n'
		out = out + '_______________________________________________\n'
 		return out
