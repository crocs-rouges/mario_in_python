import unittest

from game.enemies import EnemyController, EnemyTiles


AIR = 0
PLAYER = 100
SOLID = 1
GOOMBA = 50
KOOPA = 55


def make_controller(movement_interval=1):
    tiles = EnemyTiles(
        player=PLAYER,
        air=AIR,
        goomba=GOOMBA,
        koopa=KOOPA,
        obstacles=(SOLID,),
        support=(SOLID,),
    )
    return EnemyController(tiles, movement_interval=movement_interval)


class EnemyControllerTests(unittest.TestCase):
    def test_stomping_enemy_rewards_player_without_damage(self):
        controller = make_controller()
        level = [
            [AIR, AIR, AIR],
            [AIR, PLAYER, AIR],
            [AIR, GOOMBA, AIR],
            [SOLID, SOLID, SOLID],
        ]

        action = controller.update(level)

        self.assertEqual(level[1][1], AIR)
        self.assertEqual(level[2][1], PLAYER)
        self.assertEqual(action.score_delta, 100)
        self.assertEqual(action.damage, 0)

    def test_touching_enemy_damages_player_and_removes_enemy(self):
        controller = make_controller()
        level = [
            [AIR, AIR, AIR],
            [PLAYER, KOOPA, AIR],
            [SOLID, SOLID, SOLID],
        ]

        action = controller.update(level)

        self.assertEqual(level[1], [PLAYER, AIR, AIR])
        self.assertEqual(action.damage, 1)
        self.assertEqual(action.score_delta, 0)

    def test_enemy_moves_only_on_configured_interval(self):
        controller = make_controller(movement_interval=2)
        level = [
            [AIR, AIR, AIR, AIR],
            [AIR, GOOMBA, AIR, PLAYER],
            [SOLID, SOLID, SOLID, SOLID],
        ]

        controller.update(level)
        self.assertEqual(level[1], [AIR, GOOMBA, AIR, PLAYER])

        controller.update(level)
        self.assertEqual(level[1], [GOOMBA, AIR, AIR, PLAYER])

    def test_enemy_reverses_at_level_edge_instead_of_wrapping(self):
        controller = make_controller()
        level = [
            [AIR, AIR, PLAYER],
            [GOOMBA, AIR, AIR],
            [SOLID, SOLID, SOLID],
        ]

        controller.update(level)

        self.assertEqual(level[1], [AIR, GOOMBA, AIR])

    def test_enemy_reverses_before_walking_off_a_platform(self):
        controller = make_controller()
        level = [
            [AIR, AIR, PLAYER, AIR],
            [AIR, GOOMBA, AIR, AIR],
            [SOLID, AIR, AIR, SOLID],
        ]

        controller.update(level)

        self.assertEqual(level[1], [GOOMBA, AIR, AIR, AIR])

    def test_enemies_do_not_overwrite_each_other(self):
        controller = make_controller()
        level = [
            [AIR, AIR, AIR, PLAYER],
            [GOOMBA, AIR, KOOPA, AIR],
            [SOLID, SOLID, SOLID, SOLID],
        ]

        controller.update(level)

        self.assertEqual(level[1], [AIR, GOOMBA, AIR, KOOPA])

    def test_switching_levels_reinitializes_enemy_tracking(self):
        controller = make_controller()
        first_level = [
            [AIR, AIR, PLAYER],
            [GOOMBA, AIR, AIR],
            [SOLID, SOLID, SOLID],
        ]
        second_level = [
            [PLAYER, AIR, AIR],
            [AIR, AIR, KOOPA],
            [SOLID, SOLID, SOLID],
        ]

        controller.update(first_level)
        controller.update(second_level)

        self.assertEqual(second_level[1], [AIR, KOOPA, AIR])


if __name__ == "__main__":
    unittest.main()
