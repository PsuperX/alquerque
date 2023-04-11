from state import State


def eval_1(state: State) -> float:
    """
    Difference between player 1 pieces and player 2 pieces
    """

    count1 = count2 = 0
    for v in state.board.grid:
        if v == 1:
            count1 += 1
        elif v == 2:
            count2 += 1

    return count1 - count2


def eval_2(state: State):
    """
    Number of pieces in the borders
    """

    count1 = count2 = 0
    for i in range(state.board.num_rows):
        p = state.board.get_piece(0, i)
        if p == 1:
            count1 += 1
        elif p == 2:
            count2 += 1

        p = state.board.get_piece(state.board.num_cols - 1, i)
        if p == 1:
            count1 += 1
        elif p == 2:
            count2 += 1

    for i in range(1, state.board.num_cols - 1):
        p = state.board.get_piece(i, 0)
        if p == 1:
            count1 += 1
        elif p == 2:
            count2 += 1

        p = state.board.get_piece(i, state.board.num_rows - 1)
        if p == 1:
            count1 += 1
        elif p == 2:
            count2 += 1

    return count1 - count2
