from board import Board
from state import State

# fmt: off
grid = [0,0,0,0,2,
        0,1,1,2,0,
        2,2,1,1,0,
        0,2,0,0,0,
        1,0,0,0,0,]
# fmt: on
b = Board(5, 5, 2, grid)
s = State(b)

print(ac := b.get_valid_actions())

s.execute(ac[0])
print(b.grid)
s.undo()
print(b.grid)
