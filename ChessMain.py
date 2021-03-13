#Driver File - handling user input and displaying current gameState

import pygame as g
from ChessAI import ChessEngine

width = height = 512
dimension = 8
squareSize = height // dimension
maxFPS = 15
images = {}

#want to load in images at the beginning, pygame takes a lot of resources to load images each frame
def loadImages():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bP", "wP", "wR", "wN", "wB", "wQ", "wK"]
    for piece in pieces:
        images[piece]= g.transform.scale(g.image.load("Pieces/" + piece + ".png"), (squareSize,squareSize))

def main():
    g.init()
    g.display.set_caption('ChessAI')
    screen = g.display.set_mode((width, height))
    clock = g.time.Clock()
    screen.fill(g.Color("white"))
    gameState = ChessEngine.GameState()
    validMoves = gameState.getValidMoves()
    moveMade = False

    loadImages()
    running = True
    selected = ()
    playerClicks = []

    while running:
        for e in g.event.get():
            if e.type == g.QUIT:
                running = False
            elif e.type == g.MOUSEBUTTONDOWN: #click and drag implementation
                location = g.mouse.get_pos() #keep account for extra UI elements, make sure mouse location is relative to border
                y = location[0] // squareSize
                x = location[1] // squareSize
                if selected == (x, y): #checks to see if user clicks the same square - undo
                    selected = ()
                    playerClicks = []
                else:
                    selected = (x, y)
                    playerClicks.append(selected)
                if len(playerClicks) == 2: #make move after finalizing click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gameState.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gameState.makeMove(move)
                        moveMade = True
                    selected = ()
                    playerClicks = []
            elif e.type == g.KEYDOWN: #need to only allow one undo per move
                if e.key == g.K_z:
                    gameState.undoMove()
                    moveMade = True
        if moveMade:
            validMoves = gameState.getValidMoves()
            moveMade = False

        drawGameState(screen, gameState)
        clock.tick(maxFPS)
        g.display.flip()

def drawGameState(screen, gameState):
    drawBoard(screen)
    drawPieces(screen, gameState.board) #draw pieces on top of board

def drawBoard(screen):
    colors = [g.Color("white"), g.Color("gray")]
    for rank in range(dimension):
        for file in range(dimension):
            color = colors[(rank + file) % 2]
            g.draw.rect(screen, color, g.Rect(file*squareSize, rank*squareSize, squareSize, squareSize))

def drawPieces(screen, board): #uses current gameState.board
    for rank in range(dimension):
        for file in range(dimension):
            piece = board[rank][file]
            if piece != "--":
                screen.blit(images[piece], g.Rect(file*squareSize, rank*squareSize, squareSize, squareSize))

if __name__ == "__main__":
    main()