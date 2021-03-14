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

        self.moveFunctions = {'P':self.getPawnMoves, 'R':self.getRookMoves, 'Q':self.getQueenMoves,
                              'K': self.getKingMoves, 'N': self.getKnightMoves, 'B':self.getBishopMoves}

        self.whiteToMove = True
        self.moveLog = []
    def makeMove(self, move): #doesn't account for castling
        self.board[move.startRank][move.startFile] = "--"
        self.board[move.endRank][move.endFile] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRank][move.startFile] = move.pieceMoved
            self.board[move.endRank][move.endFile] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    def getValidMoves(self):
        return self.getAllPossibleMoves()

    def getAllPossibleMoves(self):
        moves = []
        for rank in range(len(self.board)):
            for file in range(len(self.board[rank])):
                currentColor = self.board[rank][file][0]
                if (currentColor == 'w' and self.whiteToMove) or (currentColor == 'b' and not self.whiteToMove):
                    piece = self.board[rank][file][1]
                    self.moveFunctions[piece](rank, file, moves)
        return moves

    def getPawnMoves(self, rank, file, moves): #need to do pawn promotion, en passant
        if self.whiteToMove:
            if self.board[rank-1][file] == "--":
                moves.append(Move((rank, file), (rank - 1, file), self.board))
                if rank == 6 and self.board[rank - 2][file] == "--":
                    moves.append(Move((rank, file), (rank - 2, file), self.board))
            if file-1 >= 0:
                if self.board[rank-1][file-1][0] == "b":
                    moves.append(Move((rank, file), (rank - 1, file-1), self.board))
            if file + 1 <= len(self.board[rank]) - 1:
                if self.board[rank - 1][file + 1][0] == "b":
                    moves.append(Move((rank, file), (rank - 1, file + 1), self.board))
        else:
            if self.board[rank+1][file] == "--":
                moves.append(Move((rank, file), (rank + 1, file), self.board))
                if rank == 1 and self.board[rank + 2][file] == "--":
                    moves.append(Move((rank, file), (rank + 2, file), self.board))
            if file - 1 >= 0:
                if self.board[rank+1][file-1][0] == "w":
                    moves.append(Move((rank, file), (rank + 1, file-1), self.board))
            if file + 1 <= len(self.board[rank]) - 1:
                if self.board[rank + 1][file + 1][0] == "w":
                    moves.append(Move((rank, file), (rank + 1, file + 1), self.board))

    def getBishopMoves(self, rank, file, moves):
        bishopMoves = ((-1,1), (-1,-1), (1,1),(1,-1))
        enemy = "b" if self.whiteToMove else "w"
        for i in bishopMoves:
            for d in range(1, 8):
                endRank = rank + i[0] * d
                endFile = file + i[1] * d
                if 0 <= endRank < len(self.board) and 0 <= endFile < len(self.board):
                    endPiece = self.board[endRank][endFile]
                    if endPiece[0] == enemy or endPiece == "--":
                        moves.append(Move((rank, file), (endRank, endFile), self.board))
                    else:
                        break
                else:
                    break

    def getRookMoves(self, rank, file, moves):
        same = ""
        opposite = ""
        if self.whiteToMove:
            same = "w"
            opposite = "b"
        else:
            same = "b"
            opposite = "w"
        #right
        if file + 1 <= len(self.board[rank])-1:
            for i in range(len(self.board[rank])- 1-file):
                if self.board[rank][file+i+1][0] == same:
                    break
                elif self.board[rank][file+i+1] == "--" or self.board[rank][file+i+1][0] == opposite:
                    moves.append(Move((rank, file), (rank, file+i+1), self.board))
        #left
        if file - 1 >= 0:
            for i in range(file):
                if self.board[rank][file-i-1][0] == same:
                    break
                elif self.board[rank][file-i-1] == "--" or self.board[rank][file-i-1][0] == opposite:
                    moves.append(Move((rank, file), (rank, file-i-1), self.board))
        #up
        if rank - 1 >=0:
            for i in range(rank):
                if self.board[rank-i-1][file][0] == same:
                    break
                elif self.board[rank-i-1][file] == "--" or self.board[rank-i-1][file][0] == opposite:
                    moves.append(Move((rank, file), (rank-i-1, file), self.board))
        #down
        if rank+1<= len(self.board[file])-1:
            for i in range(len(self.board[file]) - 1 - rank):
                if self.board[rank+i+1][file][0] == same:
                    break
                elif self.board[rank+i+1][file] == "--" or self.board[rank+i+1][file][0] == opposite:
                    moves.append(Move((rank, file), (rank+i+1, file), self.board))

    def getKnightMoves(self, rank, file, moves):
        knightMoves = ((-2,1), (-2,-1), (-1,-2), (-1,2), (1,2), (1,-2),(2,-1),(2,1))
        enemy = "b" if self.whiteToMove else "w"
        for i in knightMoves:
            endRank = rank + i[0]
            endFile = file + i[1]
            if 0 <= endRank < len(self.board) and 0 <= endFile < len(self.board):
                endPiece = self.board[endRank][endFile]
                if endPiece[0] == enemy or endPiece == "--":
                    moves.append(Move((rank, file), (endRank, endFile), self.board))

    def getQueenMoves(self, rank, file, moves):
        self.getRookMoves(rank, file, moves)
        self.getBishopMoves(rank, file, moves)

    def getKingMoves(self, rank, file, moves):
        kingMoves = ((-1,1), (-1,-1), (1,1),(1,-1), (1,0), (0,1), (-1,0),(0,-1))
        enemy = "b" if self.whiteToMove else "w"
        for i in kingMoves:
            endRank = rank + i[0]
            endFile = file + i[1]
            if 0<= endRank < len(self.board) and 0<= endFile < len(self.board):
                endPiece = self.board[endRank][endFile]
                if endPiece[0] == enemy or endPiece == "--":
                    moves.append(Move((rank, file), (endRank, endFile), self.board))

class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7":  1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"h": 7, "g": 6, "f": 5, "e": 4, "d": 3, "c": 2, "b": 1, "a": 0}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSquare, endSquare, board):
        self.startRank = startSquare[0]
        self.startFile = startSquare[1]
        self.endRank = endSquare[0]
        self.endFile = endSquare[1]
        self.pieceMoved = board[self.startRank][self.startFile]
        self.pieceCaptured = board[self.endRank][self.endFile]
        self.moveID = self.startRank * 1000 + self.startFile * 100 + self.endRank * 10 + self.endFile #maybe try using binary (0-64) start to end

    def __eq__(self,other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRank, self.startFile) + self.getRankFile(self.endRank, self.endFile)

    def getRankFile(self, rank, file):
        return self.colsToFiles[file] + self.rowsToRanks[rank]