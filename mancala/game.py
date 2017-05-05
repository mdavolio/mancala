# -*- coding: utf-8 -*-
"""
Mancala Game object
Everything required to play a game. Includes rule validation.
"""


class Game():
    """Represents a mancala game."""
    _default_board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]

    def __init__(self,
                 board=None,
                 player_turn=None,
                 moves=None,
                 history=None):

        # creates board, 2 players by 6 holes
        self._board = Game._default_board[:] if board is None else board
        # so the board looks like 00 01 02 03 04 05
        #                      13                   06
        #                         12 11 10 09 08 07
        # Player 1 scores in 06 and Player 2 scores in 13

        self._player_one = True if player_turn is None else (player_turn == 1)
        self._moves = [] if moves is None else moves
        self._history = [] if history is None else history

    def board(self):
        """Current game board"""
        return self._board[:]

    def history(self):
        """Array of game boards"""
        return self._history[:]

    def moves(self):
        """Array of game moves"""
        return self._moves[:]

    def turn_player(self):
        """Check number of current player"""
        return 1 if self._player_one else 2

    def score(self):
        """Returns the current score of the game"""
        return Game.score_board(self._board)

    def winner(self):
        """Returns the winner player number, or 0 if the game isn't over"""
        if not self.over():
            return 0
        return 1 if self.score()[0] > self.score()[1] else 2

    @staticmethod
    def score_board(board):
        """Scores a Mancala board"""
        return (board[6], board[13])

    def side_empty(self):
        """True is either player's side is empty of stones."""
        stones_left_01 = sum(self._board[0:6])
        stones_left_02 = sum(self._board[7:13])
        return stones_left_01 == 0 or stones_left_02 == 0

    def over(self):
        """True if the game is over"""
        return self.side_empty() or self._board[6] >= 25 or self._board[13] >= 25

    def board_render(self):
        """Renders the current board to a viewable string"""
        # There are certainly better ways to render this
        result = '    {0: >2} {1: >2} {2: >2} {3: >2} {4: >2} {5: >2}\n'.format(
            self._board[0], self._board[1], self._board[2],
            self._board[3], self._board[4], self._board[5])
        result += ' {0: >2}                   {1: >2} \n'.format(
            self._board[13], self._board[6])
        result += '    {0: >2} {1: >2} {2: >2} {3: >2} {4: >2} {5: >2}'.format(
            self._board[12], self._board[11], self._board[10],
            self._board[9], self._board[8], self._board[7])
        return result

    @staticmethod
    def idx_player_1(idx):
        """True is index is in player 1's zone"""
        return idx <= 5 and idx >= 0

    @staticmethod
    def idx_player_2(idx):
        """True is index is in player 2's zone"""
        return idx >= 7 and idx <= 12

    @staticmethod
    def own_zone(idx, player):
        """True if index is in (boolean True == 1) player's zone"""
        if player:
            return Game.idx_player_1(idx)
        else:
            return Game.idx_player_2(idx)

    def clone(self):
        """Return a clone of the game object"""
        return Game(
            self.board(),
            self.turn_player(),
            self.moves(),
            self.history()
        )

    def clone_turn(self):
        '''Return a clone of the game object but transformed'''
        if self.turn_player() == 1:
            return self.clone(), False
        else:
            rot_board = self.board()[7:14] + self.board()[0:7]
            return Game(
                rot_board,          # return rotated board
                1                  # change player back to 1
            ), True


    @staticmethod
    def rotate_board(rot_flag, move):
        '''True if player changes in order to rotate board'''
        if rot_flag:
            return move + 7
        else:
            return move

    # Called to calculate moves
    def move(self, idx):
        """Perform a move action on a given index, based on the current player"""

        if self.over():
            return self.score()

        # Illegal move if empty hole
        if self._board[idx] == 0:
            return self.score()
        # Illegal move if score hole chosen ... not really necessary but keep
        # for now
        if idx == 6 or idx == 13:
            return self.score()
        # Illegal p1 choose p2
        if self._player_one and not Game.idx_player_1(idx):
            return self.score()
        if not self._player_one and not Game.idx_player_2(idx):
            return self.score()

        self._moves.append(idx)
        self._history.append(self._board[:])
        # Calculate stones in chosen hole
        count = self._board[idx]

        self._board[idx] = 0
        current_idx = idx

        # While still stones to move
        while count > 0:
            current_idx = (current_idx + 1) % len(self._board)
            if self._player_one and current_idx == 13:
                continue
            if (not self._player_one) and current_idx == 6:
                continue
            self._board[current_idx] += 1
            count -= 1  # one less stone to move

        # If last stone ends in score go again
        if current_idx == 6 or current_idx == 13:
            return self.score()

        # Capture rule
        if(self._board[current_idx] == 1 and self._board[12 - current_idx] >= 1 and
           Game.own_zone(current_idx, self._player_one)):
            if((self._board[12 - current_idx] != sum(self._board[0:6]) and not self._player_one) or
               ((self._board[12 - current_idx] != sum(self._board[7:13]) and self._player_one))):
                extra_stones = 1 + self._board[12 - current_idx]
                self._board[12 - current_idx] = 0
                self._board[current_idx] = 0
                if self._player_one:
                    self._board[6] += extra_stones
                else:
                    self._board[13] += extra_stones

        if self.side_empty():
            self._board[6] += sum(self._board[0:6])
            self._board[13] += sum(self._board[7:13])
            self._board[0:6] = [0, 0, 0, 0, 0, 0]
            self._board[7:13] = [0, 0, 0, 0, 0, 0]
            return self.score()

        # Flip the current player IFF the turn ends on a new spot
        self._player_one = self._player_one if idx == current_idx else not self._player_one

        return self.score()
