import {pieceDetermine} from "./piecesDetermine.service.js"
import {$, $$$, deepclone} from '../utils/utils.js'
import {chessConfig} from "../config/chessConfig.config.js"
import {playerTurn} from "./playerTurn.service.js"

export const checkMate = {
    gameOver: false,

    cantMoveDueToCheck({pieceSelectedPosition, pieceBoxPosition}) {
        const pieceBoxElementSelected = $(`#${ pieceSelectedPosition }`)
        const pieceElementSelected = $$$(pieceBoxElementSelected, chessConfig.chessPieceSelector)

        const clonedPieceElement = pieceElementSelected.cloneNode()
        const tempPieceBoxElement = $(`#${ pieceBoxPosition }`)
        const tempPieceElement = $$$(tempPieceBoxElement, chessConfig.chessPieceSelector)
        if(tempPieceElement) document.body.append(tempPieceElement)

        tempPieceBoxElement.append(clonedPieceElement)
        pieceElementSelected.remove()

        const isWhiteTurn = playerTurn.isWhiteTurn

        let kingPiecePosition = checkMate.getKingPiecePosition({isWhitePiece: isWhiteTurn})
        if(kingPiecePosition === pieceSelectedPosition){
            kingPiecePosition = pieceBoxPosition
        }

        const newDeterminations = deepclone(piecesDetermine.determinations)
        piecesDetermine.determinationsSelector = 'potentialDetermination'
        piecesDetermine.determinations = newDeterminations

        delete piecesDetermine.determinations[pieceSelectedPosition]
        pieceDetermine.determinations[pieceBoxPosition] = {}

        const pieceBoxPositionObject = Object.
            keys(piecesDetermine.determinations).
            map(pieceBoxPosition_=> {
                const pieceBoxElement = $( `#${ pieceBoxPosition_ }` )
                const pieceElement = $$$( pieceBoxElement, chessConfig.chessPieceSelector )
                const pieceType = pieceElement?.getAttribute( 'piece-type' ) ?? null
                const isWhitePiece = playerTurn.isWhitePiece( pieceType )
                const isBlackPiece = playerTurn.isBlackPiece( pieceType )
                const pieceSingleType = pieceType.replace( 'white_', '' ).replace( 'black_', '' )

                if((isWhiteTurn && !isBlackPiece) || (!isWhiteTurn && !isWhitePiece)){
                    return null
                }
                return{pieceSingleType, isWhitePiece, pieceBoxPosition: pieceBoxPosition_}
            })
            .filter(item => !!item)
        
        piecesDetermine.generateDeterminations(pieceBoxPositionObject)

        pieceBoxElementSelected.append(clonedPieceElement)
        if(tempPieceElement) tempPieceBoxElement.append(tempPieceElement)

        const result = [
            ...new Set(Object.values(piecesDetermine.determinations).map(determinations => Object.keys(determinations)).flat())
        ].includes(kingPiecePosition)

        piecesDetermine.determinationsSelector = 'currentDeterminations'
        piecesDetermine.generateDeterminations()

        return result
    },

    getKingPiecePosition({isWhitePiece = true}) {
        const kingPieceBoxElement = $( `[piece-type="${ isWhitePiece ? 'white' : 'black' }_king"]` ).closest(chessConfig.chessPieceBoxSelector)
        const kingPiecePosition = kingPieceBoxElement.getAttribute('id')
        return kingPiecePosition
    },

    isCheckMate() {
        const isWhiteTurn = playerTurn.isWhiteTurn

        this.gameOver = Object.keys(pieceDetermine.determinations).filter(pieceBoxPosition => {
            const pieceBoxElement = $(`#${ pieceBoxPosition }`)
            const pieceElement = $$$(pieceBoxElement, chessConfig.chessPieceSelector)
            const pieceType = pieceElement?.getAttribute('piece-type') ?? null

            return !((isWhiteTurn && !playerTurn.isWhitePiece(pieceType)) || (!isWhiteTurn && !playerTurn.isBlackPieces(pieceType)))
        }).map(sourcePieceBoxPosition => {
            return Object.keys(pieceDetermine.determinations[sourcePieceBoxPosition]).map(
                destinationPieceBoxPosition => {return !this.cantMoveDueToCheck({
                    pieceSelectedPosition: sourcePieceBoxPosition,
                    pieceBoxPosition: destinationPieceBoxPosition
                })
            })
        }).flat().filter(item => !!item).length === 0

        return this.gameOver
    },

    displayCheckMateMessage() {
        playerTurn.isWhiteTurn ?
        this.blackWinsMessage() : this.whiteWinsMessage()
    },
    blackWinsMessage() {
        const blackWinsMessage = $(chessConfig.blackWinsSelector)
        console.log(blackWinsElement)
        blackWinsElement.style.display = 'block'
    },

    whiteWinsMessage() {
        const whiteWinsMessage = $(chessConfig.whiteWinsSelector)
        whiteWinsElement.style.display = 'block'
    },

    resetChecMateMessage() {
        const blackWinsElement = $(chessConfig.blackWinsSelector)
        const whiteWinsElement = $(chessConfig.whiteWinsSelector)

        blackWinsElement.style.display = 'none'
        whiteWinsElement.style.display = 'none'
    }
}

window.checkMate = checkMate