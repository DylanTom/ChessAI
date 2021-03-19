#Store Information about the current state and determining valid moves

class GameState():
    def __init__(self):
        #After completion of project, try to reimplement this using numpy - better for efficiency, better for AI
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
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
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.checkmate = False
        self.stalemate = False
        self.enpassantAvailable = ()
        self.currentCastlingRights = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks,
                                             self.currentCastlingRights.wqs, self.currentCastlingRights.bqs)]

    def makeMove(self, move):
        self.board[move.startRank][move.startFile] = "--"
        self.board[move.endRank][move.endFile] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRank, move. endFile)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRank, move.endFile)

        if move.pawnPromoted:
            #promotedPiece = input("Promote to Q, R, B, or N")
            self.board[move.endRank][move.endFile] = move.pieceMoved[0] + 'Q' #promotedPiece

        if move.enPassant:
            self.board[move.startRank][move.endFile] = '--'

        if move.pieceMoved[1] == "P" and abs(move.startRank - move.endRank) == 2:
            self.enpassantAvailable = ((move.startRank + move.endRank) // 2, move.endFile)
        else:
            self.enpassantAvailable = ()

        if move.isCastleMove:
            if move.endFile - move.startFile == 2:
                self.board[move.endRank][move.endFile - 1] = self.board[move.endRank][move.endFile + 1]
                self.board[move.endRank][move.endFile + 1] = "--"
            else:
                self.board[move.endRank][move.endFile+1] = self.board[move.endRank][move.endFile -2]
                self.board[move.endRank][move.endFile -2] = "--"

        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks,
                                                self.currentCastlingRights.wqs, self.currentCastlingRights.bqs))

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRank][move.startFile] = move.pieceMoved
            self.board[move.endRank][move.endFile] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.startRank, move.startFile)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.startRank, move.startFile)

        if move.enPassant:
            self.board[move.endRank][move.endFile] = "--"
            self.board[move.startRank][move.endFile] = move.pieceCaptured
            self.enpassantAvailable = (move.endRank, move.endFile)

        if move.pieceMoved[1] == 'P' and abs(move.startRank - move.endRank) == 2:
            self.enpassantAvailable = ()

        if move.isCastleMove:
            if move.endFile - move.startFile == 2:
                self.board[move.endRank][move.endFile+1] = self.board[move.endRank][move.endFile -1]
                self.board[move.endRank][move.endFile-1]="--"
            else:
                self.board[move.endRank][move.endFile -2] = self.board[move.endRank][move.endFile +1]
                self.board[move.endRank][move.endFile+1] ="--"

        self.castleRightsLog.pop()
        self.currentCastlingRights = self.castleRightsLog[-1]

        self.checkmate = False
        self.stalemate = False

    def updateCastleRights(self, move):
        if move.pieceMoved == 'wk':
            self.currentCastlingRights.wks = False
            self.currentCastlingRights.wqs = False
        elif move.pieceMoved == 'bk':
            self.currentCastlingRights.bks = False
            self.currentCastlingRights.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRank == 7:
                if move.startFile == 0:
                    self.currentCastlingRights.wqs = False
                elif move.startFile == 7:
                    self.currentCastlingRights.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRank == 0:
                if move.startFile == 0:
                    self.currentCastlingRights.bqs = False
                elif move.startFile == 7:
                    self.currentCastlingRights.bks = False

    def getValidMoves(self):
        tempEnPassant = self.enpassantAvailable
        tempCastle = CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks,
                                  self.currentCastlingRights.wqs, self.currentCastlingRights.bqs)

        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRank = self.whiteKingLocation[0]
            kingFile = self.whiteKingLocation[1]
        else:
            kingRank = self.blackKingLocation[0]
            kingFile = self.blackKingLocation[1]
        if self.inCheck:
            if len(self.checks) == 1:
                moves = self.getAllPossibleMoves()
                check = self.checks[0]
                checkRank = check[0]
                checkFile = check[1]
                pieceChecking = self.board[checkRank][checkFile]
                validSquares = []
                if pieceChecking[1] == "N":
                    validSquares = [(checkRank, checkFile)]
                else:
                    for i in range(1,8):
                        validSquare = (kingRank + check[2] *i , kingFile + check[3]*i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRank and validSquare[1] == checkFile:
                            break
                for i in range(len(moves)-1,-1,-1):
                    if moves[i].pieceMoved[1] != "K":
                        if not (moves[i].endRank, moves[i].endFile) in validSquares:
                            moves.remove(moves[i])
            else:
                self.getKingMoves(kingRank, kingFile, moves)
        else:
            moves = self.getAllPossibleMoves()
        #checkmate and stalemate
        if len(moves) == 0:
            if self.inCheck:
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False

        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)

        self.enpassantAvailable = tempEnPassant
        self.currentCastlingRights = tempCastle

        return moves


    def getAllPossibleMoves(self):
        moves = []
        for rank in range(len(self.board)):
            for file in range(len(self.board[rank])):
                currentColor = self.board[rank][file][0]
                if (currentColor == 'w' and self.whiteToMove) or (currentColor == 'b' and not self.whiteToMove):
                    piece = self.board[rank][file][1]
                    self.moveFunctions[piece](rank, file, moves)
        return moves

    def getPawnMoves(self, rank, file, moves):
        piecePinned = False
        pinDirection =()
        for i in range(len(self.pins)-1, -1,-1):
            if self.pins[i][0] == rank and self.pins[i][1] == file:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove:
            moveAmount = -1
            startRank = 6
            backRank = 0
            enemy = 'b'
        else:
            moveAmount = 1
            startRank = 1
            backRank = 7
            enemy = 'w'
        pawnPromoted = False

        if self.board[rank+moveAmount][file] == "--":
            if not piecePinned or pinDirection == (moveAmount,0):
                if rank + moveAmount == backRank:
                    pawnPromoted = True
                moves.append(Move((rank, file), (rank +moveAmount, file), self.board, pawnPromoted=pawnPromoted))
                if rank == startRank and self.board[rank + 2 * moveAmount][file] == "--":
                    moves.append(Move((rank, file), (rank + 2 * moveAmount, file), self.board))
        if file-1 >= 0:
            if not piecePinned or pinDirection == (moveAmount, -1):
                if self.board[rank + moveAmount][file - 1][0] == enemy:
                    if rank + moveAmount == backRank:
                        pawnPromoted = True
                    moves.append(Move((rank, file), (rank + moveAmount, file-1), self.board, pawnPromoted = pawnPromoted))
                if (rank + moveAmount, file -1) == self.enpassantAvailable:
                    moves.append(Move((rank, file), (rank + moveAmount, file - 1), self.board, enPassant=True))
        if file + 1 <= len(self.board[rank]) - 1:
            if not piecePinned or pinDirection == (moveAmount, 1):
                if self.board[rank + moveAmount][file + 1][0] == enemy:
                    if rank + moveAmount == backRank:
                        pawnPromoted = True
                    moves.append(Move((rank, file), (rank + moveAmount, file + 1), self.board, pawnPromoted=pawnPromoted))
                if (rank + moveAmount, file + 1) == self.enpassantAvailable:
                    moves.append(Move((rank, file), (rank + moveAmount, file +1), self.board, enPassant=True))

    def getBishopMoves(self, rank, file, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == rank and self.pins[i][1] == file:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        bishopMoves = ((-1,1), (-1,-1), (1,1),(1,-1))
        enemy = "b" if self.whiteToMove else "w"
        for i in bishopMoves:
            for d in range(1, 8):
                endRank = rank + i[0] * d
                endFile = file + i[1] * d
                if 0 <= endRank < len(self.board) and 0 <= endFile < len(self.board):
                    if not piecePinned or pinDirection == i or pinDirection == (-i[0], -i[1]):
                        endPiece = self.board[endRank][endFile]
                        if endPiece == "--":
                            moves.append(Move((rank, file), (endRank, endFile), self.board))
                        elif endPiece[0] == enemy:
                            moves.append(Move((rank, file), (endRank, endFile), self.board))
                            break
                        else:
                            break
                else:
                    break

    def getRookMoves(self, rank, file, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == rank and self.pins[i][1] == file:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[rank][file][1] != "Q":
                    self.pins.remove(self.pins[i])
                break

        rookMoves = ((-1, 0), (1, 0), (0, -1), (0,1))
        enemy = "b" if self.whiteToMove else "w"
        for i in rookMoves:
            for d in range(1, 8):
                endRank = rank + i[0] * d
                endFile = file + i[1] * d
                if 0 <= endRank < len(self.board) and 0 <= endFile < len(self.board):
                    if not piecePinned or pinDirection == i or pinDirection == (-i[0], -i[1]):
                        endPiece = self.board[endRank][endFile]
                        if endPiece == "--":
                            moves.append(Move((rank, file), (endRank, endFile), self.board))
                        elif endPiece[0] == enemy:
                            moves.append(Move((rank, file), (endRank, endFile), self.board))
                            break
                        else:
                            break
                else:
                    break

    def getKnightMoves(self, rank, file, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == rank and self.pins[i][1] == file:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break

        knightMoves = ((-2,1), (-2,-1), (-1,-2), (-1,2), (1,2), (1,-2),(2,-1),(2,1))
        enemy = "b" if self.whiteToMove else "w"
        for i in knightMoves:
            endRank = rank + i[0]
            endFile = file + i[1]
            if 0 <= endRank < len(self.board) and 0 <= endFile < len(self.board):
                if not piecePinned:
                    endPiece = self.board[endRank][endFile]
                    if endPiece[0] == enemy or endPiece == "--":
                        moves.append(Move((rank, file), (endRank, endFile), self.board))

    def getQueenMoves(self, rank, file, moves):
        self.getRookMoves(rank, file, moves)
        self.getBishopMoves(rank, file, moves)

    def getKingMoves(self, rank, file, moves):
        kingMoves = ((-1,1), (-1,-1), (1,1),(1,-1), (1,0), (0,1), (-1,0),(0,-1))
        if self.whiteToMove:
            ally = "w"
            enemy = "b"
        else:
            ally = "b"
            enemy = "w"

        for i in kingMoves:
            endRank = rank + i[0]
            endFile = file + i[1]
            if 0<= endRank < len(self.board) and 0<= endFile < len(self.board):
                endPiece = self.board[endRank][endFile]
                if endPiece[0] == enemy or endPiece == "--":
                    if ally == "w":
                        self.whiteKingLocation = (endRank, endFile)
                    else:
                        self.blackKingLocation = (endRank, endFile)
                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((rank, file), (endRank, endFile), self.board))

                    if ally == "w":
                        self.whiteKingLocation= (rank, file)
                    else:
                        self.blackKingLocation = (rank, file)

    def getCastleMoves(self, rank, file, moves):
        if self.squareUnderAttack(rank, file):
            return
        if (self.whiteToMove and self.currentCastlingRights.wks) or (not self.whiteToMove and self.currentCastlingRights.bks):
            self.getKingSideCastleMoves(rank, file, moves)
        if (self.whiteToMove and self.currentCastlingRights.wqs) or (not self.whiteToMove and self.currentCastlingRights.bqs):
            self.getQueenSideCastleMoves(rank, file, moves)

    def getKingSideCastleMoves(self, rank, file, moves):
        if 0<= file +2 < len(self.board):
            if self.board[rank][file+1] == "--" and self.board[rank][file+2]=='--':
                if not self.squareUnderAttack(rank, file+1) and not self.squareUnderAttack(rank, file +2):
                    moves.append(Move((rank, file), (rank, file +2), self.board, isCastleMove = True))

    def getQueenSideCastleMoves(self, rank, file, moves):
        if self.board[rank][file-1] == "--" and self.board[rank][file-2]=='--' and self.board[rank][file-3] == '--':
            if not self.squareUnderAttack(rank, file-1) and not self.squareUnderAttack(rank, file -2):
                moves.append(Move((rank, file), (rank, file -2), self.board, isCastleMove = True))

    def squareUnderAttack(self, rank, file):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRank == rank and move.endFile == file:
                return True
        return False

    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteToMove:
            enemy = "b"
            ally = "w"
            startRank = self.whiteKingLocation[0]
            startFile = self.whiteKingLocation[1]
        else:
            enemy = "w"
            ally = "b"
            startRank = self.blackKingLocation[0]
            startFile = self.blackKingLocation[1]
        directions = ((-1,0), (0,-1), (1,0),(0,1), (-1,-1), (-1,1), (1,-1),(1,1))
        for i in range(len(directions)):
            d = directions[i]
            possiblePin = ()
            for j in range(1,8):
                endRank = startRank + d[0] * j
                endFile = startFile + d[1] * j
                if 0 <= endRank < len(self.board) and 0 <= endFile < len(self.board):
                    endPiece = self.board[endRank][endFile]
                    if endPiece[0] == ally and endPiece[1] != "K":
                        if possiblePin == ():
                            possiblePin = (endRank, endFile, d[0], d[1])
                        else:
                            break
                    elif endPiece[0] == enemy:
                        type = endPiece[1]
                        #orthogonal direction and piece is rook
                        #diagonal direction and piece is bishop
                        #1 square away pawn
                        #any direction queen
                        #cannot enter squares controlled by other king
                        if (0 <= i <= 3 and type == "R") or \
                                (4<= i <=7 and type == "B") or \
                                (j == 1 and type == "P" and ((enemy == 'w' and 6 <= i <= 7) or (enemy == 'b' and 4 <= i <= 5))) or \
                                (type == 'Q') or (j == 1 and type == 'K'):
                            if possiblePin == ():
                                inCheck = True
                                checks.append((endRank, endFile, d[0], d[1]))
                                break
                            else:
                                pins.append(possiblePin)
                                break
                        else:
                            break
                else:
                    break
        knightMoves = ((-2,1), (-2,-1), (-1,-2), (-1,2), (1,2), (1,-2),(2,-1),(2,1))
        for m in knightMoves:
            endRank = startRank + m[0]
            endFile = startFile + m[1]
            if 0<= endRank < len(self.board) and 0 <= endFile < len(self.board):
                endPiece = self.board[endRank][endFile]
                if endPiece[0] == enemy and endPiece[1]== "N":
                    inCheck = True
                    checks.append((endRank, endFile, m[0], m[1]))
        return inCheck, pins, checks

class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7":  1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"h": 7, "g": 6, "f": 5, "e": 4, "d": 3, "c": 2, "b": 1, "a": 0}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSquare, endSquare, board, enPassant = False, pawnPromoted = False, isCastleMove = False):
        self.startRank = startSquare[0]
        self.startFile = startSquare[1]
        self.endRank = endSquare[0]
        self.endFile = endSquare[1]
        self.pieceMoved = board[self.startRank][self.startFile]
        self.pieceCaptured = board[self.endRank][self.endFile]
        #self.promotionChoice = 'Q' #have to add a parameter
        self.pawnPromoted = pawnPromoted
        self.enPassant = enPassant
        if self.enPassant:
            self.pieceCaptured = 'wP' if self.pieceMoved == 'bP' else "bP"
        self.isCastleMove = isCastleMove

        self.moveID = self.startRank * 1000 + self.startFile * 100 + self.endRank * 10 + self.endFile #maybe try using binary (0-64) start to end

    def __eq__(self,other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRank, self.startFile) + self.getRankFile(self.endRank, self.endFile)

    def getRankFile(self, rank, file):
        return self.colsToFiles[file] + self.rowsToRanks[rank]