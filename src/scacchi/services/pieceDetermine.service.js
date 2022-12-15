import pawn from "./pieceDetermine/pawn.js"
import knight from "./pieceDetermine/knight.js"
import rook from "./pieceDetermine/rook.js"
import bishop from "./pieceDetermine/bishop.js"
import queen from "./pieceDetermine/queen.js"
import king from "./pieceDetermine/king.js"
import knightKingHelpers from "./pieceDetermine/helpers/knightKing.helpers.js"
import {$, $$, $$$} from '../utils/utils.js'
import {chessConfig} from '../config/chessConfig.config.js'
import {playerTurn} from '../services/playerTurn.service.js'

export const pieceDetermine = {
    _determinations: {
        currentDeterminations: {},
        potentialDeterminations: {}
    },

    get determinations() {
        return this._determinations[this.determinationsSelector]
    },

    set determinations(value) {
        this._determinations[this.determinationsSelector] = value
    },

    generateDeterminations(pieceBoxPositionObject = null) {
        this.resetDeterminations()

        for(const {pieceSingleType, isWhitePiece, pieceBoxPosition} of (pieceBoxPositionObject || this.getCurrentPieceBoxPosition())) {
            this.determinations[pieceBoxPosition] = {}
            this[pieceDetermineConfig[pieceSingleType]]?.({isWhitePiece, pieceBoxPosition})
        }
    },

    getCurrentPieceBoxPosition() {
        const currentPieceboxPosition = []

        for(const pieceBoxElement of $$(chessConfig.chessPieceBoxSelector)){
            const pieceElement = $$$(pieceBoxElement, chessConfig.chessPieceSelector)
            if(!pieceElement) continue

            const pieceBoxPosition = pieceBoxElement.getAttribute('id')
            const pieceType = pieceElement?.getAttribute('piece-type') ?? null
            const isWhitePiece = playerTurn.isWhitePiece(pieceType)
            const pieceSingleType = pieceType.replace('white_','').replace('black_','')

            currentPieceboxPosition.push({
                pieceBoxElement,
                pieceElement,
                pieceBoxPosition,
                pieceType,
                isWhitePiece,
                pieceSingleType
            })
        }

        return currentPieceboxPosition
    },
}