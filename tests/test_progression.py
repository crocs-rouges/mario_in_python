import unittest

from game.progression import LevelProgression


class LevelProgressionTests(unittest.TestCase):
    def test_advancing_moves_to_the_next_level(self):
        progression = LevelProgression(2)

        advanced = progression.advance()

        self.assertTrue(advanced)
        self.assertEqual(progression.level_index, 1)
        self.assertFalse(progression.complete)

    def test_advancing_past_last_level_completes_the_game(self):
        progression = LevelProgression(2)
        progression.advance()

        advanced = progression.advance()

        self.assertFalse(advanced)
        self.assertTrue(progression.complete)
        self.assertFalse(progression.advance())

    def test_restart_returns_to_first_level(self):
        progression = LevelProgression(2)
        progression.advance()
        progression.advance()

        progression.restart()

        self.assertEqual(progression.level_index, 0)
        self.assertFalse(progression.complete)

    def test_progression_requires_at_least_one_level(self):
        with self.assertRaises(ValueError):
            LevelProgression(0)


if __name__ == "__main__":
    unittest.main()
