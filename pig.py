import argparse
import random
import time


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def add_score(self, points):
        self.score += points


class HumanPlayer(Player):
    def choose_action(self, turn_total):
        return input("Roll (r) or Hold (h)? ").strip().lower()


class ComputerPlayer(Player):
    def choose_action(self, turn_total):
        threshold = min(25, 100 - self.score)
        if turn_total >= threshold:
            return "h"
        return "r"


class PlayerFactory:
    @staticmethod
    def create_player(player_type, name):
        if player_type == "human":
            return HumanPlayer(name)
        if player_type == "computer":
            return ComputerPlayer(name)
        raise ValueError("Player must be human or computer")


class Die:
    def roll(self):
        return random.randint(1, 6)


class PigGame:
    def __init__(self, player1="human", player2="human"):
        self.players = [
            PlayerFactory.create_player(player1, "Player 1"),
            PlayerFactory.create_player(player2, "Player 2")
        ]
        self.die = Die()
        self.current_player = 0

    def play(self, timed_out=None):
        print("Welcome to the Pig Dice Game!")

        while True:
            if timed_out is not None and timed_out():
                return self.finish_on_time()

            player = self.players[self.current_player]
            turn_total = 0

            print(f"\n{player.name}'s turn!")
            print(f"Total score: {player.score}")

            while True:
                if timed_out is not None and timed_out():
                    return self.finish_on_time()

                print(f"\n{player.name}'s score: {player.score}")
                print(f"Current turn total: {turn_total}")
                print(f"Potential score: {player.score + turn_total}")

                choice = player.choose_action(turn_total)

                if timed_out is not None and timed_out():
                    return self.finish_on_time()

                if isinstance(player, ComputerPlayer):
                    action = "roll" if choice == "r" else "hold"
                    print(f"{player.name} chooses to {action}.")

                if choice == "r":
                    roll = self.die.roll()
                    print(f"{player.name} rolled a {roll}!")

                    if roll == 1:
                        print("You rolled a 1! Turn points are lost.")
                        break

                    turn_total += roll
                    print(f"Turn total: {turn_total}")

                elif choice == "h":
                    player.add_score(turn_total)
                    print(f"{player.name}'s total score: {player.score}")
                    break

                else:
                    print("Invalid choice. Enter r or h.")

            if player.score >= 100:
                print(f"\n{player.name} wins with {player.score} points!")
                return player

            self.current_player = 1 - self.current_player

    def finish_on_time(self):
        first, second = self.players

        print("\nTime is up!")
        print(f"{first.name}: {first.score} points")
        print(f"{second.name}: {second.score} points")

        if first.score == second.score:
            print("The game is a tie!")
            return None

        if first.score > second.score:
            winner = first
        else:
            winner = second

        print(f"{winner.name} wins!")
        return winner


class TimedGameProxy:
    def __init__(self, game, limit_seconds=60):
        self.game = game
        self.limit_seconds = limit_seconds

    def play(self):
        start = time.monotonic()

        def timed_out():
            return time.monotonic() - start >= self.limit_seconds

        return self.game.play(timed_out=timed_out)


def main():
    parser = argparse.ArgumentParser(description="Pig Dice Game")

    parser.add_argument(
        "--player1",
        choices=["human", "computer"],
        default="human"
    )

    parser.add_argument(
        "--player2",
        choices=["human", "computer"],
        default="human"
    )

    parser.add_argument(
        "--timed",
        action="store_true",
        help="Play a 60-second timed game"
    )

    args = parser.parse_args()

    game = PigGame(args.player1, args.player2)

    if args.timed:
        game = TimedGameProxy(game)

    game.play()


if __name__ == "__main__":
    main()
