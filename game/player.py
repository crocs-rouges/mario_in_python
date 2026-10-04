from dataclasses import dataclass
from typing import Any, List, Tuple


@dataclass(frozen=True)
class PlayerTiles:
    player: Any
    air: Any
    solid: Any
    ground: Tuple[Any, ...]
    horizontal_obstacles: Tuple[Any, ...]
    jump_obstacles: Tuple[Any, ...]
    breakable: Any
    broken: Any
    collectible: Any
    finish: Any
    mystery: Any
    used_mystery: Any


@dataclass(frozen=True)
class PlayerAction:
    score_delta: int = 0
    jump_started: bool = False
    redraw: bool = False
    level_finished: bool = False
    moved: bool = False
    power_up_collected: bool = False


class PlayerController:
    def __init__(self, tiles: PlayerTiles, animation_frame_count: int) -> None:
        if animation_frame_count < 1:
            raise ValueError("animation_frame_count must be positive")
        self.tiles = tiles
        self.animation_frame_count = animation_frame_count
        self.animation_frame = 0
        self.grown = False

    def reset(self) -> None:
        self.animation_frame = 0
        self.grown = False

    def take_hit(self) -> bool:
        if self.grown:
            self.grown = False
            return True
        return False

    def move(self, level: List[List[Any]], direction: str) -> PlayerAction:
        position = self._find_player(level)
        row, column = position

        if direction == "gauche":
            return self._move_horizontally(level, row, column, -1)
        if direction == "droite":
            return self._move_horizontally(level, row, column, 1)
        if direction == "haut":
            return self._jump(level, row, column)
        return PlayerAction()

    def fall(self, level: List[List[Any]]) -> PlayerAction:
        row, column = self._find_player(level)
        if row + 1 >= len(level):
            return PlayerAction()
        target = level[row + 1][column]
        if target == self.tiles.finish:
            return PlayerAction(level_finished=True)
        if target == self.tiles.air:
            level[row + 1][column] = self.tiles.player
            level[row][column] = self.tiles.air
            return PlayerAction(moved=True)
        return PlayerAction()

    def update_animation(self, level: List[List[Any]]) -> int:
        row, column = self._find_player(level)
        if row + 1 < len(level) and level[row + 1][column] != self.tiles.air:
            if self.animation_frame >= self.animation_frame_count - 2:
                self.animation_frame = 0
            else:
                self.animation_frame += 1
        else:
            self.animation_frame = self.animation_frame_count - 1
        return self.animation_frame

    def _move_horizontally(
        self, level: List[List[Any]], row: int, column: int, step: int
    ) -> PlayerAction:
        target_column = column + step
        if target_column < 0 or target_column >= len(level[row]):
            return PlayerAction()

        target = level[row][target_column]
        if target == self.tiles.finish:
            return PlayerAction(level_finished=True)
        if target not in self.tiles.horizontal_obstacles:
            score_delta = 3 if target == self.tiles.collectible else 0
            level[row][target_column] = self.tiles.player
            level[row][column] = self.tiles.air
            return PlayerAction(score_delta=score_delta, redraw=score_delta > 0)

        if row >= 2 and row + 1 < len(level):
            below = level[row + 1][column]
            can_climb = (
                below not in self.tiles.ground
                if step < 0
                else below != self.tiles.solid
            )
            if can_climb:
                level[row - 2][column] = self.tiles.player
                level[row][column] = self.tiles.air
        return PlayerAction()

    def _jump(self, level: List[List[Any]], row: int, column: int) -> PlayerAction:
        if row == 0 or row + 1 >= len(level):
            return PlayerAction()
        if level[row + 1][column] not in self.tiles.ground:
            return PlayerAction()

        above = level[row - 1][column] if row > 0 else None
        if above == self.tiles.finish:
            return PlayerAction(level_finished=True)
        if above == self.tiles.solid:
            if row >= 2:
                level[row - 2][column] = self.tiles.player
                level[row][column] = self.tiles.air
            return PlayerAction()

        if above == self.tiles.mystery:
            level[row - 1][column] = self.tiles.used_mystery
            self.grown = True
            return PlayerAction(
                score_delta=1,
                jump_started=True,
                redraw=True,
                power_up_collected=True,
            )

        if above not in self.tiles.jump_obstacles:
            score_delta = 3 if above == self.tiles.collectible else 0
            level[row - 1][column] = self.tiles.player
            level[row][column] = self.tiles.air
            return PlayerAction(score_delta=score_delta, jump_started=True, redraw=score_delta > 0)

        if above == self.tiles.breakable:
            level[row - 1][column] = self.tiles.air
            return PlayerAction(score_delta=1, jump_started=True, redraw=True)
        return PlayerAction(
            jump_started=True,
        )

    def _find_player(self, level: List[List[Any]]) -> Tuple[int, int]:
        for row_index, row in enumerate(level):
            for column_index, tile in enumerate(row):
                if tile == self.tiles.player:
                    return row_index, column_index
        raise ValueError("player tile is missing from the active level")
