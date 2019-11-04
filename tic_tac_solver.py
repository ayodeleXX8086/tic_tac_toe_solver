from random import randint

import sys


class FailedValidation(Exception):
    def __init__(self):
        pass

def convert_board_to_string(board):
    board_str=""
    for i in range(3):
        for j in range(3):
            board_str+='+' if board[i][j]==' ' else board[i][j]
    return board_str


def __board_is_empty(board):
    """
    Checks if the board is empty
    :param board:
    :return:
    """
    is_empty=True
    for i in range(3):
        for j in range(3):
            if not board[i][j]==' ':
                return False
    return is_empty

def __validate_board(board):
    if check_if_board_is_full(board):
        return False
    count_x,count_y=0,0
    for i in range(3):
        for j in range(3):
            if not board[i][j] in [' ','X','O']:
                raise FailedValidation
            count_x += 1 if board[i][j]=='X' else 0
            count_y += 1 if board[i][j]=='O' else 0
    return abs(count_x-count_y)==0 or (count_x-1)==count_y

def check_winner(board):
    for i in range(3):
        winner = False if board[i][0]==' ' else (board[i][0]==board[i][1]) and (board[i][1]==board[i][2])
        if winner:
            return (board[i][0],True)
    for i in range(3):
        winner = False if board[0][i]==' ' else (board[0][i]==board[1][i]) and (board[1][i]==board[2][i])
        if winner:
            return (board[0][i],True)
    winner = False if board[0][0]==' ' else (board[0][0]==board[1][1]) and (board[1][1]==board[2][2])
    if winner:
        return (board[0][0],True)
    winner = False if board[0][2]==' ' else (board[0][2] == board[1][1]) and (board[1][1] == board[2][0])
    if winner:
        return (board[0][2],True)
    return None

def solve_tic_tac(board_str):
    """
    This is function solves for the best path for the O move, the player is identified as X and
    the computer is identified as O
    :param board_str: This takes a string of length 9, with character's such as +,X,O
    :return: returns a string of length 9 with the best move of O
    """
    try:
        size = len(board_str) # Validate the length
        if size<9 or size>9:
            raise FailedValidation

        board  = construct_board(board_str) # Convert the string to a two dimensional board
        result = __validate_board(board)   # Validate that the board has the right characters
        if not result:
            raise FailedValidation
        winner_result = check_winner(board) # Check if the opponent returned a winning string before deciding O's move
        if winner_result:
            return convert_board_to_string(board)
        if __board_is_empty(board): # Check if the board is empty then randomly select a position in board and Move O to that position
            row = randint(0,2)
            col = randint(0,2)
            board[row][col]="O"
            return convert_board_to_string(board)
        points = []
        __min_max_solver(board,0,points,True)
        # Deciding the best position based on the points and result solved from the min_max solver
        best_point  = None
        best_result = None
        for p in points:
            if not best_result is None:
                if best_result<p[1]:
                    best_result=p[1]
                    best_point=p[0]
            else:
                best_point=p[0]
                best_result=p[1]
        board[best_point[0]][best_point[1]]='O' # Move O to the best point
        return convert_board_to_string(board) # Convert the board to the string format
    except Exception:
        raise FailedValidation




def construct_board(board_str):
    """
    :param board_str: Board in a string format such as +++++++++
    :return: returns a 2 d array of the formatted string
    """
    board = [[' ' for i in range(3)] for _ in range(3)]
    count=0
    for i in range(3):
        for j in range(3):
            board[i][j]= ' 'if board_str[count]=="+" else board_str[count]
            count+=1
    return board

def __get_children_board(board,computer):
    '''
    Based on the current state of the board, this function makes a valid move and
    returns the board with a move and the point of the move
    complexity O(N^M) N is the number of legal moves such as the Nodes of the graph and M is the depth of the Graph
    :param board: is a 2 dimensional board
    :param computer: Boolean variable that shows if it is a computer it set to True, if not is set to False
    :return: returns the board move and points
    '''
    cloned_board = [ [ v for v in i] for i in board]
    for i in range(3):
        for j in range(3):
            if cloned_board[i][j]==' ':
                cloned_board[i][j]='O' if computer else 'X'
                yield cloned_board,(i,j)

def check_if_board_is_full(board):
    is_full = True
    for i in range(3):
        for j in range(3):
            if board[i][j]==' ':
                return False
    return is_full

def __min_max_solver(board,depth,points,computer):
    '''
    To discover the best move by the computer it is ideal for the computer try all moves, this move is then traversed in a graph
    structure using a  DFS, for each move the computer will stimulates the user and computer playing different moves, it will then
    search for the path with the maximum possibility and the minimum possibilty of the user winning.
    For each node traversal there are three terminal states Such as (1) Computer winning, (-1) Computer lost, (0) A tie
    :param board: 2d array
    :param depth: depth how far as the board gone
    :param points: calculated points
    :param computer: player identity
    '''
    if check_winner(board):
        value = check_winner(board)[0]
        return 1 if value=='O' else -1

    if check_if_board_is_full(board):
        return 0

    if computer:
        best_value = -(sys.maxsize-1)
        for child in __get_children_board(board,computer):
            value = __min_max_solver(child[0],depth+1,points,False)
            if depth==0:
                points.append((child[1],value))
            child[0][child[1][0]][child[1][1]]=' '
            best_value =  max(best_value,value)
        return best_value

    else:
        best_value = sys.maxsize
        for child in __get_children_board(board,computer):
            value = __min_max_solver(child[0],depth+1,points,True)
            child[0][child[1][0]][child[1][1]] =' '
            best_value = min(best_value,value)
        return best_value

