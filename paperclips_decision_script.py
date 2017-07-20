#                   PAPERCLIPS: the game
# a game to teach kids money
# written by Jeff Mason, summer 2017
# using Python and the command line
# full rules to the game can be found in RULES.txt

# ----------------------------------------------------------------

# the following code is meant to open the game file
# import the players' names and their closed-out liquid  balances
# and, separately, their bank balances
# note: we must include the gameplay file as a command line argument

from sys import argv
import math

# h/t stackexchange user Boubakr for the following formatting code
# https://stackoverflow.com/questions/8924173/how-do-i-print-bold-text-in-python
class c:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   U = '\033[4m'
   E = '\033[0m'

play = True
payment_amt = 0
script, filename = argv

def update_for_external_processes():
	# 'game_state' variable refers to the opening situation;
	# that is, who are the players, what are their resepctive balances
	game_state = open(filename)

	# the players_line is a single line of text with space-delimited
	# list of players' names; we take this line and turn it into a
	# list object
	# ditto for the players' balances, except that the balances come in as
	# strings, so we must convert each element to a float
	game_state_txt = game_state.read().splitlines()
	players_list_str = game_state_txt[0]
	balances_list_str = game_state_txt[1]
	players = players_list_str[2:-2].split('\', \'')

	# the following turns each element from the balances line
	# into an int, which is necessary to do math,
	# which is of course necessary for the modification of balances
	balances_init = balances_list_str[1:-1].split(', ')
	balances = []
	for i in range(0,len(balances_init)):
		balances.append(float(balances_init[i]))
	game_state.close()
	return players, balances

players, balances = update_for_external_processes()
# a simple function to print a nice, formatted list of players
def print_players(balance_bool, players_list, balances_list):
	for i in range(0,len(players_list)):
		print '\t' + '* ' + c.BLUE + str(players_list[i]) + c.E,
		if (balance_bool == True):
			print '- ' + c.BOLD + str(balances_list[i]) + c.E + u'\u03FC' + '\n'
		else:
			print '\n'
def print_players_choice():
	for i in range(0,len(players)):
		print '\t' + str(i) + '. ' + str(players[i])

# this will update the in-program lists of players and balances
# after an admin has added new players
# note: the balance appended each time is '5'
# this is convention; every new player starts with 5 paperclips
def update_lists(new_plyr):
	players.append(new_plyr)
	balances.append(5.0)
def try_int(user_in):
	dummy = 0
	try:
		dummy = int(user_in)
		return True
	except TypeError:
		return False
	except ValueError:
		return False

# here we update the gamefile
# paperclips is a game in which players' balances roll-over between game sessions
# sort of like a game of pick-up basketball
def update_file(players_list, balances_list):
	writable_file = open(filename, 'w')
	player_str = str(players_list)
	balance_str = str(balances_list)
	writable_file.write(player_str + '\n' + balance_str)
	writable_file.close()
def deposit(players_list, balances_list):
	txn_incomplete = 1
	global payment_amt
	while txn_incomplete == 1:
		if payment_amt != 0:
			deposit_amt = payment_amt
			if try_int(deposit_amt):
				print c.U + "WHO IS RECEIVING PAYMENT?" + c.E
				print '\n',
				print_players_choice()
				print '\n',
				player_choice = raw_input('>')
				print '\n',
				if try_int(player_choice):
					if int(player_choice) in range(0,len(players_list)+1):
						balances_list[int(player_choice)] += int(deposit_amt)
						print "BALANCE UPDATED. %s HAS %d" % (players_list[int(player_choice)], balances_list[int(player_choice)]) + u'\u03FC.'
						update_file(players_list, balances_list)
						txn_incomplete = 0
					else:
						print "INVALID CHOICE."
				else:
					print "NOT A NUMBER!"
			elif deposit_amt == 'X' or deposit_amt == 'x':
				print "CANCELLED."
				txn_incomplete = 0
			else:
				print 'INVALID.'
		else:
			print c.U + "DEPOSIT HOW MUCH?" + c.E + " (\'X\' CANCELS.)\n"
			deposit_amt = raw_input('>')
			print '\n',
			if try_int(deposit_amt):
				print c.U + "WHO IS MAKING THE DEPOSIT?" + c.E + " \'X\' CANCELS."
				print '\n',
				print_players_choice()
				print '\n',
				player_choice = raw_input('>')
				print '\n',
				if try_int(player_choice):
					if int(player_choice) in range(0,len(players_list)+1):
						balances_list[int(player_choice)] += int(deposit_amt)
						print "BALANCE UPDATED. %s HAS %d" % (players_list[int(player_choice)], balances_list[int(player_choice)]) + u'\u03FC.'
						update_file(players_list, balances_list)
						txn_incomplete = 0
					else:
						print "INVALID CHOICE."
				elif player_choice == 'X' or player_choice == 'x' and payment_amt == 0:
					txn_incomplete = 0
				else:
					print "NOT A NUMBER!"
			elif deposit_amt == 'X' or deposit_amt == 'x':
				print "CANCELLED."
				txn_incomplete = 0
			else:
				print 'INVALID.'
def withdraw(players_list, balances_list):
	txn_incomplete = 1
	while txn_incomplete == 1:
		print c.U + "WITHDRAW HOW MUCH?" + c.E + " (\'X\' CANCELS.)\n"
		withdrawal_amt = raw_input('>')
		print '\n',
		if try_int(withdrawal_amt):
			print c.U + "WHO IS MAKING THE WITHDRAWAL?" + c.E + " \'X\' CANCELS."
			print '\n',
			print_players_choice()
			print '\n',
			player_choice = raw_input('>')
			print '\n',
			if try_int(player_choice):
				if int(player_choice) in range(0,len(players)+1):
					if int(withdrawal_amt) <= balances[int(player_choice)]:
						balances[int(player_choice)] -= int(withdrawal_amt)
						print "BALANCE UPDATED. %s HAS %d" % (players[int(player_choice)], balances[int(player_choice)]) + u'\u03FC.'
						update_file(players_list, balances_list)
						global payment_amt
						payment_amt = withdrawal_amt
						txn_incomplete = 0
					else:
						print "SORRY, %s.  YOU DON'T HAVE THAT MUCH MONEY." % players[int(player_choice)]
				else:
					print "INVALID CHOICE."
			elif player_choice == 'X' or player_choice == 'x':
				txn_incomplete = 0
			else:
				print "NOT A NUMBER!"
		elif withdrawal_amt == 'X' or withdrawal_amt == 'x':
			print "CANCELLED."
			txn_incomplete = 0
		else:
			print 'INVALID.'
def borrow():
	print ''

players, balances = update_for_external_processes()
# this prints the players' names
print c.U + "\nPAPERCLIPS HAS BEEN ACTIVATED.  THE PLAYERS ARE:\n",
print c.E
print_players(False, players, balances)

# since we may have new players at the outset, we verify the above
# list is complete
def add_remove_players(players_list, balances_list):
	new_players_loop_exit = 0
	while new_players_loop_exit == 0:
		print "ARE THERE OTHER PLAYERS? (Y/N/D)\n"
		new_players_yn = raw_input('>')
	# here the user has indicated there are players that needed
	# to be added to the gamefile
		if new_players_yn == ('y' or 'Y'):
			print "\nTHERE ARE NEW PLAYERS."
			print c.U + "WHO IS/ARE THE NEW PLAYER(s)?" + c.E + "\n"
			# take input, space-delimited
			joining_the_game = raw_input('>')
			new_players_list = joining_the_game.split(' ')
			for i in range(0,len(new_players_list)):
				# split the space-delimited new player string and kick
				# each element out to updates_lists
				update_lists(new_players_list[i])
			# we update the gamefile itself
			update_file(players_list, balances_list)
			# finally we print the new player list for good measure
			print c.U + "\nTHE UPDATED PLAYER LIST:\n" + c.E
			print_players(False, players, balances)
		# no new players, the game can start
		elif new_players_yn == ('n' or 'N'):
			new_players_loop_exit = 1
			print "\nLET THE GAME BEGIN.\n"
	# come back here and add a delete player functionality
	#	elif new_players_yn == ('d' or 'D'):
	#		print "TBD"
		else:
			print "\nINVALID RESPONSE.\n"

add_remove_players(players, balances)

players, balances = update_for_external_processes()
print "THE PLAYERS' BANK BALANCES ARE AS LISTED:\n"
print_players(True, players, balances)

while play == True:
	print c.U + "WHAT WOULD YOU LIKE TO DO?" + c.E + '\n'
	print c.U + "B" + c.E + "ANK / " + c.U + "T" + c.E + "RADE / " + c.U + "Q" + c.E + 'UIT / ' + c.U + 'A' + c.E + 'DMIN\n'
	decision = raw_input('>')
	print '\n',
	if decision == ('q' or 'Q'):
		play = False
	elif decision == ('t' or 'T'):
		players, balances = update_for_external_processes()
		withdraw(players, balances)
		deposit(players, balances)
		global payment_amt
		payment_amt = 0
	elif decision == ('b' or 'B'):
		print c.U + "AT THE BANK." + c.E
		print c.U + "D" + c.E + "EPOSIT / " + c.U + "W" + c.E + "ITHDRAW / " + c.U + "B" + c.E + 'ORROW\n'
		at_the_bank = raw_input('>')
		print '\n',
		if at_the_bank == ('d' or 'D'):
			players, balances = update_for_external_processes()
			deposit(players, balances)
		elif at_the_bank == ('w' or 'W'):
			players, balances = update_for_external_processes()
			withdraw(players, balances)
		elif at_the_bank == ('b' or 'B'):
			update_for_external_processes()
			borrow()
		else:
			print "CANCELLED."
	elif decision == ('a' or 'A'):
		print c.U + "ADMIN." + c.E + " (\'X\' CANCELS.)\n"
		print c.U + "L" + c.E + "IST BALANCES / " + c.U + "A" + c.E + "DD or REMOVE PLAYERS / " + 'ADJUST ' + c.U + "B" + c.E + "ALANCES\n"
		admin_decision = raw_input('>')
		print '\n',
		if admin_decision == ('l' or 'L'):
			players, balances = update_for_external_processes()
			print_players(True, players, balances)
		elif admin_decision == ('a' or 'A'):
			players, balances = update_for_external_processes()
			add_remove_players(players, balances)
		elif admin_decision == ('b' or 'B'):
			update_for_external_processes()
			borrow()
		else:
			print "CANCELLED."
	else:
		print ''
