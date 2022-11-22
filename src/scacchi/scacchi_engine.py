'''
Serve per memorizare le informazioni sullo stato della partita
sarà responsabile nel gestire le attuali mosse legali e terra un log 
delle mosse
'''

class Gamest():
    def __init__(self):
        #la scacchiera viene rappresentata come un array a due dimensioni
        #ogni elemento della scacchira ha due caratteri il primo 
        #rappresenta il colore del pezzo mentre il secondo il tipo
        #la stringa -- rappresenta lo spazio vuoto
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]]
        self.whiteToMove = True
        self.moveLog = []