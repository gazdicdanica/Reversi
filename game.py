import copy
import state
import tree
import datetime
import hashmap

heuristic_map = hashmap.Hashmap()


class Game(object):
    __slots__ = ['_current_state', '_players_turn', '_game_tree']

    def __init__(self):
        self._current_state = None
        self._players_turn = 'B'
        self.initialize_game()

    def initialize_game(self):
        self._current_state = state.State()

    def show_possible_moves(self):
        board = copy.deepcopy(self._current_state)
        moves = state.State.legal_moves(self._current_state, 'B')
        for move in moves:
            x = move[0]
            y = move[1]
            state.State.set_value(board, x, y, '*')
        return board, moves

    def print_state(self):
        player_score, ai_score = state.State.score(self._current_state)
        print("Your score:",  player_score, ", Computers score:", ai_score)
        print(self._current_state)

    def minimax_min(self, node, depth, alpha, beta, game_tree):
        global heuristic_map
        qx = -1
        qy = -1
        value = 10000000
        if game_tree.depth(node) == depth:
            if node.value in heuristic_map:
                heuristic = heuristic_map[node.value]
            else:
                heuristic = state.State.heuristic_eval(node.value)
                hashmap.Hashmap.__setitem__(heuristic_map, node.value, heuristic)
            return heuristic, qx, qy
        for move in state.State.legal_moves(node.value, 'B'):
            new_board = copy.deepcopy(node.value)
            state.State.make_move(new_board, move[0], move[1], 'B')
            child = tree.Node(new_board, [move[0], move[1]])
            node.add_child(child)
            child.parent = node
        for child in node.children:
            (m, max_i, max_j) = self.minimax_max(child, depth, alpha, beta, game_tree)
            if m < value:
                value = m
                qx = child.coordinates[0]
                qy = child.coordinates[1]
            if value <= alpha:
                return value, qx, qy
            if value < beta:
                beta = value
        return value, qx, qy

    def minimax_max(self, node, depth, alpha, beta, game_tree):
        global heuristic_map
        px = -1
        py = -1
        value = -10000000
        if game_tree.depth(node) == depth:
            if node.value in heuristic_map:
                heuristic = heuristic_map[node.value]
            else:
                heuristic = state.State.heuristic_eval(node.value)
                hashmap.Hashmap.__setitem__(heuristic_map, node.value, heuristic)
            return heuristic, px, py
        for move in state.State.legal_moves(node.value, 'W'):
            new_board = copy.deepcopy(node.value)
            state.State.make_move(new_board, move[0], move[1], 'W')
            child = tree.Node(new_board, [move[0], move[1]])
            node.add_child(child)
            child.parent = node
        for child in node.children:
            (m, min_i, min_j) = self.minimax_min(child, depth, alpha, beta, game_tree)
            if m > value:
                value = m
                px = child.coordinates[0]
                py = child.coordinates[1]
            if value >= beta:
                return value, px, py
            if value > alpha:
                alpha = value
        return value, px, py

    def play(self):
        print('\n\nWELCOME TO REVERSI!\nYou (B) are playing against a computer (W).\nGood luck!\n\n')
        while True:
            end, winner = state.State.end(self._current_state)
            if end:
                if winner == 'B':
                    print('Congrats! You won!')
                elif winner == 'W':
                    print('The computer has beaten you!')
                else:
                    print("It's a tie!")
                self.initialize_game()
                break
            if self._players_turn == 'B':
                if len(state.State.legal_moves(self._current_state, 'B')) == 0:
                    print('You have no legal moves.')
                    self._players_turn = 'W'
                    continue
                player_score, ai_score = state.State.score(self._current_state)
                print("Your score:", player_score, ", Computers score:", ai_score)
                board, moves = self.show_possible_moves()
                print(board)
                print('Possible moves: ', moves, '\n')
                valid = False
                while not valid:
                    print('Enter x and y coordinates:')
                    try:
                        x = int(input('X coordinate:'))
                        y = int(input('Y coordinate: '))
                        print('\n')
                    except ValueError:
                        print('\n\nCoordinate is not valid, please input a number between 0 and 7!\n')
                        x = int(input('X coordinate:'))
                        y = int(input('Y coordinate: '))
                        print('\n')
                    if state.State.valid_move(self._current_state, x, y, 'B'):
                        state.State.make_move(self._current_state, x, y, 'B')
                        valid = True
                    else:
                        print('\nPlease enter one of the valid moves marked with *\n')
                self.print_state()
                self._players_turn = 'W'
            else:
                if len(state.State.legal_moves(self._current_state, 'W')) == 0:
                    self._players_turn = 'B'
                    print('Computer has no moves')
                    continue
                node = tree.Node(self._current_state)
                game_tree = tree.Tree(node)
                start = datetime.datetime.now()
                (m, px, py) = self.minimax_max(game_tree.root, 3, -9999999999, 9999999999, game_tree)
                state.State.make_move(self._current_state, px, py, 'W')
                end = datetime.datetime.now()
                print(end - start)
                self._players_turn = 'B'

