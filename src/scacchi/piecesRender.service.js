import {piecesImages} from '../config/piecesImages.config.js'
import {initialGame} from '../config/initialGame.config.js'
import {potentialGame} from '../config/potentialGame.config.js'
import {chessConfig} from '../config/chessConfig.config.js'
import {piecesHandle} from '../services/piecesHandle.service.js'
import {piecesDetermine} from '../services/piecesDetermine.service.js'
import {$, $$, $$$} from '../utils/utils.js'

export const piecesRender = {
    piecesEventListeners: {},

    renderPieces() {
        const gameSetup = chessConfig.useInitialGame ? initialGame : potentialGame

        this.placePieceBoxNumbers()
        this.placeWhiteDownOrUp()
        this.placePiecesInPosition(gameSetup)
        this.addPiecesBoxListeners()
        this.piecesDetermine()
    },

    placePieceBoxNumbers() {
        $$(chessConfig.chessPieceBoxSelector).map(pieceBoxElement => {
            const spanElement = document.createElement('span')
            spanElement.classList.add('piece-box-text')
            spanElement.innerHTML = pieceBoxElement.getAttribute('id')

            pieceBoxElement.append(spanElement)
        })
    },

    
}