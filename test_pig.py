import unittest
from unittest.mock import patch
from pig import Player, Die, PigGame


class TestPigGame(unittest.TestCase):

    def test_player_starts_at_zero(self):
        player = Player("Player 1")
        self.assertEqual(player.score, 0)

    def test_player_adds_points(self):
        player = Player("Player 1")
        player.add_score(10)
        self.assertEqual(player.score, 10)

    def test_die_rolls_valid_number(self):
        die = Die()
        for _ in range(100):
            self.assertIn(die.roll(), range(1, 7))

    def test_rolling_one_loses_turn(self):
        game = PigGame()

        # Player 1 rolls a 4, then a 1.
        # Player 2 starts at 99 and wins by rolling 2 and holding.
        game.players[1].score = 99

        with patch.object(game.die, "roll", side_effect=[4, 1, 2]):
            with patch("builtins.input", side_effect=["r", "r", "r", "h"]):
                game.play()

        self.assertEqual(game.players[0].score, 0)
        self.assertEqual(game.players[1].score, 101)

    def test_game_stops_at_100(self):
        game = PigGame()
        game.players[0].score = 98

        with patch.object(game.die, "roll", return_value=3):
            with patch("builtins.input", side_effect=["r", "h"]):
                game.play()

        self.assertEqual(game.players[0].score, 101)
        self.assertEqual(game.current_player, 0)


if __name__ == "__main__":
    unittest.main()
