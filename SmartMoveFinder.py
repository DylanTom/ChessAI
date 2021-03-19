import random
from ChessAI import PieceSquareTable

pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N":3, "P":1}

checkmate = 1000
stalemate = 0
depth = 3

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]

#Maximize your own score
def findBestMove(gameState, validMoves):
    turnMultiplier = 1 if gameState.whiteToMove else -1
    opponentMinMaxScore = checkmate
    bestPlayerMove = None
    random.shuffle(validMoves)
    #region minimize best move
    for playerMove in validMoves:
        gameState.makeMove(playerMove)
        #region maximize opponents best move
        opponentMoves = gameState.getValidMoves()
        if gameState.stalemate:
            opponentMaxScore = stalemate
        elif gameState.checkmate:
            opponentMaxScore = -checkmate
        else:
           opponentMaxScore = -checkmate
        for opponentMove in opponentMoves:
            gameState.makeMove(opponentMove)
            gameState.getValidMoves()
            if gameState.checkmate:
                score = checkmate
            elif gameState.stalemate:
                score = stalemate
            else:
                score = -turnMultiplier * scoreMaterial(gameState.board)
            if score > opponentMaxScore:
                opponentMaxScore = score
            gameState.undoMove()
        if opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        gameState.undoMove()
    return bestPlayerMove

def findBestMoveMinMax(gameState, validMoves):
    global nextMove
    nextMove = None
    findMoveNegaMaxAB(gameState, validMoves, depth, -checkmate, checkmate, 1 if gameState.whiteToMove else -1)
    return nextMove

def findMinMaxMove(gameState, validMoves, depthA, whiteToMove):
    global nextMove
    if depthA == 0:
        return scoreMaterial(gameState.board)

    if whiteToMove:
        maxScore = -checkmate
        random.shuffle(validMoves)
        for i in validMoves:
            gameState.makeMove(i)
            nextMoves = gameState.getValidMoves()
            score = findMinMaxMove(gameState,nextMoves, depthA-1, False)
            if score > maxScore:
                maxScore = score
                if depthA == depth:
                    nextMove = i
            gameState.undoMove()
        return maxScore

    else:
        minScore = checkmate
        for i in validMoves:
            gameState.makeMove(i)
            nextMoves = gameState.getValidMoves()
            score = findMinMaxMove(gameState, nextMoves, depthA -1, True)
            if score < minScore:
                minScore = score
                if depthA == depth:
                    nextMove = i
            gameState.undoMove()
        return minScore

def findMoveNegaMax(gameState, validMoves, depthA, turnMultiplier):
    global nextMove
    if depthA == 0:
        return turnMultiplier * scoreBoard(gameState)

    maxScore = -checkmate
    for i in validMoves:
        gameState.makeMove(i)
        nextMoves = gameState.getValidMoves()
        score = -findMoveNegaMax(gameState, nextMoves, depthA - 1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depthA == depth:
                nextMove = i
        gameState.undoMove()
    return maxScore

def findMoveNegaMaxAB(gameState, validMoves, depthA, alpha, beta, turnMultiplier):
    global nextMove
    if depthA == 0:
        return turnMultiplier * scoreBoard(gameState)

    maxScore = -checkmate
    random.shuffle(validMoves)
    for i in validMoves:
        gameState.makeMove(i)
        nextMoves = gameState.getValidMoves()
        score = -findMoveNegaMaxAB(gameState, nextMoves, depthA - 1,-beta, -alpha,-turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depthA == depth:
                nextMove = i
        gameState.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore

def scoreBoard(gameState):
    if gameState.checkmate:
        if gameState.whiteToMove:
            return -checkmate
        else:
            return checkmate
    elif gameState.stalemate:
        return stalemate

    score = 0
    for rank in gameState.board:
        for square in rank:
            if square[0] == "w":
                if square[1] == "K" and gameState.inCheck:
                    score += 100
                else:
                    score += pieceScore[square[1]]
            elif square[0] == "b":
                if square[1] == "K" and gameState.inCheck:
                    score -= 100
                else:
                    score -= pieceScore[square[1]]

    return score

def scoreMaterial(board):
    score = 0
    for rank in board:
        for square in rank:
            if square[0] == "w":
                score += pieceScore[square[1]]
            elif square[0] == "b":
                score -= pieceScore[square[1]]

    return score