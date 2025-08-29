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
    from ludo.bots.random_bot import RandomBot

    players = []
    for role in args.players:
        if role == "human":
            players.append(role)
        elif role == "random":
            players.append(RandomBot())
        else:
            raise ValueError(f"Unknown player role: {role}")

    game = Game(players=players, dice=dice)
    game.loop_cli()  # human input via stdin; bots via strategy

if __name__ == "__main__":
    main()
