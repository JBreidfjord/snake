from collections import deque
from enum import Enum
from random import choice


# Move._member_names_ to get a list of names
class Move(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class Game:
    def __init__(self, size: int = 10):
        # Enforce minimum grid size
        if size < 3:
            size = 3
        self.size = size

        # Calculate center square for starting index
        center = size // 2 if size % 2 == 0 else size // 2 + 1
        center_square = size * (center - 1) + center - 1

        # Create queue representing snake's path and append starting index
        self.snake: deque[int] = deque(maxlen=size ** 2)
        self.snake.append(center_square)

        # Place starting food
        self._place_food()

    def make_move(self, move: Move):
        x, y = move.value
        head = self.snake[-1]

        # Check if next move would move snake into side walls
        if (head % self.size == self.size - 1 and move.name == "RIGHT") or (
            head % self.size == 0 and move.name == "LEFT"
        ):
            self._game_over()
            return

        # Add x and y values to current head index
        # y is multiplied by grid size to shift index by a row
        head += x + y * self.size
        self.snake.append(head)  # Move head

        self._next_frame()

    def _next_frame(self):
        head = self.snake[-1]

        # Check if snake has moved off grid vertically
        if not 0 <= head < self.size ** 2:
            self._game_over()
            return

        # Check if snake moved into itself
        if self.snake.count(head) > 1:
            self._game_over()
            return

        # Check if snake found food
        if head == self.food:
            self._place_food()
        elif len(self.snake) > 2:
            # Move tail if no food found and minimum length has been reached
            self.snake.popleft()

        self.display()

    def _place_food(self):
        # Get list of empty squares
        valid_squares = set(self.snake) ^ set(range(self.size ** 2))

        # Select random square from list of empty squares
        self.food = choice(list(valid_squares))

    def _game_over(self):
        print(f"Game over! Your score was {len(self.snake) - 1}.")

    def display(self):
        head = self.snake[-1]
        out = "|"
        out += "---" * self.size
        for y in range(0, self.size ** 2, self.size):
            out += "|\n|"
            for x in range(self.size):
                i = y + x
                if i == head:
                    out += " \u25A1 "
                elif i == self.food:
                    out += " \u2022 "
                elif i in self.snake:
                    out += " \u25A0 "
                else:
                    out += "   "
        out += "|\n|"
        out += "---" * self.size
        out += "|"
        print(out)

