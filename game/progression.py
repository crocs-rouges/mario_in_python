class LevelProgression:
    def __init__(self, level_count: int) -> None:
        if level_count < 1:
            raise ValueError("level_count must be positive")
        self.level_count = level_count
        self.level_index = 0
        self.complete = False

    def advance(self) -> bool:
        if self.complete:
            return False
        if self.level_index + 1 < self.level_count:
            self.level_index += 1
            return True
        self.complete = True
        return False

    def restart(self) -> None:
        self.level_index = 0
        self.complete = False
