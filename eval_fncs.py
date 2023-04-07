from state import State


def eval_1(state: State):
    count1 = count2 = 0
    for v in state.board.grid:
        if v == 1:
            count1 += 1
        elif v == 2:
            count2 += 1

    return count1 - count2
