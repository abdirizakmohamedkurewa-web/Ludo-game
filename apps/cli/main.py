from ludo.game import Game
from ludo.dice import Dice

def main():
    """The main entry point for the command-line application."""
    print("Hello Ludo")
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--players", nargs="+", default=["human","random"])
    p.add_argument("--seed", type=int, default=None)
    args = p.parse_args()

    dice = Dice(seed=args.seed)
    players = []
    for role in args.players:
        players.append(role)  # "human" or Strategy instance ("random")

    game = Game(players=players, dice=dice)
    game.loop_cli()  # human input via stdin; bots via strategy

if __name__ == "__main__":
    main()
