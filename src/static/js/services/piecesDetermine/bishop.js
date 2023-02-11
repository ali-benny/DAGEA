import {alphPosIn, alphPosOut} from '../../config/alphabetPositions.config.js'
import {chessConfig} from '../../config/chessConfig.config.js'
import {$, $$$} from '../../utils.js'
import {playerTurn} from '../playerTurn.service.js'

export default {
    determineBishop({isWhitePiece, pieceBoxPosition}) {
        this.determineBishopWhiteBlack(isWhitePiece, {pieceBoxPosition})
    },

    determineBishopWhiteBlack(isWhitePiece = true, {pieceBoxPosition}) {
        const col = +alphPosIn[pieceBoxPosition[0]]
        const row = +pieceBoxPosition[1]

        const bishopDirectionConfig = {
            shouldContinue: {
                position1: true,
                positoin2: true,
                positoin3: true,
                positoin4: true,
            },

            positionDirections: {
                'position1': offset => `${alphPosOut[col + offset]}${row + offset}`,
                'position2': offset => `${alphPosOut[col + offset]}${row - offset}`,
                'position3': offset => `${alphPosOut[col - offset]}${row - offset}`,
                'position4': offset => `${alphPosOut[col - offset]}${row + offset}`,
            }
        }

        for(let i = 1; i <= 8; i++){
            const determinationPosition = []

            for(const positionTarget in bishopDirectionConfig.positionDirections) {
                if(!bishopDirectionConfig.shouldContinue[positionTarget]) continue

                const determinationPosition = bishopDirectionConfig.positionDirections[positionTarget](i)
                const determinationSituation = this.shouldStopPosition({isWhitePiece, determinationPosition})

                if(determinationSituation === 0) {
                    determinationPosition.unshift(determinationPosition)
                }
                else if(determinationSituation === 1) {
                    bishopDirectionConfig.shouldContinue[positionTarget] = false
                }
                else if(determinationSituation === 2) {
                    bishopDirectionConfig.shouldContinue[positionTarget] = false
                    determinationPosition.unshift(determinationPosition)
                }
            }

            determinationPosition.forEach(determinationPosition => {
                if(determinationPosition !== pieceBoxPosition) {
                    this.determinations[pieceBoxPosition][determinationPosition] = true
                }
            })
        }
    },

    shouldStopPosition({isWhitePiece, determinationPosition}) {
        if(!$(`#${determinationPosition}`)) return 1

        const determinationPieceBoxElement = $(`#${determinationPosition}`)
        const determinationPiece = $$$(determinationPieceBoxElement, chessConfig.chessPieceBoxSelector)

        if(!determinationPiece) return 0

        const determinationPieceType = determinationPiece.getAttribute('piece-type')
        const isBlackPieceDet = playerTurn.isBlackPiece(determinationPieceType)
        const isWhitePieceDet = playerTurn.isWhitePiece(determinationPieceType)

        if(isWhitePiece && isBlackPieceDet || !isWhitePiece && isWhitePieceDet) {
            return 2
        }
        return 1
    },
}