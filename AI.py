import random

from Board import Board


def best_move(board: Board, depth: int, maximizing_player=True):
    return minimax(board, depth, alpha=-float('inf'), beta=+float('inf'), maximizing_player=maximizing_player)[1]


def minimax(board: Board, depth: int, alpha=-float('inf'), beta=+float('inf'), maximizing_player=True):
    """
    Calculate the best move to play using the minimax algorithm.
    This algorithm is fully deterministic but yet, because of time limits and irrational players, you can still lose a
    game using this algorithm.

    :param board: The board of th game.
    :param depth: Number of steps to look into the future. Warning: has an exponential time growth.
    :param alpha: Used to improve the average time.
    :param beta: Used to improve the average time.
    :param maximizing_player: Determines the goal of the player. It tries to get the maximal or the minimal score.
    :return: Best game-state that can be leaded to, The best move you can make, Depth the game ends in.
    """
    state_value = board.state_value()
    if abs(state_value) == float('inf') or (not board.available_cols):  # game over
        return state_value, None, 0

    if depth == 0:  # end of recursion
        return state_value, None, -float('inf')

    # randomize the order it checks moves to reduce the average time.
    check_column_order = [i for i in board.available_cols]
    random.shuffle(check_column_order)

    move = None
    move_end_game_depth = 0
    if maximizing_player:
        max_eval = -float('inf')
        for col in check_column_order:
            board.turn(col)
            rec = minimax(board, depth - 1, alpha, beta, maximizing_player=False)
            evaluation = rec[0]
            board.undo_tern(col)

            if evaluation > max_eval:
                max_eval = evaluation
                move = col
                move_end_game_depth = rec[2]

            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break

        return max_eval, move, move_end_game_depth + 1

    else:
        min_eval = +float('inf')
        for col in check_column_order:
            board.turn(col)
            rec = minimax(board, depth - 1, alpha, beta, maximizing_player=True)
            evaluation = rec[0]
            board.undo_tern(col)

            if evaluation < min_eval:
                min_eval = evaluation
                move = col
                move_end_game_depth = rec[2]

            beta = min(beta, evaluation)
            if beta <= alpha:
                break

        return min_eval, move, move_end_game_depth + 1


def play_against_ai(board, depth, you_start=True):
    history = []
    while True:
        board.printb()
        value = board.state_value()
        if abs(value) == float('inf'):
            if board.current_turn == you_start:
                print("Congratulations! You won!")
            else:
                print("AI won. :(")
            break

        if board.current_turn != you_start:
            while True:
                col = input(">>>")
                if col == 'c':
                    break
                try:
                    col = int(col)
                    if col not in board.available_cols:
                        print("Unavailable column. Please choose other one.")
                        continue
                    break
                except ValueError:
                    pass

        else:
            best_val, col, time_till_end = minimax(board, depth, maximizing_player=not you_start)
            if col is None:
                col = random.choice(list(board.available_cols))
                print("(Random)")
            print(f"AI moved in column number {col}.")
            print("best move value:", best_val)

        if col == 'c':
            break
        if not board.available_cols:
            print("Draw.")
            break
        print(board.state_value())
        board.turn(col)
        history.append(col)
        print(board.state_value())

    return history
