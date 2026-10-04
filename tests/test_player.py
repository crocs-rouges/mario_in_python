import unittest

from game.player import PlayerController, PlayerTiles


AIR = 0
PLAYER = 100
SOLID = 1
BRICK = 2
BROKEN_BRICK = 22
PIPE = 4
MIST = 5
COIN = 3
FINISH = 6
MYSTERY = 7
USED_MYSTERY = 8


def make_player():
    tiles = PlayerTiles(
        player=PLAYER,
        air=AIR,
        solid=SOLID,
        ground=(SOLID, BRICK, PIPE, MIST),
        horizontal_obstacles=(SOLID, BRICK, PIPE, MIST),
        jump_obstacles=(BRICK, PIPE, MIST, USED_MYSTERY),
        breakable=BRICK,
        broken=BROKEN_BRICK,
        collectible=COIN,
        finish=FINISH,
        mystery=MYSTERY,
        used_mystery=USED_MYSTERY,
    )
    return PlayerController(tiles, animation_frame_count=4)


class PlayerControllerTests(unittest.TestCase):
    def test_horizontal_movement_stops_at_both_edges(self):
        player = make_player()
        left_edge = [[AIR, AIR], [PLAYER, AIR], [SOLID, SOLID]]
        right_edge = [[AIR, AIR], [AIR, PLAYER], [SOLID, SOLID]]

        player.move(left_edge, "gauche")
        player.move(right_edge, "droite")

        self.assertEqual(left_edge[1], [PLAYER, AIR])
        self.assertEqual(right_edge[1], [AIR, PLAYER])

    def test_collecting_coin_moves_player_and_returns_score(self):
        player = make_player()
        level = [[AIR, AIR, AIR], [PLAYER, COIN, AIR], [SOLID] * 3]

        result = player.move(level, "droite")

        self.assertEqual(level[1], [AIR, PLAYER, AIR])
        self.assertEqual(result.score_delta, 3)
        self.assertTrue(result.redraw)

    def test_reaching_finish_signals_level_completion_without_replacing_marker(self):
        player = make_player()
        level = [[AIR, PLAYER, FINISH], [SOLID, SOLID, SOLID]]

        result = player.move(level, "droite")

        self.assertEqual(level[0], [AIR, PLAYER, FINISH])
        self.assertTrue(result.level_finished)

    def test_jumping_into_finish_signals_level_completion(self):
        player = make_player()
        level = [
            [AIR, FINISH],
            [AIR, PLAYER],
            [SOLID, SOLID],
        ]

        result = player.move(level, "haut")

        self.assertTrue(result.level_finished)
        self.assertEqual(level[0][1], FINISH)
        self.assertEqual(level[1][1], PLAYER)

    def test_falling_onto_finish_signals_level_completion(self):
        player = make_player()
        level = [[AIR], [PLAYER], [FINISH], [SOLID]]

        result = player.fall(level)

        self.assertTrue(result.level_finished)
        self.assertFalse(result.moved)
        self.assertEqual([row[0] for row in level], [AIR, PLAYER, FINISH, SOLID])

    def test_jumping_into_brick_breaks_it_without_moving_player(self):
        player = make_player()
        level = [
            [AIR, AIR, AIR],
            [AIR, BRICK, AIR],
            [AIR, PLAYER, AIR],
            [SOLID, SOLID, SOLID],
        ]

        result = player.move(level, "haut")

        self.assertEqual(level[1][1], AIR)
        self.assertEqual(level[2][1], PLAYER)
        self.assertEqual(result.score_delta, 1)
        self.assertTrue(result.jump_started)

    def test_mystery_block_grants_growth_and_becomes_used(self):
        player = make_player()
        level = [
            [AIR, AIR, AIR],
            [AIR, MYSTERY, AIR],
            [AIR, PLAYER, AIR],
            [SOLID, SOLID, SOLID],
        ]

        result = player.move(level, "haut")

        self.assertEqual(level[1][1], USED_MYSTERY)
        self.assertTrue(player.grown)
        self.assertTrue(result.power_up_collected)
        self.assertTrue(result.jump_started)

    def test_used_mystery_block_does_not_grant_power_again(self):
        player = make_player()
        player.grown = True
        level = [
            [AIR, AIR, AIR],
            [AIR, USED_MYSTERY, AIR],
            [AIR, PLAYER, AIR],
            [SOLID, SOLID, SOLID],
        ]

        result = player.move(level, "haut")

        self.assertTrue(player.grown)
        self.assertFalse(result.power_up_collected)
        self.assertEqual(level[1][1], USED_MYSTERY)

    def test_grown_player_loses_power_before_losing_a_life(self):
        player = make_player()
        player.grown = True

        self.assertTrue(player.take_hit())
        self.assertFalse(player.grown)
        self.assertFalse(player.take_hit())

    def test_falling_moves_player_down_one_empty_cell(self):
        player = make_player()
        level = [[AIR], [PLAYER], [AIR], [SOLID]]

        result = player.fall(level)

        self.assertTrue(result.moved)
        self.assertEqual([row[0] for row in level], [AIR, AIR, PLAYER, SOLID])

    def test_animation_uses_jump_frame_in_air(self):
        player = make_player()
        level = [[AIR], [PLAYER], [AIR], [SOLID]]

        frame = player.update_animation(level)

        self.assertEqual(frame, 3)


if __name__ == "__main__":
    unittest.main()
