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
        # Player 1 scores in 13 and Player 2 scores in 06

        self._player_one = True
        self._moves = []

    def turn_player(self):
        return 1 if self._player_one else 2

    def score(self):
        return (self._board[13], self._board[6])

    def over(self):
        stones_left_01 = sum(self._board[0:6])
        stones_left_02 = sum(self._board[7:13])
        return stones_left_01 == 0 or stones_left_02 == 0

    def board_render(self):
        # There are certainly better ways to render this
        s = '    {0: >2} {1: >2} {2: >2} {3: >2} {4: >2} {5: >2}\n'.format(
            self._board[0], self._board[1], self._board[2], self._board[3], self._board[4], self._board[5])
        s += ' {0: >2}                   {0: >2} \n'.format(
            self._board[13], self._board[6])
        s += '    {0: >2} {1: >2} {2: >2} {3: >2} {4: >2} {5: >2}'.format(
            self._board[12], self._board[11], self._board[10], self._board[9], self._board[8], self._board[7])
        return s

    # Called to calculate moves
    def move(self, idx):
        """Perform a move action on a given index, based on the current player"""
        if (self.over()):
            return self.score()

        # TODO: check if player is allowed to move this spot
        # ie, in their side of the board, it's actually a valid board spot, not empty, etc

        self._moves.append(idx)
        # Calculate stones in chosen hole
        count = self._board[idx]

        self._board[idx] = 0
        current_idx = idx

        # Player one moves right to left
        # Player two moves left to right
        motion = 1 if self._player_one else -1

        # While still stones to move
        while count > 0:
            current_idx += motion
            if (self._player_one and current_idx == 6):
                continue
            if ((not self._player_one) and current_idx == 13):
                continue
            self._board[current_idx] += 1
            count -= 1  # one less stone to move

        # Flip the current player IFF the turn ends on a new spot
        self._player_one = self._player_one if idx == current_idx else not self._player_one

        return self.score()
