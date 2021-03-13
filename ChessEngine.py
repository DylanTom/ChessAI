#Store Information about the current state and determining valid moves

class GameState():
    def __init__(self):
        #After completion of project, try to reimplement this using numpy - better for efficiency, better for AI
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"], #Represent an empty space
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.whiteToMove = True
        self.moveLog = []
    def makeMove(self, move):
        self.board[move.startRank][move.startFile] = "--"
        self.board[move.endRank][move.endFile] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

class Move():
    ranksToRows = {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}
    rowsToRanks = {v:k for k, v in ranksToRows.items()}
    filesToCols = {"h": 7, "g": 6, "f": 5, "e": 4, "d": 3, "c": 2, "b": 1, "a": 0}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSquare, endSquare, board):
        self.startRank = startSquare[0]
        self.startFile = startSquare[1]
        self.endRank = endSquare[0]
        self.endFile = endSquare[1]
        self.pieceMoved = board[self.startRank][self.startFile]
        self.pieceCaptured = board[self.endRank][self.endFile]

    def getChessNotation(self):
        return self.getRankFile(self.startRank, self.startFile) + self.getRankFile(self.endRank, self.endFile)

    def getRankFile(self, rank, file):
        return self.colsToFiles[file] + self.rowsToRanks[rank]