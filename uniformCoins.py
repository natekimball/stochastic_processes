from random import random
import sys

def runRound(verbose=False):
    coinOdds, flip1, flip2, flip3 = [random() for _ in range(4)]
    if verbose:
        print("the coin has odds of", coinOdds, "of landing on heads")
        print(flip1)
        print("the first flip is", "heads" if flip1<=coinOdds else "tails")
        print(flip2)
        print("the second flip is", "heads" if flip2<=coinOdds else "tails")
        print(flip3)
        print("the third flip is", "heads" if flip3<=coinOdds else "tails")
    heads = (flip1<=coinOdds) + (flip2<=coinOdds) + (flip3<=coinOdds)
    return heads==3

if "-r" in sys.argv:
    rounds = int(sys.argv[sys.argv.index("-r")+1])
elif "--rounds" in sys.argv:
    rounds = int(sys.argv[sys.argv.index("--rounds")+1])
else:
    rounds = 100

player1 = "nate"
player2 = "aneesh"

if rounds==1:
    print(player1 if runRound(True) else player2, "wins")
else:    
    wins = 0
    for i in range(rounds):
        if runRound():
            wins += 1

    print(player1,"won", wins, "times")
    print(player2, "won", rounds-wins, "times")
    print(player1,"won", wins/rounds*100, "% of the time")