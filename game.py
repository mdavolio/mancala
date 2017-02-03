# -*- coding: utf-8 -*-


class Game():
    """Represents a mancala game."""
    _default_board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]

    def __init__(self):

        # creates board, 2 players by 6 holes
        self._board = Game._default_board[:]
        # so the board looks like 00 01 02 03 04 05
        #                      13                   06
        #                         12 11 10 09 08 07
        # Player 1 scores in 06 and Player 2 scores in 13

        self._player_one = True
        self._moves = []

    def turn_player(self):
        return 1 if self._player_one else 2

    def score(self):
        return (self._board[6], self._board[13])

    def side_empty(self):
        stones_left_01 = sum(self._board[0:6])
        stones_left_02 = sum(self._board[7:13])
        return stones_left_01 == 0 or stones_left_02 == 0

    def over(self):
        return self._board[6] >= 25 or self._board[13] >= 25

    def board_render(self):
        # There are certainly better ways to render this
        s = '    {0: >2} {1: >2} {2: >2} {3: >2} {4: >2} {5: >2}\n'.format(
            self._board[0], self._board[1], self._board[2], self._board[3], self._board[4], self._board[5])
        s += ' {0: >2}                   {1: >2} \n'.format(
            self._board[13], self._board[6])
        s += '    {0: >2} {1: >2} {2: >2} {3: >2} {4: >2} {5: >2}'.format(
            self._board[12], self._board[11], self._board[10], self._board[9], self._board[8], self._board[7])
        return s

    @staticmethod
    def idx_player_1(idx):
        return idx <= 5 and idx >= 0

    @staticmethod
    def idx_player_2(idx):
        return idx >= 7 and idx <= 12

    @staticmethod
    def own_zone(idx, player):
        if player:
            return Game.idx_player_1(idx)
        else:
            return Game.idx_player_2(idx)

    # Called to calculate moves
    def move(self, idx):
        """Perform a move action on a given index, based on the current player"""

        if (self.over()):
            return self.score()

        # Illegal move if empty hole
        if (self._board[idx] == 0):
            return self.score()
        # Illegal move if score hole chosen ... not really necessary but keep for now
        if(idx == 6 or idx == 13):
            return self.score()
        # Illegal p1 choose p2
        if(self._player_one and not Game.idx_player_1(idx)):
            return self.score()
        if(not self._player_one and not Game.idx_player_2(idx)):
            return self.score()

        self._moves.append(idx)
        # Calculate stones in chosen hole
        count = self._board[idx]

        self._board[idx] = 0
        current_idx = idx

        # While still stones to move
        while count > 0:
            current_idx = (current_idx + 1) % len(self._board)
            if (self._player_one and current_idx == 13):
                continue
            if ((not self._player_one) and current_idx == 6):
                continue
            self._board[current_idx] += 1
            count -= 1  # one less stone to move

        # If last stone ends in score go again
        if(current_idx == 6 or current_idx == 13):
            return self.score()

        # Capture rule
        if(self._board[current_idx] == 1 and self._board[12 - current_idx] >= 1 and Game.own_zone(current_idx, self._player_one)):
            extra_stones = 1 + self._board[12 - current_idx]
            self._board[12 - current_idx] = 0
            self._board[current_idx] = 0
            if(self._player_one):
                self._board[6] += extra_stones
            else:
                self._board[13] += extra_stones

        if (self.side_empty()):
            self._board[6] += sum(self._board[0:6])
            self._board[13] += sum(self._board[7:13])
            self._board[0:6] = [0,0,0,0,0,0]
            self._board[7:13] = [0,0,0,0,0,0]
            return self.score()


        # Flip the current player IFF the turn ends on a new spot
        self._player_one = self._player_one if idx == current_idx else not self._player_one

        return self.score()
