
from random import randint
import multiprocessing as mp

INTMIN = -100000000

def RandomPlayer(node):
	"""
	Simulate one play from a player that only does random movements
	Inputs:
		node - current game state
	Returns:
		new_node - game state after player move
	"""

	#dumb player plays	
	possible_moves = node.PossibleMoves()
	move = possible_moves[randint(0,len(possible_moves)-1)]
	return node.DoMove(move)

def FinishSquarePlayer(node):
	"""
	Simulate one play from a player that plays according to normal TicTacToe 
	rules (always tries to win current subgame_state)
	Inputs:
		node - current game state
	Returns:
		new_node - game state after player move
	"""

	# determine which players turn it is
	player = node.turn
	if player == 'X':
		opponent = 'O'
	else:
		opponent = 'X'

	# check if all possible moves are associated 
	# with the same subgame or if it is possible to 
	# choose which subgame to play in 
	# (this happens when you are sent to a subgame which was already won)

	same_subgame = True
	possible_moves = node.PossibleMoves()
	for move in possible_moves:
		if move[0] != possible_moves[0][0]:
			same_subgame = False
			break

	if same_subgame:
		# In this scenario it plays according to a perfect TicTactToe player
		# strategy as defined in 
		# https://en.wikipedia.org/wiki/Tic-tac-toe
		subgame_to_play = possible_moves[0][0]
		subgame_state = node.ttt[subgame_to_play]

		# 1. Check if it can win subgame, if so win subgame
		possible_win = subgame_state.CheckPossibleWin(player)
		if possible_win != None:
			return node.DoMove([subgame_to_play,possible_win])

		# 2. Check if opponent can win subgame, if so block
		possible_loss = subgame_state.CheckPossibleWin(opponent)
		if possible_loss != None:
			return node.DoMove([subgame_to_play, possible_loss])

		# 3. Check if fork possible for himself
		possible_fork = subgame_state.CheckPossibleFork(player)
		if possible_fork != None:
			return node.DoMove([subgame_to_play, possible_fork])

		# 4. Check if opponent can fork, block it
		#-- 1st type fork
		possible_diag_fork = subgame_state.PossibleDiagonalFork(opponent)
		if possible_diag_fork != None:
			if subgame_state.PossibleCenter():
				return node.DoMove([subgame_to_play, 4])
			else:
				return node.DoMove([subgame_to_play,subgame_state.PossibleSide()])
		#-- 2nd type fork
		possible_c_fork =  subgame_state.PossibleCFork(opponent)
		if possible_c_fork != None:
			return node.DoMove([subgame_to_play, possible_c_fork])

		# 5. Play in center
		if subgame_state.PossibleCenter():
			return node.DoMove([subgame_to_play,4])

		# 6. Play in opposite corner
		possible_opposite_corner = subgame_state.PossibleOppositeCorner(opponent)
		if possible_opposite_corner != None:
			return node.DoMove([subgame_to_play, possible_opposite_corner])

		# 7. Play in the corner
		possible_corner = subgame_state.PossibleCorner()
		if possible_corner != None:
			return node.DoMove([subgame_to_play,possible_corner])

		# 8. Play in one side
		possible_side = subgame_state.PossibleSide()
		if possible_side != None:
			return node.DoMove([subgame_to_play, possible_side])

	else:
		# In this scenario it follows a different strategy
		# where winning or blocking subgames wins from opponents
		# are prioritized
		possible_subgames = []
		for move in possible_moves:
			if move[0] not in possible_subgames:
				possible_subgames.append(move[0])

		# 1. Check if it can win subgame, if so win subgame
		for subgame_to_play in possible_subgames:
			subgame_state = node.ttt[subgame_to_play]
			possible_win = subgame_state.CheckPossibleWin(player)
			if possible_win != None:
				return node.DoMove([subgame_to_play,possible_win])

		# 2. Check if opponent can win subgame, if so block
		for subgame_to_play in possible_subgames:
			subgame_state = node.ttt[subgame_to_play]
			possible_loss = subgame_state.CheckPossibleWin(opponent)
			if possible_loss != None:
				return node.DoMove([subgame_to_play, possible_loss])

#------------------------------
		# 3. Check if fork possible for himself
		for subgame_to_play in possible_subgames:
			subgame_state = node.ttt[subgame_to_play]
			possible_fork = subgame_state.CheckPossibleFork(player)
			if possible_fork != None:
				return node.DoMove([subgame_to_play, possible_fork])

		# 4. Check if opponent can fork, block it
		#-- 1st type fork
		for subgame_to_play in possible_subgames:
			subgame_state = node.ttt[subgame_to_play]
			possible_diag_fork = subgame_state.PossibleDiagonalFork(opponent)
			if possible_diag_fork != None:
				if subgame_state.PossibleCenter():
					return node.DoMove([subgame_to_play, 4])
				else:
					return node.DoMove([subgame_to_play,subgame_state.PossibleSide()])
	
		#-- 2nd type fork
		for subgame_to_play in possible_subgames:
			subgame_state = node.ttt[subgame_to_play]
			possible_c_fork =  subgame_state.PossibleCFork(opponent)
			if possible_c_fork != None:
				return node.DoMove([subgame_to_play, possible_c_fork])
#------------------------------

		# 5. Play in center
		for subgame_to_play in possible_subgames:
			subgame_state = node.ttt[subgame_to_play]
			if subgame_state.PossibleCenter():
				return node.DoMove([subgame_to_play,4])

		# 6. Play in opposite corner
		for subgame_to_play in possible_subgames:
			subgame_state = node.ttt[subgame_to_play]
			possible_opposite_corner = subgame_state.PossibleOppositeCorner(opponent)
			if possible_opposite_corner != None:
				return node.DoMove([subgame_to_play, possible_opposite_corner])

		# 7. Play in the corner
		for subgame_to_play in possible_subgames:
			subgame_state = node.ttt[subgame_to_play]	
			possible_corner = subgame_state.PossibleCorner()
			if possible_corner != None:
				return node.DoMove([subgame_to_play,possible_corner])

		# 8. Play in one side
		for subgame_to_play in possible_subgames:
			subgame_state = node.ttt[subgame_to_play]	
			possible_side = subgame_state.PossibleSide()
			if possible_side != None:
				return node.DoMove([subgame_to_play, possible_side])


def MCCompleteGame(node,b_MC):
	"""
	Performs a complete game between two different AIs
	Inputs :
		node - 
		b_MC -

	"""
	while(1):
		
		# inteligent player plays
		#node = MCIteration(node,b_MC)
		#node = RandomPlayer(node)
		node = MCSearchParallelv2(node,b_MC)
		##print node

		#check if complete
		try:
			if node.CheckComplete():
			##print 'FINITO !!!!!!!!!!!!!!!!!!!'
			##print node
				#print 'XXXXXXXXXX'
				print 'Win :', node.win
				#print node
				#print node.args
				break
		except:
			print 'erroooooooooooooooooooooooooo4'
			print node
			print node.args
		
		#print 'RandomPlayer Moved ---------------------------'
		#print node
		#print node.args, node.complete

		node = MCTreeSearchIteration(node,10*b_MC)
		#node = FinishSquarePlayer(node)
		#node = RandomPlayer(node)
		##print node

		#check if complete
		try:
			if node.CheckComplete():
			##print 'FINITO !!!!!!!!!!!!!!!!!!!'
			##print node
				#print 'OOOOOOOOOOOOOO'
				print 'Win :', node.win
				#print node
				#print node.args
				break
		except:
			print 'erroooooooooooooooooooooooooo5'
			print node
			print node.args

		#print node
		#print node.args, node.complete

# -----------------------------------------------------------------------------------
# Serial version of Monte Carlo Search

def CreateProbes(node,b_MC):
	"""
	Creates probes for a given node
	Inputs:
		node - current node
		b_MC - number of probes created per successor
	Outputs:
		list_probes - list with possible successor states of current node 
					  (might contain repetitions)
	"""
	
	# check possible moves
	possible_moves = node.PossibleMoves()
	n_moves = len(possible_moves)

	# if none return empty list (draw case)
	if n_moves == 0:
		return []

	# if not an empty list
	else :
		# generate random choice of moves
		list_moves = [possible_moves[randint(0,n_moves-1)] for i in range(b_MC)]
		
		# generate probes based on those moves
		list_probes = [node.DoMove(move) for move in list_moves]

		return list_probes
	
def SendProbe(node):
	"""
	Sends probes by simulating a full random game until terminal state is reached
	Inputs:
		node - current node
	Outputs:
		result - final winner of game

	"""

	#try:
	possible_moves = node.PossibleMoves()
	n_moves = len(possible_moves)

	# if probe reached end send final result				
	if n_moves == 0:
		return node.win

	# if not keep going by making a random move
	else:	
		move = possible_moves[randint(0,n_moves-1)]
		node.DoMove2(move)
		return SendProbe(node)


def MCSearch(node,b_MC):
	"""
	Implements Monte Carlo Search, without any parallelization
	Inputs:
		node - current node
		b_MC - number of probes created per successor to perform MC search
	Returns:
		final_successor - successor node which obtained the best overall score
	"""

	#create all possible successors
	successors = node.Expand()

	# if any successor is goal state, return it
	# this way we avoid sending probes when not needed
	for successor in successors:
		if successor.CheckComplete():
			if successor.win == 1:
				return successor

	#case no successor is goal state	
	result_max = INTMIN
	for successor in successors:

		result = 0
		
		#create probes for this successor
		probes = CreateProbes(successor,b_MC)
		
		# if no probes were created means it is a dead end (draw)
		# cannot be loss otherwise game would have already ended
		if(len(probes)) == 0:
			result = node.win
		# in case the game did not end (probes available)
		# send probes and update result for all probes
		else:
			for probe in probes:
				result = result + SendProbe(probe)

		# if this successor has the best observed result 
		# store it as the best choice
		if result > result_max:
			final_successor = successor
			result_max = result

	return final_successor

# -----------------------------------------------------------------------------------
# Parallelized versions of Monte Carlo Search

def MCSearchParallel(node,b_MC):	
	"""
	Implements Monte Carlo Search, where the sending of probes is parallelized
	using the multiprocessing module
	Inputs:
		node - current node
		b_MC - number of probes created per successor to perform MC search
	Returns:
		final_successor - successor node which obtained the best overall score
	"""

	# possible successors
	successors = node.Expand()

	# if any successor is goal state, return it
	# this way we avoid sending probes when not needed
	for successor in successors:
		if successor.CheckComplete():
			if successor.win == 1:
				return successor

	
	def SendProbeParallel(node,result):
		"""
		Sends probes by simulating a full random game until terminal state is reached.
		Auxiliary to MCSearchParallel 
		Inputs:
			node - current node
		Outputs:
			result - final winner of game

		"""	
		possible_moves = node.PossibleMoves()
		n_moves = len(possible_moves)

		# if probe reached end send final result				
		if n_moves == 0:
			result.put(node.win)

		# if not keep going by making a random move
		else:	
			move = possible_moves[randint(0,n_moves-1)]
			node.DoMove2(move)
			SendProbeParallel(node,result)

		
	# case no successor is goal state	
	result_max = INTMIN
	for successor in successors:

		# stores sum of node final probe values
		result = 0
		
		# create probes for this successor
		probes = CreateProbes(successor,b_MC)
		
		# if no probes were created means it is a dead end (draw)
		# cannot be loss otherwise game would have already ended
		if(len(probes)) == 0:
			result = node.win

		# in case the game did not end (probes available)
		# send probes and update result for all probes
		else:
			output = mp.Queue()
			processes = [mp.Process(target=SendProbeParallel, args=(probes[x], output)) for x in range(b_MC)]
			for p in processes:
				p.start()
			for p in processes:
				p.join()
			
			# collect results from each probe and calculate 
			# total score
			results = [output.get() for p in processes]
			for result_probe in results:
				result += result_probe

		# if this successor has the best observed result 
		# store it as the best choice
		if result > result_max:
			final_successor = successor
			result_max = result
	
	return final_successor

	
def MCSearchParallelv2(node,b_MC):
	"""
	Implements Monte Carlo Search, where the creation and sending of probes is parallelized
	using the multiprocessing module
	Inputs:
		node - current node
		b_MC - number of probes created per successor to perform MC search
	Returns:
		final_successor - successor node which obtained the best overall score
	"""

	def CreateSendProbesParallel(node,b_MC,n_successor,output):

		result = 0
		probes = CreateProbes(node,b_MC)

		# if no probes were created means it is a dead end (draw)
		# cannot be loss otherwise game would have already ended
		if(len(probes)) == 0:
			output.put([n_successor,node.win])

		#in case the game did not end with (probes available)
		#send probes and update result for all probes
		for probe in probes:
			##print 'Probe Launched'
			##print probe
			result = result + SendProbe(probe)

		output.put([n_successor,result])


	successors = node.Expand()

	# if any successor is goal state, return it
	# this way we avoid sending probes when not needed
	for successor in successors:
		if successor.CheckComplete():
			if successor.win == 1:
				return successor

	# case no successor is goal state	
	result_max = INTMIN
	# creation and sending of probes
	output = mp.Queue()
	processes = [mp.Process(target=CreateSendProbesParallel, args=(successors[x],b_MC,x,output)) for x in range(len(successors))]
	for p in processes:
		p.start()
	for p in processes:
		p.join()

	# collect results from each successor
	# and choose the one which maximizes its value
	results = [output.get() for p in processes]	
	for result in results:
		if result[1]>result_max:
			final_successor = successors[result[0]]
			result_max = result[1]

	return final_successor

# -----------------------------------------------------------------------------------
# Monte Carlo Search with some domain knowledge enforcing choices

def MCMixed(node,b_MC):
	"""
	Implements Monte Carlo Search with some domain knowledge, also makes use of MCSearchParallelv2 
	Inputs:
		node - current node
		b_MC - number of probes created per successor to perform MC search
	Returns:
		final_successor - successor node which obtained the best overall score OR follows 
						  policy defined by domain knowledge
	"""
	player = node.turn
	if player == 'X':
		opponent = 'O'
	else:
		opponent = 'X'

	# check if all possible moves are associated 
	# with the same subgame or if it is possible to 
	# choose which subgame to play in 
	# (this happens when you are sent to a subgame which was already won)

	possible_moves = node.PossibleMoves()
	same_subgame = True

	for move in possible_moves:
		if move[0] != possible_moves[0][0]:
			same_subgame = False
			break

	if same_subgame:
		subgame_to_play = possible_moves[0][0]
		subgame_state = node.ttt[subgame_to_play]

		# 1. Check if it can win subgame, if so win subgame
		possible_win = subgame_state.CheckPossibleWin(player)
		if possible_win != None:
			#print 'Win Game Situation'
			return node.DoMove([subgame_to_play,possible_win])

		# 2. Check if opponent can win subgame, if so block
		possible_loss = subgame_state.CheckPossibleWin(opponent)
		if possible_loss != None:
			return node.DoMove([subgame_to_play, possible_loss])

		# 3. If none of the above use MCSearch
		else :
			return MCSearchParallelv2(node,b_MC)

	else:
		possible_squares = []
		for move in possible_moves:
			if move[0] not in possible_squares:
				possible_squares.append(move[0])

		# 1. Check if it can win subgame, if so win subgame
		for subgame_to_play in possible_squares:
			subgame_state = node.ttt[subgame_to_play]
			possible_win = subgame_state.CheckPossibleWin(player)
			
			if possible_win != None:
				return node.DoMove([subgame_to_play,possible_win])

		# 2. Check if opponent can win subgame, if so block
		for subgame_to_play in possible_squares:
			subgame_state = node.ttt[subgame_to_play]
			possible_loss = subgame_state.CheckPossibleWin(opponent)
			if possible_loss != None:
				return node.DoMove([subgame_to_play, possible_loss])

		# 3. If none of the above use MCSearch
		return MCSearchParallelv2(node,b_MC)

# -----------------------------------------------------------------------------------
# Monte Carlo Tree Search

def MCTreeSearch(root_node,n_expansions):
	"""
	Implements Monte Carlo Tree Search
	Inputs:
		root_node 	 - current node where tree starts
		n_expansions - number of full games to be simulated from root node
	Returns:
		final_successor - successor node which obtained the best overall score
	"""

	# key is node position in Tree, value is list with successors position in Tree
	successor_Dict = {}
	# key is node position in Tree, value is parent position in Tree
	parent_Dict = {}

	# stores all tree
	Tree =  [root_node]

	# expand root node and add its first successors
	successors = root_node.Expand()
	parent_Dict[0] = None
	successor_Dict[0] = [i+1 for i in range(len(successors))]
	for i in range(len(successors)):
		Tree.append(successors[i])
		parent_Dict[i+1] = 0

	# auxiliary to check all possibile games starting from 
	# a given node were already explored. 
	full_explored_list = [0 for i in range(len(Tree))]
	# if this has happened TREE_COMPLETE will become True
	TREE_COMPLETE = False

	for i in range(n_expansions):
		
		# always start at the root node
		current_node = root_node
		position_tree = 0
		
		# search until leaf node is found
		# while node reached was already expanded 
		# successor_Dict has an element
		# which key is the position of the given node
		# in the 'Tree' array
		while(position_tree in successor_Dict):

			# get all current_node successors positions 
			successor_position = successor_Dict[position_tree]
			value_max = INTMIN
			for position in successor_position:
				# check if there are still possibilities not explored
				# after this successor node
				if full_explored_list[position] == 0:
					# calculate UCB1 value for this node
					value = Tree[position].UCB1(current_node.ni)

					# if new max value observed
					# update as best choice to select as next node	
					if value > value_max:
						value_max = value
						best_position = position

			# case in which every successor of the current node
			# has run out of options
			if value_max == INTMIN:
				full_explored_list[position_tree] = 1 
				position_tree = parent_Dict[position_tree]
				# case were we went all the way back to the root node 
				# we move out of this loop and will evaluate best
				# successor option knowing the complete tree
				if position_tree == None:
					TREE_COMPLETE = True
					break
				# if we are not at the root node go back to the
				# parent node and select a new successor which still 
				# has not yet visited full gameplays
				else:
					current_node = Tree[position_tree]
				
			# if there are still succesors that have unnexplored options
			# update current node with best successor option
			else:
				current_node = Tree[best_position]
				position_tree = best_position

		# case full tree was discovered, just break the loop
		if TREE_COMPLETE:
			break

		last_node = current_node
		
		# check if it is the first time leaf node is reached
		if last_node.ni == 0 :
			# check if it is terminal node
			if last_node.CheckComplete():
				full_explored_list[position_tree] = 1
			# if not send random probe
			result = SendProbe(last_node.Copy())	
		else :
			# get all successors
			last_node = last_node.Expand()
			# add dictionary entry with positions of last_node successors in Tree array
			initial_length_tree = len(Tree)
			successor_Dict[position_tree] = [initial_length_tree+i for i in range(len(last_node))]
			# add successors to Tree
			for i in range(len(last_node)):
				Tree.append(last_node[i])
				full_explored_list.append(0)
				parent_Dict[initial_length_tree+i] = position_tree
			# choose first successor and send probe
			last_node = last_node[0].Copy()
			position_tree = successor_Dict[position_tree][0]
			result = SendProbe(last_node)

		current_node = last_node
		# backtrack and update results
		# along the way
		while True:
			# update score and ni
			current_node.score += result			
			current_node.ni += 1
			# if state is root break
			if position_tree == 0:
				break
			# else update current_node	
			position_tree = parent_Dict[position_tree]
			current_node = Tree[position_tree]

	#choose successor with best outcome
	first_successors_positions = successor_Dict[0]
	best_score = -1.1
	best_successor = None
	for position in first_successors_positions:
		score = Tree[position].Score()	
		print score, Tree[position].score , Tree[position].ni
		if score > best_score:
			best_score = score
			best_successor = Tree[position]

	return best_successor