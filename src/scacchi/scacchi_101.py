'''
Questo file si occuperà di controllare lo stato della partita
e di disegnare ogni volta la scacchiera con tutti i pezzi necesssari
'''
import pygame as p
import chess
import sys
import app
from . import scacchi_engine


WIDTH = HEIGHT = 512 #volendo si può scegliere 400 come dimensione
DIMENSION = 8 #dimesione della scacchiera
SQ_SIZE = WIDTH // DIMENSION #grandezza di un singolo quadrato
MAX_FPS = 15 #serve se si vogliono aggingere animazioni nel gioco
IMAGES = {}

p.display.set_caption('Scacchi')

def loadImages():
    pieces = ['bR','bN','bB','bQ','bK','bp','wp','wQ','wK','wB','wN','wR']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("scacchi/immagini/"+ piece +".png"),(SQ_SIZE,SQ_SIZE))
        #N.B. in caso se volessimo chiamare uno specifico pezzo ci basterebbe fare IMAGES['nome pezzo']

def __main__():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = scacchi_engine.Gamest()
    loadImages() #viene fatto solo una volta prima del ciclo
    run = True
    print('BEFORE while')
    while run:
        print('------------------------------------------------')
        for event in p.event.get():
            if event.type == p.QUIT:
                print('EXIT')
                run = False
        drawGamest(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()
        print('END LOOP')
    p.quit()
    sys.exit()
    print('AFTER while')
    return True

def drawGamest(screen, gs):
    drawBoard(screen) #disegnerà i quadrati della scacchiera
    drawPieces(screen, gs.board) #disegnerà i pezzi sopra la scacchiera
    
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": #non è vuoto
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

    
if __name__ == "__main__":
    __main__()
