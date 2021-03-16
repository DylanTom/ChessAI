import random

pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N":3, "P":1}
checkmate = 1000
stalemate = 0

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]

#Maximize your own score
def findGreedyMove(gameState, validMoves):
    turnMultiplier = 1 if gameState.whiteToMove else -1
    maxScore = -checkmate
    bestMove = None
    for playerMove in validMoves:
        gameState.makeMove(playerMove)
        if gameState.checkmate:
            score = checkmate
        elif gameState.stalemate:
            score = stalemate
        else:
            score = turnMultiplier * scoreMaterial(gameState.board)
        if score > maxScore:
            score = maxScore
            bestMove = playerMove
        gameState.undoMove()
    return bestMove

def scoreMaterial(board):
    score = 0
    for rank in board:
        for square in rank:
            if square[0] == "w":
                score += pieceScore[square[1]]
            elif square[0] == "b":
                score -= pieceScore[square[1]]

    return score