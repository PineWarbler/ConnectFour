# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 21:52:57 2022

@author: REYNOLDSPG21
"""

# modified version from: https://github.com/KeithGalli/Connect4-Python/blob/master/connect4_with_ai.py
# all pygame functionality has been commented out

# average minimax step time on RPi is:  5.428 ± 1.152s, a significant improvement over the 25s step time with the previous implementation of minimax

import numpy as np
import random
# import pygame
import sys
import math

# note that input board is flipped vertically 180 degrees!!! to revert the flip, use np.flip(board, 0)


# BLUE = (0,0,255)
# BLACK = (0,0,0)
# RED = (255,0,0)
# YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

# SEARCH_DEPTH = 5

WINDOW_LENGTH = 4 # this is number of consecutive tokens needed to win

def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def print_board(board):
	print(np.flip(board, 0))

def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

def evaluate_window(window, piece):
	score = 0
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 4

	return score

def score_position(board, piece):
	score = 0

	## Score center column
	center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	## Score Horizontal
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLUMN_COUNT-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score Vertical
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score posiive sloped diagonal
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	return score

def is_terminal_node(board):
	return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, AI_PIECE):
				return (None, 100000000000000)
			elif winning_move(board, PLAYER_PIECE):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(board, AI_PIECE))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, AI_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, PLAYER_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations

def pick_best_move(board, piece):

	valid_locations = get_valid_locations(board)
	best_score = -10000
	best_col = random.choice(valid_locations)
	for col in valid_locations:
		row = get_next_open_row(board, col)
		temp_board = board.copy()
		drop_piece(temp_board, row, col, piece)
		score = score_position(temp_board, piece)
		if score > best_score:
			best_score = score
			best_col = col

	return best_col

# This one-liner function checks for floating pieces (author: Peter Reynolds)
# do whole board at once
def get_board_validity(board):
    return np.array_equal(np.flip(np.cumprod(np.flip(board, 0), axis=0), 0), board) # explanation: in this column-wise cumprod, all elements following a zero (empty space) are turned into zeros, so all spaces above an empty space must also be empty.  If the rest of the observed column does not exhibit this behavior, board is invalid

"""
AUTHOR: Connor Felton
This function ensures that the board's current state is valid.
Good for making sure there were no issues when translating the picture to a board.
Returns true if the state is valid, false otherwise.
Only call if the player or AI has already placed a piece.
"""
def board_is_valid(board, first_player, current_player, turns):
	aiPieces = 0
	playerPieces = 0
	bad_if_air = False
	# ^ This variable tracks if an empty piece was found in the column.
	#   If this is True and a non-empty piece is found (there is a floating piece,)
	#   then the board is invalid.

	# Count all pieces. Make sure no pieces are floating.
	for i in range(7): # Every column
		bad_if_air = False
		for j in range(6): # Each row of the column
			if (board[j][i]==PLAYER_PIECE):
				if (bad_if_air):
					return False
				playerPieces += 1
			elif (board[j][i]==AI_PIECE):
				if (bad_if_air):
					return False
				aiPieces += 1
			else:
				bad_if_air = True

	# If the total number of pieces is wrong, return false.
	if (turns != (aiPieces + playerPieces)):
		return False
	
	# Ensure that the number of each piece is valid.
	if (first_player == current_player):
		# If the player that moved first just moved, they should have 1 more chip than the opponent.
		if (current_player == PLAYER):
			return (playerPieces - aiPieces) == 1
		else:
			return (aiPieces - playerPieces) == 1
	else:
		# Otherwise, both players should have equal pieces.
		return (playerPieces == aiPieces)
		
		

"""
AUTHOR: Connor Felton, some code borrowed from original pygame implementation.
This function plays a single game of Connect 4 against the player.
"""
def play_game(depth):
	no_winner = True
	detect_errors = True # Always True unless the user decides to ignore errors.
	invalid = False

	#Set up the game.
	turn = random.randint(PLAYER, AI)
	totalTurns = 0
	first_player = turn
	board = create_board()

	#Play until a player wins.
	while (no_winner):
		if (turn == PLAYER):
			print("Player's turn. Waiting for player...")
			
			# TODO: Code here that waits until a new piece is detected. Update board state.
			
			# TEMPORARY CODE: The real program should get board state from images, not the keyboard.
			col = int(input(" > ")) - 1
			if (is_valid_location(board, col)):
				row = get_next_open_row(board, col)
				drop_piece(board, row, col, PLAYER_PIECE)
			else:
				print("Invalid column")

			totalTurns += 1

			# Make sure the board is valid.
			'''if (board_is_valid(board, first_player, turn, totalTurns) == False):
				invalid = True
			else:
				invalid = False'''
				
			invalid = not board_is_valid(board, first_player, turn, totalTurns) # simplified by P. Reynolds from the above if-else implementation
			
			while (detect_errors and invalid):
				print_board(board)
				print("Board invalid. Select an option:\n 1. Read board state again\n 2. Ignore error and try to keep playing\n 3. End game")
				option = int(input(">>> "))
				if (option == 1):
					# TODO: The robot should attempt to read the board again.
					#       Ideally, it will try several times before asking the user what to do.
					if (board_is_valid(board, first_player, turn) == False):
						invalid = True
					else:
						invalid = False
				elif (option == 2):
					print("Will attempt to keep playing. Error checking disabled.")
					detect_errors = False
				else:
					print("Game Terminated.")
					return

			# Check if the player has won.
			if (winning_move(board, PLAYER_PIECE)):
				print("Player wins!")
				no_winner = False
			
			# Print the board so that the user can make sure the game is working correctly.
			# Pass the turn to the AI.
			print_board(board)
			turn = AI
		else:
			print("AI's turn.")

			# Minimax and drop the piece.
			col, score = minimax(board, depth, -math.inf, math.inf, True)
			if (is_valid_location(board, col)):
				row = get_next_open_row(board, col)
				drop_piece(board, row, col, AI_PIECE)
			else:
				# I don't know how the AI would ever pick an invalid column, but if it does, ask the user what to do.
				print("AI chose invalid column. Select an option:\n 1. Pick a column and keep playing.\n 2. Stop playing.")
				if (int(input(">>> ")) != 1):
					# Quit the game.
					return
				# Find a valid column to drop a piece so as to prevent future errors.
				for i in range(7):
					if (is_valid_location(board, col)):
						row = get_next_open_row(board, col)
						drop_piece(board, row, col, AI_PIECE)
						break
			
			totalTurns += 1

			# Check if the AI has won.
			if (winning_move(board, AI_PIECE)):
				print("AI wins!")
				no_winner = False

			# Print the board so that the user can make sure the game is working correctly.
			# Pass the turn to the player.
			print_board(board)
			turn = PLAYER


print("Connect 4 Robot")

# Continue playing rounds until the user enters 0 for search depth.
depth = 1
while (depth > 0):
	# Get search depth
	# It is not recommended to use a search depth greater than 5.
	print("\nEnter search depth.\n >= 1: AI difficulty. Higher is harder.\n 0: Quit.")
	depth = input(">>> ")
	depth = int(depth)

	# If the depth is greater than 0, play a round.
	if (depth > 0):
		play_game(depth)

print("Exiting program.")
