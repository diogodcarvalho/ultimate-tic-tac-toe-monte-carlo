
import sys
import time
import pygame
from tictactoe import *
from mc_tree import *

# RGB color codes
WHITE = (255,255,255)
BLACK = (0,0,0)
RED   = (255,0,0)
GREEN = (0,255,0)
BLUE  = (0,0,255)
LIGHTRED = (255,204,204)
LIGHTBLUE = (173,216,230)

# Useful window size values
WINDOW_WIDTH  = 720
WINDOW_HEIGHT = 720
XMARGIN = 50
YMARGIN = 50
GAPSIZE = 10
BOXSIZE = 200
XMARGIN2 = 5
YMARGIN2 = 5
GAPSIZE2 = 5
BOXSIZE2 = 60
XMARK = 'X'
OMARK = 'O'
XCOLOR = BLUE
OCOLOR = RED
DCOLOR = GREEN
OCOLORLIGHT = LIGHTRED
XCOLORLIGHT = LIGHTBLUE


# Initialize font module
pygame.font.init()
# font to write win message
WIN_FONT = pygame.font.SysFont(None,150)
# font to write on tiles
SMALL_FONT = pygame.font.SysFont('Helvetica', 70)
BIG_FONT = pygame.font.SysFont('Helvetica', 320)


def main(argv):

	global GAMEDISPLAY

	# initial game
	TTT = ultimate_tictactoe()

	pygame.init()
	# initiate window with given size
	GAMEDISPLAY = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
	# set title of window
	pygame.display.set_caption('Ultimate TicTacToe')
	
	# fill window 
	GAMEDISPLAY.fill(WHITE)
	# draw grid
	DrawLines()
	# update display
	pygame.display.update()

	# mouse positions
	mouse_x = 0
	mouse_y = 0
	player = 'X'
	
	# player starts the game
	player_turn = True
	AI_turn = False
	button_pressed = False
	# list boxes available for next play
	allowed_boxes = range(9)
	# list of finished games
	subgame_closed = [False]*9

	# end game flag
	gameExit = False
	

	def Redraw(TTT, next_player, previous_boxes, next_boxes):

		# remove highlight from previous boxes
		if isinstance(previous_boxes,int):
			previous_boxes = [previous_boxes]
		for box in previous_boxes:
			HighlightBox(box,WHITE)
		
		# highlight boxes where next plays can occur
		if isinstance(next_boxes,int):
			next_boxes = [next_boxes]
		for box in next_boxes:
			if next_player == 'X':
				HighlightBox(box,XCOLORLIGHT)
			else:
				HighlightBox(box,OCOLORLIGHT)

		# redraw lines
		DrawLines()

		# redraw small 'X', 'O' symbols
		for box1,subgame in enumerate(TTT.ttt):
			for box2,value in enumerate(subgame):
				if value != '-':
					MarkBox(box1,box2,value,SMALL_FONT)

		# draw if needed big 'X', 'O' symbols
		for subgame,subgame_winner in enumerate(TTT.args):
			if subgame_winner != '-' and not(subgame_closed[subgame]):
				subgame_closed[subgame] = True
				if subgame_winner == 'X':
					color = XCOLOR
				elif subgame_winner == 'O':
					color = OCOLOR	
				else:
					color = DCOLOR

				text = BIG_FONT.render(subgame_winner, True, color)
				surface = pygame.Surface((BOXSIZE,BOXSIZE))
				surface.fill(WHITE)
				text_surface = text.get_rect()
				text_surface.center = surface.get_rect().center
				text_surface.centery += 12
				surface.blit(text,text_surface)
				surface.set_alpha(100)
				GAMEDISPLAY.blit(surface, TopLeftCornerOfBox(subgame,0))

		# update display
		pygame.display.update()

	Redraw(TTT,'X',0,allowed_boxes)

	while not gameExit:

		# check pygame.event 
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameExit = True
			elif event.type == pygame.MOUSEMOTION:
				mouse_x, mouse_y = event.pos
				pygame.display.update()
			elif event.type == pygame.MOUSEBUTTONUP:
				mouse_x, mouse_y = event.pos
				button_pressed = True 
				print mouse_x,mouse_y

		if player_turn and button_pressed:
			# disable pressed button flag
			button_pressed = False
			# check which box was pressed
			box1,box2 = GetBox(mouse_x,mouse_y)
			print 'Player X : ', box1, box2
			# check if it is a valid box
			if box1 != None and box2 != None:
				# check if it selected subgame corresponds to the one we are supposed to play in
				if (TTT.args[box1] == '-' and box1 == TTT.subgame_to_play) or (TTT.args[TTT.subgame_to_play] != '-' and TTT.args[box1] == '-') or allowed_boxes == range(9):
					# check if square selected in that subgame is not yet filled
					if TTT.ttt[box1].args[box2] == '-':
						# do move 
						TTT = TTT.DoMove([box1,box2])
						# determine boxes where next player can play	
						allowed_moves_next = TTT.PossibleMoves() 
						allowed_boxes_next = set([moves[0] for moves in allowed_moves_next])
						# redraw game
						Redraw(TTT,'O',allowed_boxes,allowed_boxes_next)
						
						# check if game is finished
						if TTT.CheckComplete():
							if TTT.win == 0:
								print 'DRAW'
								message_to_screen('DRAW', GREEN)
							else: 
								print 'X WINS'
								message_to_screen('X WINS', XCOLOR)
							pygame.display.update()
							time.sleep(5)
							gameExit = True

						else:
							# change turn
							player_turn = False
							AI_turn = True
							allowed_boxes = allowed_boxes_next

		elif AI_turn:
			# choose which AI you want to play against
			# TTT = FinishSquarePlayer(TTT)
			# TTT = MCSearchParallel2(TTT,100)
			# TTT = MCMixed(TTT,1000)
			TTT = MCTreeSearch(TTT,1000)

			box1,box2 = TTT.move[0], TTT.move[1]
			print 'Player O:', box1,box2

			# determine boxes where next player can play	
			allowed_moves_next = TTT.PossibleMoves() 
			allowed_boxes_next = set([moves[0] for moves in allowed_moves_next])
			# redraw game
			Redraw(TTT,'X',allowed_boxes,allowed_boxes_next)

			# check if game is finished
			if TTT.CheckComplete():
				if TTT.win == 0:
						print 'DRAW'
						message_to_screen('DRAW', GREEN)
				else: 
					print 'O WINS'
					message_to_screen('O WINS', OCOLOR)
				pygame.display.update()
				time.sleep(5)
				gameExit = True	

			else:
				# change turn
				AI_turn = False
				player_turn = True
				allowed_boxes = allowed_boxes_next
				

	pygame.quit()
	quit()
		

def TileCoordinate(posx,posy):

	tile1x = None
	tile1y = None
	tile2x = None
	tile2y = None
	
	for i in range(3):
		if((posx> XMARGIN + i*(BOXSIZE+GAPSIZE)) and (posx < XMARGIN + BOXSIZE + i*(BOXSIZE + GAPSIZE))):
			tile1x = i
		if((posy> YMARGIN + i*(BOXSIZE+GAPSIZE)) and (posy < YMARGIN + BOXSIZE + i*(BOXSIZE + GAPSIZE))):
			tile1y = i

	if tile1x != None and tile1y != None:

		xmin = XMARGIN + tile1x*(BOXSIZE+GAPSIZE) + XMARGIN2
		ymin = YMARGIN + tile1y*(BOXSIZE+GAPSIZE) + YMARGIN2
		for i in range(3):
			if((posx> xmin + i*(BOXSIZE2 + GAPSIZE2)) and (posx < xmin + BOXSIZE2 + i*(BOXSIZE2 + GAPSIZE2))):
				tile2x = i
			if((posy> ymin + i*(BOXSIZE2 + GAPSIZE2)) and (posy < ymin + BOXSIZE2 + i*(BOXSIZE2 + GAPSIZE2))):
				tile2y = i

	return tile1x, tile1y, tile2x, tile2y

def HighlightBox(new_box,color):

	tx = new_box%3
	ty = new_box/3

	left = XMARGIN - GAPSIZE+ tx*(BOXSIZE+GAPSIZE) 
	top  = YMARGIN - GAPSIZE+ ty*(BOXSIZE+GAPSIZE)
	width = BOXSIZE + 2*GAPSIZE #GAPSIZE	
	height = BOXSIZE + 2*GAPSIZE

	Rect = pygame.Rect(left,top,width,height)
	pygame.draw.rect(GAMEDISPLAY,color,Rect)


def GetBox(posx,posy):
	t1x,t1y,t2x,t2y = TileCoordinate(posx,posy)
	box1 = None
	box2 = None
	if t2x != None and t2y != None:
		box1 = t1x + 3*t1y
		box2 = t2x + 3*t2y

	return box1,box2

def TopLeftCornerOfBox(box1,box2):
	t1x = box1%3
	t1y = box1/3
	t2x = box2%3
	t2y = box2/3
	topx = XMARGIN + t1x*(BOXSIZE+GAPSIZE) + t2x*(BOXSIZE2 + GAPSIZE2) 
	topy = YMARGIN + t1y*(BOXSIZE+GAPSIZE) + t2y*(BOXSIZE2 + GAPSIZE2)
	return topx,topy

def CenterOfBox(box1,box2):
	t1x = box1%3
	t1y = box1/3
	t2x = box2%3
	t2y = box2/3
	centerx = XMARGIN + t1x*(BOXSIZE+GAPSIZE) + XMARGIN2 + t2x*(BOXSIZE2 + GAPSIZE2) + BOXSIZE2/2
	centery = YMARGIN + t1y*(BOXSIZE+GAPSIZE) + YMARGIN2  + t2y*(BOXSIZE2 + GAPSIZE2) + BOXSIZE2/2	
	return centerx, centery

def MarkBox(box1,box2,player,SMALL_FONT):
	centerx, centery = CenterOfBox(box1,box2)
	print centerx, centery

	if player == 'X':
		color = XCOLOR
	elif player == 'O':
		color = OCOLOR

	if centerx != None and centery != None:
		mark = SMALL_FONT.render(player, True, color)
		markRect = mark.get_rect()
		markRect.centerx = centerx
		markRect.centery = centery
		GAMEDISPLAY.blit(mark, markRect)

def DrawLines():
	
	# -------------------------MAIN GAME LINES --------------------------------
	
	# VERTICAL
	left = XMARGIN + BOXSIZE
	top = YMARGIN
	width = GAPSIZE
	height = WINDOW_HEIGHT-2*YMARGIN
	
	vertRect1 = pygame.Rect(left, top, width, height)
	pygame.draw.rect(GAMEDISPLAY, BLACK, vertRect1)

	vertRect2 = pygame.Rect(left + BOXSIZE + GAPSIZE, top, width, height)
	pygame.draw.rect(GAMEDISPLAY, BLACK, vertRect2)

	vertRect3 = pygame.Rect(left  - BOXSIZE - GAPSIZE, top, width, height)
	pygame.draw.rect(GAMEDISPLAY, BLACK, vertRect3)

	vertRect4 = pygame.Rect(left + 2*BOXSIZE + 2*GAPSIZE, top, width, height)
	pygame.draw.rect(GAMEDISPLAY, BLACK, vertRect4)

	# HORIZONTAL
	left = XMARGIN
	top = YMARGIN + BOXSIZE
	width = WINDOW_HEIGHT-2*XMARGIN
	height = GAPSIZE
	
	horizRect1 = pygame.Rect(left, top, width, height)
	pygame.draw.rect(GAMEDISPLAY, BLACK,  horizRect1)

	horizRect2 = pygame.Rect(left, top + BOXSIZE + GAPSIZE, width, height)
	pygame.draw.rect(GAMEDISPLAY, BLACK, horizRect2)

	horizRect3 = pygame.Rect(left- GAPSIZE, top - BOXSIZE - GAPSIZE, width+2*GAPSIZE, height)
	pygame.draw.rect(GAMEDISPLAY, BLACK,  horizRect3)

	horizRect4 = pygame.Rect(left- GAPSIZE, top + 2*BOXSIZE + 2*GAPSIZE, width+2*GAPSIZE, height)
	pygame.draw.rect(GAMEDISPLAY, BLACK, horizRect4)

	# ------------------------- SMALL GAME LINES --------------------------------

	# VERTICAL
	for i in range(3):
		for j in range(3):
			left = XMARGIN + XMARGIN2 + BOXSIZE2 + i*(BOXSIZE+GAPSIZE)
			top  = YMARGIN + YMARGIN2 + j*(BOXSIZE+GAPSIZE)
			width = GAPSIZE2	
			height = BOXSIZE - 2*YMARGIN2

			vertRect1 = pygame.Rect(left, top, width, height)
			pygame.draw.rect(GAMEDISPLAY, BLACK, vertRect1)

			vertRect2 = pygame.Rect(left + BOXSIZE2 + GAPSIZE2, top, width, height)
			pygame.draw.rect(GAMEDISPLAY, BLACK, vertRect2)

	# HORIZONTAL
	for i in range(3):
		for j in range(3):
			left = XMARGIN + XMARGIN2 + i*(BOXSIZE+GAPSIZE)
			top  = YMARGIN + YMARGIN2 + BOXSIZE2 + j*(BOXSIZE+GAPSIZE)
			width = BOXSIZE - 2*XMARGIN2 
			height = GAPSIZE2	

			vertRect1 = pygame.Rect(left, top, width, height)
			pygame.draw.rect(GAMEDISPLAY, BLACK, vertRect1)

			vertRect2 = pygame.Rect(left, top + BOXSIZE2 + GAPSIZE2, width, height)
			pygame.draw.rect(GAMEDISPLAY, BLACK, vertRect2)

def message_to_screen(msg,color):

	left = WINDOW_WIDTH/2-250
	top  = WINDOW_HEIGHT/2-100
	width = 500	
	height = 200

	Rect1 = pygame.Rect(left, top, width, height)
	pygame.draw.rect(GAMEDISPLAY, color, Rect1)
	
	screen_text = WIN_FONT.render(msg, True, WHITE)
	GAMEDISPLAY.blit(screen_text,[WINDOW_WIDTH/2-190,WINDOW_HEIGHT/2-50])

if __name__ == "__main__":
	
	main(sys.argv)

