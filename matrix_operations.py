import random

class MatrixOperations:
    @staticmethod
    def stack(matrix):
        new_matrix = [[0] * 4 for x in range(4)]
        for i in range(4):
            fill_position = 0
            for j in range(4):
                if matrix[i][j] != 0:
                    new_matrix[i][fill_position] = matrix[i][j]
                    fill_position += 1
        return new_matrix

    @staticmethod
    def combine(matrix, score):
        for i in range(4):
            for j in range(3):
                if matrix[i][j] != 0 and matrix[i][j] == matrix[i][j + 1]:
                    matrix[i][j] *= 2
                    matrix[i][j + 1] = 0
                    score += matrix[i][j]
        return matrix, score

    @staticmethod
    def reverse_matrix_row(matrix):
        new_matrix = []
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                new_matrix[i].append(matrix[i][3 - j])
        return new_matrix

    @staticmethod
    def transpose_matrix_row(matrix):
        new_matrix = [[0] * 4 for x in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j] = matrix[j][i]
        return new_matrix
    
    @staticmethod
    def get_new_state(node, move):
        new_state = [row[:] for row in node]
        score = 0
        if move == "left":
            new_state = MatrixOperations.stack(new_state)
            new_state, score = MatrixOperations.combine(new_state, 0)
            new_state = MatrixOperations.stack(new_state)
        elif move == "right":
            new_state = MatrixOperations.reverse_matrix_row(new_state)
            new_state = MatrixOperations.stack(new_state)
            new_state, score = MatrixOperations.combine(new_state, 0)
            new_state = MatrixOperations.stack(new_state)
            new_state = MatrixOperations.reverse_matrix_row(new_state)
        elif move == "up":
            new_state = MatrixOperations.transpose_matrix_row(new_state)
            new_state = MatrixOperations.stack(new_state)
            new_state, score = MatrixOperations.combine(new_state, 0)
            new_state = MatrixOperations.stack(new_state)
            new_state = MatrixOperations.transpose_matrix_row(new_state)
        elif move == "down":
            new_state = MatrixOperations.transpose_matrix_row(new_state)
            new_state = MatrixOperations.reverse_matrix_row(new_state)
            new_state = MatrixOperations.stack(new_state)
            new_state, score = MatrixOperations.combine(new_state, 0)
            new_state = MatrixOperations.stack(new_state)
            new_state = MatrixOperations.reverse_matrix_row(new_state)
            new_state = MatrixOperations.transpose_matrix_row(new_state)
        return new_state, score
    
    @staticmethod
    def can_move_left(matrix):
        for row in matrix:
            # Check if there is an empty space or adjacent equal values
            for j in range(1, len(row)):
                if row[j] != 0 and (row[j - 1] == 0 or row[j - 1] == row[j]):
                    return True
        return False

    @staticmethod
    def can_move_right(matrix):
        # Check if a right move is possible
        reversed_matrix = [row[::-1] for row in matrix]
        return MatrixOperations.can_move_left(reversed_matrix)

    @staticmethod
    def can_move_up(matrix):
        for col in range(len(matrix[0])):
            for row in range(1, len(matrix)):
                if matrix[row][col] != 0 and (matrix[row - 1][col] == 0 or matrix[row - 1][col] == matrix[row][col]):
                    return True
        return False

    @staticmethod
    def can_move_down(matrix):
        for col in range(len(matrix[0])):
            for row in range(len(matrix) - 1):
                if matrix[row][col] != 0 and (matrix[row + 1][col] == 0 or matrix[row + 1][col] == matrix[row][col]):
                    return True
        return False
    
    @staticmethod
    def get_possible_moves(matrix):
        acceptable_moves = []
        if MatrixOperations.can_move_up(matrix):
            acceptable_moves.append("up")
        
        if MatrixOperations.can_move_down(matrix):
            acceptable_moves.append("down")
        
        if MatrixOperations.can_move_left(matrix):
            acceptable_moves.append("left")
        
        if MatrixOperations.can_move_right(matrix):
            acceptable_moves.append("right")
        
        return acceptable_moves
    
    @staticmethod
    def addNumber(matrix):
        row = random.randint(0,3)
        col = random.randint(0,3)
        while(matrix[row][col] != 0):
            row = random.randint(0,3)
            col = random.randint(0,3)
        matrix[row][col] = random.choice([2,4])
        return matrix
