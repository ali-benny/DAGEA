import {playerTurn} from '../../playerTurn.service.js'
import {piecesDetermmine} from '../../piecesDetermine.service.js'
import {checkMate} from '../../checkMate.service.js'

export default {
    handlePieceMouseenter({pieceBoxElement, pieceBoxPosition, pieceElement, pieceType}) {
        if(checkMate.gameOver) {
            return
        }

        if(this.isPieceSelected() && this.isNotOnPieceSelected(pieceBoxPosition)) {
            const hasPiecePotential = piecesDetermmine.hasPiecePotential(this.pieceSelectedPosition, pieceBoxPosition)

            if(hasPiecePotential) {
                this.setPointer(pieceBoxElement)
            }
            return
        }

        if(this.isPieceSelected()) {
            return
        }

        if(!pieceElement) {
            return
        }

        if(playerTurn.isRightTurn(pieceType)) {
            this.setSelected(pieceBoxElement)
        }
    }
}