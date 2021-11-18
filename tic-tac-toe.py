#!/usr/bin/python3
from random import choice
from itertools import permutations
from math import inf
from sys import exit

def play_again():
	return 'y' in input(" Do you want to play a game?\n > ").lower()

def print_table(table):
	print('\n', '\n '.join([' '.join(row) for row in table]), end='\n\n')

def do_move(tic_tac_screen, move, piece):
	tic_tac_screen[(move - 1) // 3][(move - 1) % 3] = piece
	return move

def winner(moves):
	winning_combinations = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7),
							(2, 5, 8), (3, 6, 9), (1, 5, 9), (3, 5, 7)]
	for moves in permutations(moves, 3):
		if moves in winning_combinations:
			return True
	return False

def computer_move_wins(tic_tac_screen, player_moves, computer_moves):
	depth = len(
		set(range(1, 10)).difference(player_moves.union(computer_moves)))
	computer_moves.add(
		do_move(tic_tac_screen,
			minimax(player_moves, computer_moves, True, depth)[0],
			"\x1B[31mo\x1B[m"))
	if winner(computer_moves):
		print_table(tic_tac_screen)
		return True
	return False

def minimax(player_moves, computer_moves, computer, depth):
	best = [-1, -inf] if computer else [-1, +inf]
	if (depth == 0) or (winner(player_moves) or winner(computer_moves)):
		outcome = +1 if winner(computer_moves) else (
			-1 if winner(player_moves) else 0)
		return [-1, outcome]
	
	for move in set(range(1,10)).difference(player_moves.union(computer_moves)):
		if computer:
			computer_moves.add(move)
			score = [move, minimax(
				player_moves, computer_moves, not computer, depth - 1)[1]]
			computer_moves.remove(move)
			if score[1] > best[1]:
				best = score
		else:
			player_moves.add(move)
			score = [move, minimax(
				player_moves, computer_moves, not computer, depth - 1)[1]]
			player_moves.remove(move)
			if score[1] < best[1]:
				best = score
	return best

def player_move_wins(tic_tac_screen, player_moves, computer_moves):
	attempt = int(input(" Input the number that corresponds to the area\n > "))
	while attempt in player_moves.union(computer_moves):
		print("That area is occupied. Try again.")
		attempt = int(input("Input the number that corresponds to the area: "))
	player_moves.add(do_move(tic_tac_screen, attempt, "\x1B[32mx\x1B[m"))
	if winner(player_moves):
		print_table(tic_tac_screen)
		return True
	return False

def is_tie(tic_tac_screen, player_moves, computer_moves):
	if (len(computer_moves) + len(player_moves)) >= 9:
		print_table(tic_tac_screen)
		return True
	return False

def start():
	player_moves = set()
	computer_moves = set()
	tic_tac_screen = [[str(i+j) for j in range(3)] for i in range(1, 9, 3)]
	
	while True:
		print_table(tic_tac_screen)
		if player_move_wins(tic_tac_screen, player_moves, computer_moves):
			return print("You Win! (Player Wins)")
		if is_tie(tic_tac_screen, player_moves, computer_moves):
			return print("Tie Game")
		if computer_move_wins(tic_tac_screen, player_moves, computer_moves):
			return print("You Lose! (Computer Wins)")
		if is_tie(tic_tac_screen, player_moves, computer_moves):
			return print("Tie Game")

if __name__ == "__main__":
	try:
		while play_again():
			try: start()
			except (KeyboardInterrupt, EOFError):
				print("\n Resigned game")
	finally:
		exit()
