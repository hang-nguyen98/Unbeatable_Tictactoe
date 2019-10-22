# Tic Tac Toe

import random
MAX = 100
MIN = -100
DRAW_VALUE = 0
PLY = 9


"""
Prints out the board that it was passed.
Parameter:
    board: a list of 10 strings representing the board (ignore index 0)
"""
def drawBoard(board):

    print('   |   |')
    print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
    print('   |   |')


"""
Lets the player type which letter they want to be.
Returns a list with the player’s letter as the first item, and the computer's letter as the second.
"""
def inputPlayerLetter():
    letter = ''

    while not (letter == 'X' or letter == 'O'):
        print('Do you want to be X or O?')
        letter = input().upper()
         # the first element in the list is the player’s letter, the second is the computer's letter.
        if letter == 'X':
            return ['X', 'O']
        else:   
             return ['O', 'X']


"""Randomly choose the player who goes first."""
def whoGoesFirst():
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'

"""This function returns True if the player wants to play again, otherwise it returns False."""
def playAgain():
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')


def makeMove(board, letter, move):
    board[move] = letter


"""Given a board and a player’s letter, this function returns True if that player has won.
    # We use bo instead of board and le instead of letter so we don’t have to type as much."""
def isWinner(board, letter):
    return ((board[7] == letter and board[8] == letter and board[9] == letter) or # across the top
    (board[4] == letter and board[5] == letter and board[6] == letter) or # across the middle
    (board[1] == letter and board[2] == letter and board[3] == letter) or # across the bottom
    (board[7] == letter and board[4] == letter and board[1] == letter) or # down the left side
    (board[8] == letter and board[5] == letter and board[2] == letter) or # down the middle
    (board[9] == letter and board[6] == letter and board[3] == letter) or # down the right side
    (board[7] == letter and board[5] == letter and board[3] == letter) or # diagonal
    (board[9] == letter and board[5] == letter and board[1] == letter)) # diagonal


"""Make a duplicate of the board list and return it the duplicate."""
def getBoardCopy(board):
    copyBoard = []
    for i in board:
        copyBoard.append(i)
    return copyBoard


"""Return true if the passed move is free on the passed board."""
def isSpaceFree(board, move):
    return board[move] == ' '


"""Let the player type in their move."""
def getPlayerMove(board):
    move = ' '
    while move not in '1 2 3 4 5 6 7 8 9'.split() or not isSpaceFree(board, int(move)):
        print('What is your next move? (1-9)')
        move = input()
    return int(move)


"""Returns a valid move from the passed list on the passed board.
Returns None if there is no valid move."""
def chooseRandomMoveFromList(board, movesList):
    possibleMoves = []
    for i in movesList:
        if isSpaceFree(board, i):
            possibleMoves.append(i)

    if len(possibleMoves) != 0:
        return random.choice(possibleMoves)
    else:
        return None

"""
Generate a list of possible boards and possible moves for a player
Parameter:
    board: the current board/state of the game
    letter: decide on whose boards and moves we're returning, either player or computer
"""

def generateBoardList(board,computerLetter):
    possibleMoves = []
    boardList = []
    for i in range(1,10): # first spot of the board is always left empty
        if isSpaceFree(board, i):
            possibleMoves.append(i)
            copy = getBoardCopy(board)
            makeMove(copy, computerLetter, i) #board[move] = letter 
            boardList.append(copy)
    return boardList, possibleMoves
    #boardList the current states/position of robot and goal
    #possible moves is adjacent list



"""
Return the best value and best move for the computer
Parameter:
    isMaximizingPlayer: true if the next turn is computer's, false otherwise
    curBoard: the current state that the game is examining
    ply: how far ahead the search goes
    computerLetter, playerLetter: letters (X or O) that represent computer's move and player's move
"""

def minimax(isMaximizingPlayer, curBoard, ply, computerLetter, playerLetter):
 
    if isWinner(curBoard, computerLetter): #computer wins
        return [MAX-ply] 
    elif isWinner(curBoard, playerLetter): #player wins
        return [MIN+ply]
    elif isBoardFull(curBoard) or ply == PLY: #a tie, or the result isn't settled with ply layers:
        return [DRAW_VALUE]          

    else: #keep looking ahead
        #maximizing player's turn
        if isMaximizingPlayer:
            bestVal = -1000
            bestMove = None
            #boardList contains possible states of robot and goal for next move
            #possibleMoves is a list of intergers, representing computer's next move
            boardList, possibleMoves = generateBoardList(curBoard, computerLetter)

            #examine each possible state and pick the best one
            for i in range (len(possibleMoves)):
                value = minimax(False, boardList[i], ply+1, computerLetter, playerLetter)[0]
                if value >= bestVal:
                    bestVal = value
                    bestMove = possibleMoves[i]
            return bestVal, bestMove

        #minimizing player's turn
        else:
            
            bestVal = +1000
            bestMove = None
            #boardList contains possible states of robot and goal for next move
            #possibleMoves is a list of intergers, representing player's next move
            boardList, possibleMoves = generateBoardList(curBoard, playerLetter)

            for i in range (len(possibleMoves)):
                value = minimax(True, boardList[i], ply+1, computerLetter, playerLetter)[0]
                if value <= bestVal: 
                    bestVal = value
                    bestMove = possibleMoves[i]
            return bestVal, bestMove
                

"""
Returns True if every space on the board has been taken. Otherwise returns False.
"""
def isBoardFull(board):
    for i in range(1, 10):
        if isSpaceFree(board, i):
            return False
    return True

def main():
    print('Welcome to Tic Tac Toe!')
    while True:
        # Reset the board
        theBoard = [' '] * 10
        playerLetter, computerLetter = inputPlayerLetter()
        turn = whoGoesFirst()
        maximizingPlayer = turn
        print('The ' + turn + ' will go first.')
        gameIsPlaying = True
        
        while gameIsPlaying:
            if turn == 'player':
                # Player’s turn.
                drawBoard(theBoard)
                move = getPlayerMove(theBoard)
                makeMove(theBoard, playerLetter, move)
                print("You made a move at ", move)

                if isWinner(theBoard, playerLetter):
                    drawBoard(theBoard)
                    print('Hooray! You have won the game!')
                    gameIsPlaying = False
                else:
                    if isBoardFull(theBoard):
                        drawBoard(theBoard)
                        print('The game is a tie!')
                        break
                    else:
                        turn = 'computer'
            
            else: # Computer’s turn.
                copy = getBoardCopy(theBoard)
                move = minimax(True, copy, 0, computerLetter, playerLetter)[1]
                makeMove(theBoard, computerLetter, move)
                print("The computer made a move at ", move)

                if isWinner(theBoard, computerLetter):
                    drawBoard(theBoard)
                    print('The computer has beaten you! You lose.')
                    gameIsPlaying = False
                else:
                    if isBoardFull(theBoard):
                        drawBoard(theBoard)
                        print('The game is a tie!')
                        break
                    else:
                        turn = 'player'


        if not playAgain(): #inside while gameIsPlaying
            break
