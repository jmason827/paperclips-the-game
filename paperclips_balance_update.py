import time
from sys import argv

#print c.U + "D" + c.E + "EPOSIT / " + c.U + "B" + c.E + "UY / " + c.U + "S" + c.E + "ELL / BORRO" + c.U + "W" + c.E + ' / ' + c.U + "Q" + c.E + 'UIT / ' + c.U + 'A' + c.E + 'DMIN\n'
#print c.U + "B" + c.E + "ANK / " + c.U + "T" + c.E + "RADE /" + c.U + "Q" + c.E + 'UIT / ' + c.U + 'A' + c.E + 'DMIN\n\n\n\n'

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

banking = True
script, filename = argv
# 'game_state' variable refers to the opening situation;
# that is, who are the players, what are their resepctive balances
def update_external():
    game_state = open(filename)
    game_state_txt = game_state.read().splitlines()
    players_list_str = game_state_txt[0]
    balances_list_str = game_state_txt[1]
    players = players_list_str[2:-2].split('\', \'')
    balances_init = balances_list_str[1:-1].split(', ')
    balances = []
    for i in range(0,len(balances_init)):
    	balances.append(float(balances_init[i]))
    game_state.close()
    return players, balances

def update_file(players_list, balances_list):
    writable_file = open(filename, 'w')
    player_str = str(players_list)
    balance_str = str(balances_list)
    writable_file.write(player_str + '\n' + balance_str)
    writable_file.close()

def accruing_interest():
    players, balances = update_external()
    t0 = time.clock()
    while ( time.clock() - t0 ) <= 10:
        dummy = 0
    print c.U + "\nBALANCE UPDATE:\n" + c.E
    for i in range(0,len(balances)):
        if balances[i] != 0:
            new_bal = balances[i]*0.005
            players, balances = update_external()
            balances[i] += new_bal
            print c.DARKCYAN + "%s" % players[i] + c.E + "'s BALANCE IS " + c.GREEN + "%.2f" % balances[i] + c.E + u'\u03FC.'
            update_file(players, balances)
        else:
            print "%s's BALANCE IS ZERO." % players[i]
            update_file(players, balances)
    print '\n',
    update_file(players, balances)

while banking == True:
    accruing_interest()
