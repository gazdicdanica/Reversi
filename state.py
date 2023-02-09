DIRECTIONS = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]

HEURISTIC = [[20, -3, 11, 8, 8, 11, -3, 20],
             [-3, -7, -4, 1, 1, -4, -7, -3],
             [11, -4, 2, 2, 2, 2, -4, 11],
             [8, 1, 2, -3, -3, 2, 1, 8],
             [8, 1, 2, -3, -3, 2, 1, 8],
             [11, -4, 2, 2, 2, 2, -4, 11],
             [-3, -7, -4, 1, 1, -4, -7, -3],
             [20, -3, 11, 8, 8, 11, -3, 20]]


def on_board(x, y):
    return 0 <= x <= 7 and 0 <= y <= 7


class State(object):

    def __init__(self):
        self._board = []
        for i in range(8):
            self._board.append(8*['-'])
        self._board[3][3] = 'W'
        self._board[4][4] = 'W'
        self._board[3][4] = 'B'
        self._board[4][3] = 'B'

    def __str__(self):
        ret = "\n    0   1   2   3   4   5   6   7\n  ---------------------------------\n"
        for i in range(0, 8):
            ret += str(i)
            ret += " |"
            for j in range(0, 8):
                if self._board[i][j] == '-':
                    ret += "   |"
                else:
                    ret += " %s |" % self._board[i][j]
            ret += "\n  ---------------------------------\n"
        return ret

    def get_value(self, i, j):
        return self._board[i][j]

    def set_value(self, i, j, value):
        self._board[i][j] = value

    def make_move(self, x, y, player):
        self._board[x][y] = player
        for d in DIRECTIONS:
            self.flip(x, y, player, d)

    def flip(self, x, y, player, d):
        xdir = d[0]
        ydir = d[1]
        next_tiles = self.find_next_tile(x, y, player, d)
        if not next_tiles:
            return
        x += xdir
        y += ydir
        for tile in next_tiles:
            self._board[tile[0]][tile[1]] = player

    def find_next_tile(self, x, y, player, direction):
        for_flipping = []
        ix = x
        iy = y
        xdir = direction[0]
        ydir = direction[1]
        if player == 'B':
            opponent = 'W'
        else:
            opponent = 'B'
        x += xdir
        y += ydir
        if not on_board(x, y):
            return
        if self._board[x][y] != opponent:
            return
        while self._board[x][y] == opponent:
            x += xdir
            y += ydir
            if not on_board(x, y):
                break
        if not on_board(x, y):
            return
        if self._board[x][y] == player:
            while True:
                x -= xdir
                y -= ydir
                if x == ix and y == iy:
                    break
                for_flipping.append([x, y])
        return for_flipping

    def valid_move(self, x, y, value):
        if not on_board(x, y):
            return False
        if self._board[x][y] != '-':
            return False
        if (x, y) not in self.legal_moves(value):
            return False
        return True

    def check_direction(self, x, y, direction, player):
        found = False
        counter = 0
        xdir = direction[0]
        ydir = direction[1]
        while True:
            x += xdir
            y += ydir
            if not on_board(x, y):
                break
            space = self._board[x][y]
            if space == '-':
                break
            elif space == player:
                found = True
                break
            else:
                counter += 1
        if counter > 0 and found:
            return True
        return False

    def legal_moves(self, player):
        moves=[]
        for x in range(0, 8):
            for y in range(0, 8):
                if self._board[x][y] != '-':
                    pass
                else:
                    for d in DIRECTIONS:
                        if self.check_direction(x, y, d, player) and (x, y) not in moves:
                            moves.append((x, y))
        return moves

    def score(self):
        player_tiles = 0
        ai_tiles = 0
        for x in range(0, 8):
            for y in range(0, 8):
                if self._board[x][y] == 'B':
                    player_tiles += 1
                elif self._board[x][y] == 'W':
                    ai_tiles += 1
        return player_tiles, ai_tiles

    def heuristic_eval(self):
        difference = 0
        ai_tiles = 0
        player_tiles = 0
        for x in range(0, 8):
            for y in range(0, 8):
                if self._board[x][y] == 'B':
                    difference += HEURISTIC[x][y]
                    player_tiles += 1
                else:
                    difference -= HEURISTIC[x][y]
                    ai_tiles += 1
        if player_tiles > ai_tiles:
            percentage = (100 * player_tiles) / (player_tiles + ai_tiles)
        elif player_tiles < ai_tiles:
            percentage = -(100 * ai_tiles) / (player_tiles + ai_tiles)
        else:
            percentage = 0

        ai_tiles = 0
        player_tiles = 0
        if self._board[0][0] == 'B':
            player_tiles += 1
        elif self._board[0][0] == 'W':
            ai_tiles += 1
        if self._board[0][7] == 'B':
            player_tiles += 1
        elif self._board[0][7] == 'W':
            ai_tiles += 1
        if self._board[7][0] == 'B':
            player_tiles += 1
        elif self._board[7][0] == 'W':
            ai_tiles += 1
        if self._board[7][7] == 'B':
            player_tiles += 1
        elif self._board[7][7] == 'W':
            ai_tiles += 1

        corners = 25 * (player_tiles - ai_tiles)

        ai_tiles = 0
        player_tiles = 0
        if self._board[0][0] == '-':
            if self._board[0][1] == 'B':
                player_tiles += 1
            elif self._board[0][1] == 'W':
                ai_tiles += 1
            if self._board[1][1] == 'B':
                player_tiles += 1
            elif self._board[1][1] == 'W':
                ai_tiles += 1
            if self._board[1][0] == 'B':
                player_tiles += 1
            elif self._board[1][0] == 'W':
                ai_tiles += 1

        if self._board[0][7] == '-':
            if self._board[0][6] == 'B':
                player_tiles += 1
            elif self._board[0][6] == 'W':
                ai_tiles += 1
            if self._board[1][6] == 'B':
                player_tiles += 1
            elif self._board[1][6] == 'W':
                ai_tiles += 1
            if self._board[6][0] == 'B':
                player_tiles += 1
            elif self._board[6][0] == 'W':
                ai_tiles += 1

        if self._board[7][0] == '-':
            if self._board[7][1] == 'B':
                player_tiles += 1
            elif self._board[7][1] == 'W':
                ai_tiles += 1
            if self._board[6][1] == 'B':
                player_tiles += 1
            elif self._board[6][1] == 'W':
                ai_tiles += 1
            if self._board[6][0] == 'B':
                player_tiles += 1
            elif self._board[6][0] == 'W':
                ai_tiles += 1

        if self._board[7][7] == '-':
            if self._board[6][1] == 'B':
                player_tiles += 1
            elif self._board[6][1] == 'W':
                ai_tiles += 1
            if self._board[6][6] == 'B':
                player_tiles += 1
            elif self._board[6][6] == 'W':
                ai_tiles += 1
            if self._board[7][6] == 'B':
                player_tiles += 1
            elif self._board[7][6] == 'W':
                ai_tiles += 1

        around_corner = -12.5 * (player_tiles - ai_tiles)

        result = 10 * percentage + 10 * difference + 801 * corners + 382*around_corner
        return result

    def end(self):
        if len(self.legal_moves('B')) == 0 and len(self.legal_moves('W')) == 0:
            tiles = self.score()
            if tiles[0] > tiles[1]:
                return True, 'B'
            if tiles[0] < tiles[1]:
                return True, 'W'
            else:
                return True, '0'
        return False, '0'
