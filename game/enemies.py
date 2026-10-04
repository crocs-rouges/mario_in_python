from dataclasses import dataclass
from typing import Any, List, Tuple


@dataclass(frozen=True)
class EnemyTiles:
    player: Any
    air: Any
    goomba: Any
    koopa: Any
    obstacles: Tuple[Any, ...]
    support: Tuple[Any, ...]


@dataclass(frozen=True)
class EnemyAction:
    score_delta: int = 0
    damage: int = 0
    redraw: bool = False


@dataclass
class _Enemy:
    row: int
    column: int
    tile: Any
    direction: int = -1


class EnemyController:
    def __init__(
        self,
        tiles: EnemyTiles,
        movement_interval: int = 20,
        stomp_score: int = 100,
    ) -> None:
        if movement_interval < 1:
            raise ValueError("movement_interval must be positive")
        self.tiles = tiles
        self.movement_interval = movement_interval
        self.stomp_score = stomp_score
        self._frame = 0
        self._level_id = None
        self._enemies: List[_Enemy] = []

    def reset(self) -> None:
        self._frame = 0
        self._level_id = None
        self._enemies = []

    def update(self, level: List[List[Any]]) -> EnemyAction:
        self._sync_enemies(level)
        self._frame += 1
        score_delta = 0
        damage = 0
        redraw = False

        player_position = self._find_player(level)
        player_row, player_column = player_position
        stomped = [
            enemy
            for enemy in self._enemies
            if enemy.row == player_row + 1 and enemy.column == player_column
        ]

        if stomped:
            enemy = stomped[0]
            level[enemy.row][enemy.column] = self.tiles.player
            level[player_row][player_column] = self.tiles.air
            self._enemies.remove(enemy)
            score_delta += self.stomp_score
            redraw = True
        else:
            for enemy in list(self._enemies):
                if enemy.row == player_row and abs(enemy.column - player_column) == 1:
                    level[enemy.row][enemy.column] = self.tiles.air
                    self._enemies.remove(enemy)
                    damage += 1
                    redraw = True

        if self._frame % self.movement_interval == 0:
            for enemy in self._enemies:
                self._move_enemy(level, enemy)

        return EnemyAction(
            score_delta=score_delta,
            damage=damage,
            redraw=redraw,
        )

    def _sync_enemies(self, level: List[List[Any]]) -> None:
        if id(level) != self._level_id:
            self._level_id = id(level)
            self._frame = 0
            self._enemies = []

        self._enemies = [
            enemy
            for enemy in self._enemies
            if self._tile_at(level, enemy.row, enemy.column) == enemy.tile
        ]
        known_positions = {
            (enemy.row, enemy.column) for enemy in self._enemies
        }

        for row_index, row in enumerate(level):
            for column_index, tile in enumerate(row):
                if tile in (self.tiles.goomba, self.tiles.koopa) and (
                    row_index,
                    column_index,
                ) not in known_positions:
                    self._enemies.append(_Enemy(row_index, column_index, tile))

    def _move_enemy(self, level: List[List[Any]], enemy: _Enemy) -> None:
        next_column = enemy.column + enemy.direction
        if self._can_move_to(level, enemy.row, next_column):
            self._move_to(level, enemy, next_column)
            return

        enemy.direction *= -1
        next_column = enemy.column + enemy.direction
        if self._can_move_to(level, enemy.row, next_column):
            self._move_to(level, enemy, next_column)

    def _can_move_to(self, level: List[List[Any]], row: int, column: int) -> bool:
        if row < 0 or row >= len(level) or column < 0 or column >= len(level[row]):
            return False
        tile = level[row][column]
        if tile in (
            *self.tiles.obstacles,
            self.tiles.player,
            self.tiles.goomba,
            self.tiles.koopa,
        ):
            return False

        below_row = row + 1
        return (
            below_row < len(level)
            and level[below_row][column] in self.tiles.support
        )

    def _move_to(self, level: List[List[Any]], enemy: _Enemy, column: int) -> None:
        level[enemy.row][enemy.column] = self.tiles.air
        level[enemy.row][column] = enemy.tile
        enemy.column = column

    @staticmethod
    def _tile_at(level: List[List[Any]], row: int, column: int) -> Any:
        if row < 0 or row >= len(level) or column < 0 or column >= len(level[row]):
            return None
        return level[row][column]

    def _find_player(self, level: List[List[Any]]) -> Tuple[int, int]:
        for row_index, row in enumerate(level):
            for column_index, tile in enumerate(row):
                if tile == self.tiles.player:
                    return row_index, column_index
        raise ValueError("player tile is missing from the active level")
