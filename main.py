## Gamboard based on this youtube tutorial
## https://www.youtube.com/watch?v=b4XP2IcI-Bg

import tkinter as tk
import colors as c
import random
import time

from matrix_operations import MatrixOperations

class Game(tk.Frame):
    """ The main game class, handles the GUI as well as the game logic. `use_ai` is a boolean that determines whether the AI should be used or not. `ai_delay` is the delay between each move of the AI."""
    def __init__(self, use_ai=False, ai_delay=0.1):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title('2048')
        self.matrix_operations = MatrixOperations()
       
        self.main_grid = tk.Frame(self, bg=c.GRID_COLOR, bd=3, width=600, height=600)
        self.main_grid.grid(pady=(100,0))
        self.makeGUI()
        self.startGame()
       
        if use_ai:
            self.ai_play(ai_delay, "montecarlo")
        else:
            self.master.bind("<Left>", self.left)
            self.master.bind("<Right>", self.right)
            self.master.bind("<Up>", self.up)
            self.master.bind("<Down>", self.down)
       
        self.mainloop()
           
           
## ***************************************************************************            
## ***************************************************************************            
## *********************** GAMEBOARD GUI SECTION *****************************
## ***************************************************************************            
## ***************************************************************************    

    # creates the GUI gameborad using tkinter
    def makeGUI(self):
        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                cell_frame = tk.Frame(self.main_grid, bg=c.EMPTY_CELL_COLOR, width= 150, height=150)
                cell_frame.grid(row=i, column=j, padx=5, pady=5)
                cell_number = tk.Label(self.main_grid, bg=c.EMPTY_CELL_COLOR)
                cell_number.grid(row=i, column=j)
                cell_data = {"frame": cell_frame, "number": cell_number}
                row.append(cell_data)
            self.cells.append(row)

        #Scoreboard Header Code
        score_frame = tk.Frame(self)
        score_frame.place(relx=0.5, y=45, anchor="center")
        tk.Label(score_frame, text="Score", font=c.SCORE_LABEL_FONT).grid(row=0)
        self.score_label = tk.Label(score_frame, text="0", font=c.SCORE_FONT)
        self.score_label.grid(row=1)
        
    # initialize the game board and GUI colors respectively
    def startGame(self):
        # creates the gamerboard matrix of all 0's
        self.matrix = [[0]*4 for x in range(4)]
        
        # fill the board with 2 random 2's
        row = random.randint(0,3)
        col = random.randint(0,3)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])
        self.cells[row][col]["number"].configure(bg=c.CELL_COLORS[2], fg=c.CELL_NUMBER_COLORS[2], font=c.CELL_NUMBER_FONTS[2], text="2")
        
        while(self.matrix[row][col] != 0):
            row = random.randint(0,3)
            col = random.randint(0,3)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])
        self.cells[row][col]["number"].configure(bg=c.CELL_COLORS[2], fg=c.CELL_NUMBER_COLORS[2], font=c.CELL_NUMBER_FONTS[2], text="2")
        
        self.score = 0
        
    # add a new 2 or 4 to the board after a move is executed
    def addNewTile(self):
        row = random.randint(0,3)
        col = random.randint(0,3)
        while(self.matrix[row][col] != 0):
            row = random.randint(0,3)
            col = random.randint(0,3)
        self.matrix[row][col] = random.choice([2,4])
        
    #update the GUi based on the matrix
    def updateGUI(self):
        for i in range(4):
            for j in range(4):
                cell_value = self.matrix[i][j]
                if cell_value == 0:
                    self.cells[i][j]["frame"].configure(bg=c.EMPTY_CELL_COLOR)
                    self.cells[i][j]["number"].configure(bg=c.EMPTY_CELL_COLOR, text="")
                else:
                    self.cells[i][j]["frame"].configure(bg=c.CELL_COLORS[cell_value])
                    self.cells[i][j]["number"].configure(
                        bg=c.CELL_COLORS[cell_value], 
                        fg=c.CELL_NUMBER_COLORS[cell_value], 
                        font=c.CELL_NUMBER_FONTS[cell_value], 
                        text=str(cell_value))
        self.score_label.configure(text=self.score)
        self.update_idletasks()
        
    # after a move is executed, add a new tile, update the GUI, and check if the game is over
    def afterMoveFunction(self):
        self.addNewTile()
        self.updateGUI()
        self.isGameOver()
        
        
    # NOTE about the following 4 functions:
    # Instead of writing functions of combining the matrix in all 4 directions, 
    # I wrote one function that stacks the matrix in a certain direction, 
    # combines the matrix, and then stacks it back to its original orientation. 
    #
    # This is done by using the transpose and reverse functions from matrix_operations.py 
        
    # when left move is executed
    def left(self, event):
        if self.matrix_operations.can_move_left(self.matrix):
            self.matrix = self.matrix_operations.stack(self.matrix)
            self.matrix, self.score = self.matrix_operations.combine(self.matrix, self.score)
            self.matrix = self.matrix_operations.stack(self.matrix)
            self.afterMoveFunction()

    # when right move is executed
    def right(self, event):
        if self.matrix_operations.can_move_right(self.matrix):
            self.matrix = self.matrix_operations.reverse_matrix_row(self.matrix)
            self.matrix = self.matrix_operations.stack(self.matrix)
            self.matrix, self.score = self.matrix_operations.combine(self.matrix, self.score)
            self.matrix = self.matrix_operations.stack(self.matrix)
            self.matrix = self.matrix_operations.reverse_matrix_row(self.matrix)
            self.afterMoveFunction()

    # when up move is executed
    def up(self, event):
        if self.matrix_operations.can_move_up(self.matrix):
            self.matrix = self.matrix_operations.transpose_matrix_row(self.matrix)
            self.matrix = self.matrix_operations.stack(self.matrix)
            self.matrix, self.score = self.matrix_operations.combine(self.matrix, self.score)
            self.matrix = self.matrix_operations.stack(self.matrix)
            self.matrix = self.matrix_operations.transpose_matrix_row(self.matrix)
            self.afterMoveFunction()
    
    # when down move is executed
    def down(self, event):
        if self.matrix_operations.can_move_down(self.matrix):
            self.matrix = self.matrix_operations.transpose_matrix_row(self.matrix)
            self.matrix = self.matrix_operations.reverse_matrix_row(self.matrix)
            self.matrix = self.matrix_operations.stack(self.matrix)
            self.matrix, self.score = self.matrix_operations.combine(self.matrix, self.score)
            self.matrix = self.matrix_operations.stack(self.matrix)
            self.matrix = self.matrix_operations.reverse_matrix_row(self.matrix)
            self.matrix = self.matrix_operations.transpose_matrix_row(self.matrix)
            self.afterMoveFunction()
    
    # check if a horizontal move is possible -- could be improved
    def horizontalMoveExists(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j+1]:
                    return True
        return False
    
    # check if a horizontal move is possible -- could be improved
    def verticalMoveExists(self):
        for i in range(3):
            for j in range(4):
                if self.matrix[i][j] == self.matrix[i+1][j]:
                    return True
        return False
    
    # chekc if the game is over
    def isGameOver(self):
        if any(2048 in row for row in self.matrix):
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(game_over_frame, text="You Win!",
                     bg= c.WINNER_BG,
                     fg=c.GAME_OVER_FONT_COLOR,
                     font=c.GAME_OVER_FONT).pack()
            return True
        elif not any(0 in row for row in self.matrix) and not self.horizontalMoveExists() and not self.verticalMoveExists():
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(game_over_frame, text="Game Over!",
                     bg= c.LOSER_BG,
                     fg=c.GAME_OVER_FONT_COLOR,
                     font=c.GAME_OVER_FONT).pack()
            return True
        
    
## ***************************************************************************            
## ***************************************************************************            
## **************************** AI SECTION ***********************************
## ***************************************************************************            
## ***************************************************************************            

    # AI player         
    def ai_play(self, ai_delay, agent):
        print(" **** STARTING AI PLAYER **** ")
        scores = []
        num_games = 100
        wins = 0
        start = time.time()
        for game_num in range(1, num_games + 1):
            print(f"Game {game_num} / {num_games}")
            while not self.isGameOver():
                if agent == "expectimax":
                    _, best_move = self.minimax(self.matrix, depth=1, maximizing_player=True)
                    print("Best Move is:", best_move)
                    
                    if(best_move == "left" and self.matrix_operations.can_move_left(self.matrix) == False):
                        print("Can't move left")
                        best_move = "right"
                        print("Changed Best Move:", best_move)
                    elif(best_move == "right" and self.matrix_operations.can_move_right(self.matrix) == False):
                        print("Can't move right")
                        best_move = "left"
                        print("Changed Best Move:", best_move)
                    elif(best_move == "up" and self.matrix_operations.can_move_up(self.matrix) == False):
                        print("Can't move up")
                        best_move = "down"
                        print("Changed Best Move:", best_move)
                    elif(best_move == "down" and self.matrix_operations.can_move_down(self.matrix) == False):
                        print("Can't move down")
                        best_move = "up"
                        print("Changed Best Move:", best_move)
                    elif(best_move == None):
                        print("No best move")
                        best_move = random.choice(["left", "right", "up", "down"])
                        print("Changed Best Move:", best_move)
                    
                    if best_move == "left":
                        self.left(None)
                    elif best_move == "right":
                        self.right(None)
                    elif best_move == "up":
                        self.up(None)
                    elif best_move == "down":
                        self.down(None)
                    self.update()
                    time.sleep(ai_delay)
                
                if agent == "montecarlo":
                    best_move = self.montecarlo(self.matrix)
                    
                    if best_move == "left":
                        self.left(None)
                    elif best_move == "right":
                        self.right(None)
                    elif best_move == "up":
                        self.up(None)
                    elif best_move == "down":
                        self.down(None)
                    
                    self.update()
                    time.sleep(ai_delay)
        
            if any(2048 in row for row in self.matrix):
                wins += 1

            scores.append(self.score)
            self.startGame()
        
        end = time.time()

        print("All games completed. Scores:")
        print(scores)
        print("Wins:")
        print(wins)
        print("Total Time:")
        print(end - start)

    def minimax(self, node, depth, maximizing_player):
        if depth == 0 or not self.horizontalMoveExists() and not self.verticalMoveExists():
            return self.evaluate_board(node), None

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            moves = ["left", "right", "up", "down"]
            # random.shuffle(moves)
            for move in moves:
                new_node, score = self.matrix_operations.get_new_state(node, move)
                evalLocal, _ = self.minimax(new_node, depth - 1, False)
                # evalLocal += score  # Add the score to the evaluation
                if evalLocal > max_eval:
                    max_eval = evalLocal
                    best_move = move
            return max_eval, best_move
        else:
            min_eval = float('inf')
            empty_cells = [(i, j) for i in range(4) for j in range(4) if node[i][j] == 0]
            for cell in empty_cells:
                for value in [2, 4]:
                    new_node, score = self.matrix_operations.get_new_state(node, move)
                    evalLocal, _ = self.minimax(new_node, depth - 1, True)
                    # evalLocal += score  # Add the score to the evaluation
                    min_eval = min(min_eval, evalLocal)
            return min_eval, None
    
    def montecarlo(self, board):
        """
        Idead: Considering each possible move, make 50 moves ahead. Whatever inital move get's us the highest score 50
        moves ahead is our best move.
        """
        simulation_scores = {} # resulting scores for each initial move
        best_move = None #Trying to figure out
        initial_moves = self.matrix_operations.get_possible_moves(board) # Get the legal moves given the current board
        for move in initial_moves:
            simulation_scores[move] = 0 # all legal moves have a starting score of zero
        simulation_steps = 10 # Look 10 moves ahead
        num_simulations = 250 #simulate each initial move x times

        for move in initial_moves:
            #simulated_board = board
            for i in range(num_simulations):
                simulated_board, current_score = self.matrix_operations.get_new_state(board, move) # initial move
                simulated_board = self.matrix_operations.addNumber(simulated_board) # add a new number
                board_evaluation = self.montecarlo_evaluation(simulated_board, current_score) # evaluate current state
                legal_moves = self.matrix_operations.get_possible_moves(simulated_board) #check legal moves

                moves_ahead = 0
                while len(legal_moves)!=0 and moves_ahead < simulation_steps:
                    next_move = random.choice(legal_moves) #get next move
                    simulated_board, current_score = self.matrix_operations.get_new_state(simulated_board, next_move) #make move
                    simulated_board = self.matrix_operations.addNumber(simulated_board) # update new number
                    
                    board_evaluation = self.montecarlo_evaluation(simulated_board, current_score) # evaluate current state
                    legal_moves = self.matrix_operations.get_possible_moves(simulated_board) #check legal moves
                    moves_ahead += 1
                
                simulation_scores[move] += board_evaluation
        
        if simulation_scores:
            best_move = max(simulation_scores, key=simulation_scores.get)
        else:
            best_move = random.choice(legal_moves)
        return best_move

    def evaluate_board(self, node):
        # Simple evaluation function, can be improved
        empty_cells = sum(row.count(0) for row in node)
        max_tile = max(max(row) for row in node)
        score = self.score
        return empty_cells + max_tile + score
    
    def montecarlo_evaluation(self, board, score):
        empty_cells = sum(row.count(0) for row in board)
        max_tile = max(max(row) for row in board)
        return 200 * empty_cells + 2 * max_tile + score

def main():
    # use_ai -- True if you want the AI to play the game, False if you want to play the game yourself
    # ai_delay -- the delay between each move of the AI, in seconds
    Game(use_ai=True, ai_delay=0.0)
    
if __name__ == "__main__":
    main()
        