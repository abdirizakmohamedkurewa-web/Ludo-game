import argparse
from ludo.game import Game
from ludo.dice import Dice
from ludo.player import Player
from ludo.bots.human_bot import HumanBot
from ludo.bots.random_bot import RandomBot
from ludo.utils.constants import PlayerColor
from ludo.persistence import load_game

def main():
    """The main entry point for the command-line application."""
    p = argparse.ArgumentParser()
    p.add_argument("--players", nargs="+", default=["human", "random"])
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--load-game", type=str, default=None, help="Path to a saved game file to load.")
    args = p.parse_args()

    if args.load_game:
        print(f"Loading game from {args.load_game}...")
        state = load_game(args.load_game)
        dice = Dice(seed=state.dice_seed)
        players = state.players
        strategies = []
        for player in players:
            if player.role == "human":
                strategies.append(HumanBot())
            elif player.role == "random":
                strategies.append(RandomBot())
            else:
                raise ValueError(f"Unknown player role in saved game: {player.role}")
        game = Game(players=players, strategies=strategies, dice=dice, state=state)
        print("Game loaded successfully.")
    else:
        dice = Dice(seed=args.seed)
        colors = [PlayerColor.RED, PlayerColor.GREEN, PlayerColor.YELLOW, PlayerColor.BLUE]

        players = []
        strategies = []
        for i, role in enumerate(args.players):
            if i >= len(colors):
                print(f"Warning: Too many players. Max is {len(colors)}. Ignoring extra players.")
                break

            color = colors[i]
            player = Player(color=color, role=role)
            players.append(player)

            if role == "human":
                strategies.append(HumanBot())
            elif role == "random":
                strategies.append(RandomBot())
            else:
                raise ValueError(f"Unknown player role: {role}")
        game = Game(players=players, strategies=strategies, dice=dice)

    game.loop_cli()

if __name__ == "__main__":
    import sys
    main()
    sys.exit(0)
