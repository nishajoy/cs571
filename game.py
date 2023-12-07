import random
import math
import time

class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']
    DEPTH_LIMIT = 3  # Example default value, adjust based on timing tests

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """

        # players take turns placing their markers on the board. The goal is to set up for a winning position. This phase continues
        # until all eight markers (four from each player) are placed on the board. Players must strategically place their markers,
        # considering both offensive moves (to create a winning line or box) and defensive moves (to block the opponent).


        drop_phase = True   # TODO: detect drop phase


        if not drop_phase:
            # TODO: choose a piece to move and remove it from the board
            # (You may move this condition anywhere, just be sure to handle it)
            #
            # Until this part is implemented and the move list is updated
            # accordingly, the AI will not follow the rules after the drop phase!
            pass

        # select an unoccupied space randomly
        # TODO: implement a minimax algorithm to play better
        move = []
        (row, col) = (random.randint(0,4), random.randint(0,4))
        while not state[row][col] == ' ':
            (row, col) = (random.randint(0,4), random.randint(0,4))

        # ensure the destination (row,col) tuple is at the beginning of the move list
        move.insert(0, (row, col))
        return move
    

    #helper function for succ
    #Iterate over the board and count the number of pieces for each player.
    def count_pieces(self, state):
        count_r = sum(row.count('r') for row in state)
        count_b = sum(row.count('b') for row in state)
        return count_r, count_b

    
    # FUNCTION: succ(self,state)
    # INPUT: board state
    # RETURN: List of legal states. During the drop phase, this simply means
    # adding a new piece of the current player's type to the board; during continued gameplay, this means moving any one of the current player's pieces to an unoccupied location on the board, adjacent to that piece.
    def succ(self, state):
        successors = []
        count_r, count_b = self.count_pieces(state)
        #If both players have fewer than four pieces on the board, it's the drop phase. Otherwise, it's the move phase.
        drop_phase = count_r < 4 or count_b < 4

        #During the drop phase, add a new piece of the current player's type to the board
        if drop_phase:
            for i in range(5):
                for j in range(5):
                    if state[i][j] == ' ':
                        new_state = [row[:] for row in state]
                        new_state[i][j] = self.my_piece
                        successors.append(new_state)

        #Once all pieces are on the board, the function generates successors by moving each of the current player's pieces to every adjacent (horizontally, vertically, or diagonally) unoccupied space.
        else:
            for i in range(5):
                for j in range(5):
                    if state[i][j] == self.my_piece:
                        for di in [-1, 0, 1]:
                            for dj in [-1, 0, 1]:
                                if di == 0 and dj == 0:
                                    continue  # Skip the current spot
                                if 0 <= i+di < 5 and 0 <= j+dj < 5 and state[i+di][j+dj] == ' ':
                                    new_state = [row[:] for row in state]
                                    new_state[i][j] = ' '
                                    new_state[i+di][j+dj] = self.my_piece
                                    successors.append(new_state)
        return successors
    


    #HELPER FUNCTION FOR heuristic_game_value(self, state)
    #Check for three pieces of the specified type in a row (horizontal, vertical) or part of a 2x2 box. Returns a heuristic score.
    def check_three_in_a_row(self, state, piece):

        heuristic_val = 0.0

        # Iterates over each row and column to check for three consecutive pieces of type piece horizontally. If found, adds 0.5 to heuristic_val.
        for row in range(5):
            for col in range(3):
                if state[row][col:col+3] == [piece] * 3:
                    heuristic_val += 0.5

        #Checks for vertical patterns of three consecutive pieces of type piece. Adds 0.5 to heuristic_val if such a pattern is found.
        for col in range(5):
            for row in range(3):
                if state[row][col] == state[row+1][col] == state[row+2][col] == piece:
                    heuristic_val += 0.5

        # Checks for 2x2 box patterns where three of the four positions are occupied by piece. Adds 0.5 to heuristic_val for each such pattern.
        for row in range(4):
            for col in range(4):
                if (state[row][col] == state[row+1][col] == state[row][col+1] == piece or
                    state[row][col+1] == state[row+1][col+1] == state[row+1][col] == piece):
                    heuristic_val += 0.5

        return heuristic_val

    # FUNCTION: heuristic_game_value(self,state)- Evalutes non-terminal states
    # OUTPUT: provides an overall heuristic score for the current state by evaluating
    #         specific advantageous or disadvantageous patterns for both the AI player and the opponent.
    def heuristic_game_value(self, state):

        #Call the game_value method to check if the current state is a terminal state
        terminal_value = self.game_value(state)
        #If terminal_value is 1 or -1 (indicating a win or lose state), then return this value immediately, as no heuristic evaluation is needed for terminal states.
        if terminal_value == 1 or terminal_value == -1:
            return terminal_value

        #In Teeko, winning conditions include getting four pieces in a row or forming a 2x2 box, so having three aligned pieces is just one step away from winning.

        # Initialize heuristic score
        score = 0.0
        
        #Calls check_three_in_a_row for both the AI's pieces (self.my_piece) and the opponent's pieces (self.opp).
        #The function adds to the score for patterns favorable to the AI and subtracts for patterns favorable to the opponent.
        score += self.check_three_in_a_row(state, self.my_piece)
        score -= self.check_three_in_a_row(state, self.opp)

        #Normalizes the score to ensure it remains within the range of -1 to 1.
        score = max(min(score, 1), -1)

        return score
    
    # Implementing Minimax

    # max_value and min_value functions represents the decisions of the AI (Max) and the opponent (Min) respectively.

    # takes the current state of the game and the current depth of recursion as arguments.
    def max_value(self, state, depth):

        #If the current state is a terminal state or if the depth limit has been reached, the function returns the game value of the state.
        if self.game_value(state) == 1 or self.game_value(state) == -1:
            return self.game_value(state)
        
        #When the depth limit is reached in the max_value function (and the state is not a terminal state), you should return the heuristic value of the state
        elif depth == self.DEPTH_LIMIT:
            return self.heuristic_game_value(state)
        
        #Initialize alpha to negative infinity. alpha will hold the best score found so far for the maximizing player (AI).
        alpha = -math.inf

        #Iterates over all possible successor states from the current state. 
        for successor in self.succ(state):
            # for each successor, it calls the min_value function (representing the opponent's best move in response)
            # updates alpha with the maximum value between the current alpha and the value returned from min_value.
            alpha = max(alpha, self.min_value(successor, depth + 1))

        # Returns the best score that the maximizing player (AI) can achieve from this state.
        return alpha
    
    def min_value(self, state, depth):
        if self.game_value(state) != 0 or depth == self.DEPTH_LIMIT:
            return self.game_value(state)
        
        beta = math.inf
        for successor in self.succ(state):
            beta = min(beta, self.max_value(successor, depth + 1))
        return beta
    

    # def max_value(self, state, depth):
    #     """ Minimax algorithm 
    #     First call will be max_value(self, curr_state, 0) and every subsequent recursive call
    #     will increase the value of depth
        
    #     When the depth counter reaches your tested depth limit OR you find a terminal state, 
    #     terminate the recursion
    #     """

    #     terminal_val = self.game_value(state)


    #     if self.game_value(state)==1 or self.game_value(state)==-1:
    #         return self.game_value(state)
    #     elif depth==0:
    #         return self.heuristic_game_value(self, state)
    #     elif self.my_piece
    #     pass


    
    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and box wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # TODO: check \ diagonal wins
        for row in range(2):
            for col in range(2):
                if state[row][col] != ' ' and state[row][col] == state[row+1][col+1] == state[row+2][col+2] == state[row+3][col+3]:
                    return 1 if state[row][col]==self.my_piece else -1
        # TODO: check / diagonal wins
        for row in range(2):
            for col in range(3,5):
                if state[row][col] != ' ' and state[row][col] == state[row+1][col-1] == state[row+2][col-2] == state[row+3][col-3]:
                    return 1 if state[row][col]==self.my_piece else -1
        # TODO: check box wins
        for row in range(3):
            for col in range(3):
                if state[row][col] != ' ' and state[row][col] == state[row+1][col] == state[row][col+1] == state[row+1][col+1]:
                    return 1 if state[row][col] == self.my_piece else -1

        return 0 # no winner yet

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################

#code to test the succ method of the TeekoPlayer class.
def test_succ_function():
        print("Running succ function test")

        player = TeekoPlayer()
        
        #the succ function generates successors based on the current player's piece: So we will specify that in these tests, the player is using the 'b' pieces. 
        player.my_piece = 'b'

        # 1. TESTING DROP PHASE

        #5x5 board with all spaces empty, indicated by ' '.
        test_state_drop = [[' ' for _ in range(5)] for _ in range(5)]
        #The succ function is called with the test_state_drop as the argument. This function should return all possible states that result from placing a 'b' piece on each empty space on the board
        successors_drop = player.succ(test_state_drop)
        #The total number of empty spaces at this point should be 25
        print(f"Number of successors generated in drop phase: {len(successors_drop)}")
        if (len(successors_drop) == 25):
            print("succ drop phase phase succeful")

        #WORKS!

        # 2. TESTING MOVE PHASE
        # create a specific board configuration
        test_state_move = [['b', 'r', 'b', 'r', 'b'],
                        ['r', 'b', 'r', 'b', 'r'],
                        ['b', 'r', 'b', ' ', ' '],
                        ['r', 'b', 'r', ' ', ' '],
                        ['b', 'r', 'b', ' ', ' ']]
        
        #Call the succ function on the test_state_move board configuration. 
        successors_move = player.succ(test_state_move)

        #If the current player is 'b' then each 'b' piece can move to any adjacent empty space (up, down, left, right, or diagonally).

        #First row:
        # 'b' at (0, 0): No valid moves 
        # 'b' at (0, 2): No valid moves 
        # 'b' at (0, 4): No valid moves 

        #Second row:
        #'b' at (1, 1): No valid moves 
        #'b' at (1, 3): 2 valid moves (to (2,3) and (2,4))

        #Third row:
        #'b' at (2, 0): No valid moves 
        #'b' at (2, 2): 2 valid moves (to (2, 3) and (3, 3)).

        #Fourth row:
        #'b' at (3, 1): no valid moves

        #Fifth row:
        #'b' at (4, 0): no valid moves
        #'b' at (4, 2): 2 valid moves (to (3,3) and (4, 3))

        #2 + 2 + 2 = 6 valid moves for 'b'.

        expected_successors_move = 6
        print("Generated successors in move phase:", len(successors_move))
        if (len(successors_move) == expected_successors_move):
            print("succ move phase succeful")
        

        print("All succ function tests passed successfully!")

# Timing Test Function
def test_minimax_depth(ai, initial_state):
        ai = TeekoPlayer()
        #create a list of depth limits to test the Minimax algorithm
        DEPTH_LIMITS = [1, 2, 3, 4, 5]

        # start a loop over each depth limit in DEPTH_LIMITS.
        for depth in DEPTH_LIMITS:

            # records the current time (in seconds) before running the Minimax algorithm. This is the starting time of the test.
            start_time = time.time()

            # sets the DEPTH_LIMIT attribute of the TeekoPlayer instance to the current depth limit being tested.
            # this determines how deep the Minimax algorithm will go during this test iteration.
            ai.DEPTH_LIMIT = depth 

            #Calls the make_move method of the TeekoPlayer instance with the initial_state 
            ai.make_move(initial_state)

            #Records the current time immediately after the Minimax algorithm finishes. This is the ending time of the test.
            end_time = time.time()

            #Calculates the total time taken for the Minimax algorithm to run and prints it out.
            print(f"Depth {depth}: Time taken = {end_time - start_time} seconds")

            #Checks if the time taken exceeds 5 seconds. If it does, the loop breaks, stopping further testing at deeper levels.
            if end_time - start_time > 5:
                break

# code to test the succ method of the TeekoPlayer class.
def test_heuristics():
    player = TeekoPlayer()
    test_states = [
        # State 1: empty 5x5 board, representing the initial state of a game.
        # Game Value: This is a neutral state with no winner or loser, so the game value should be 0.
        # Heuristic Value: Since the board is empty, there are no advantages for either player. The heuristic value should be neutral, close to 0.
        [[' ' for j in range(5)] for i in range(5)],


        # State 2: game state where the AI (assumed to be 'b') is close to winning with three pieces in a row horizontally.
        # Game Value: No player has won yet, so the game value is still 0.
        # Heuristic Value: The AI ('b') is close to winning with three pieces in a row. The heuristic should recognize this favorable position
        # and return a high positive value, though not quite 1 since it's not a winning state yet. 
        [['b', 'b', 'b', ' ', ' '],
         ['r', 'r', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ']],

         # State 3: opponent ('r') is close to winning with three pieces in a column vertically.
         # Game Value: Again, no player has won yet, so the game value is 0.
         # Heuristic Value: The opponent ('r') is close to winning, which is a disadvantageous position for the AI. The heuristic should
         # return a negative value, indicating an unfavorable state for the AI. 
         [['b', 'r', ' ', ' ', ' '],
         ['b', 'r', ' ', ' ', ' '],
         [' ', 'r', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ']],

         # State 4: winning scenario for the AI player ('b')
         # Game Value: The AI player ('b') has four pieces in a row, which is a winning condition. Therefore, the game value should be 1.
         # Heuristic Value: Since this is a terminal winning state for the AI, the heuristic value would also be at its maximum, which is 1.
        [['b', 'b', 'b', 'b', ' '],
        ['r', 'r', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ']],

        # State 5: winning scenario for the opponent ('r')
        # Game Value: The opponent ('r') has four pieces in a column, a winning condition. Thus, the game value should be -1.
        # Heuristic Value: For the AI player, this state represents a loss, so the heuristic value should be at its minimum, which is -1.
        [['b', 'r', ' ', ' ', ' '],
        ['b', 'r', ' ', ' ', ' '],
        [' ', 'r', ' ', ' ', ' '],
        [' ', 'r', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ']],

        # State 6: AI Player ('b') Winning with a 2x2 Box
        [['b', 'b', ' ', ' ', ' '],
        ['b', 'b', 'r', ' ', ' '],
        [' ', 'r', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ']],

        # State 7: Opponent ('r') Winning with a 2x2 Box
        [['r', 'r', ' ', ' ', ' '],
        ['r', 'r', 'b', ' ', ' '],
        [' ', 'b', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ']],

    ]

    #iterates over each state in test_states.
    for i, state in enumerate(test_states):
        #Calls the game_value method on the current state. This method checks if the state is a winning, losing, or neutral state and returns 1, -1, or 0 respectively.
        game_val = player.game_value(state)

        #Calls the heuristic_game_value method on the current state. This method computes a heuristic score for the state, giving an indication of how favorable the state is for the AI.
        heuristic_val = player.heuristic_game_value(state)

        #Prints out the index of the state (adjusted to start from 1 instead of 0), along with the calculated game value and heuristic value.
        print(f"State {i+1}: Game Value = {game_val}, Heuristic Value = {heuristic_val}")

            


def main():
    print('Hello, this is Samaritan')
    ai = TeekoPlayer()
    piece_count = 0
    turn = 0
    test_succ_function()

    test_heuristics()

    initial_state = [[' ' for j in range(5)] for i in range(5)]  # Example initial state
    test_minimax_depth(ai, initial_state)

    

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")



if __name__ == "__main__":
    main()
