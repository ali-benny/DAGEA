import handlePieceEventsMethods from './pieceHandle/handlePieceEvent.methods.js'
import handlePieceStatesMethods from './pieceHandle/handlePieceStates.methods.js'

export const pieceHandle = {
    pieceSelectedPosition: null,

    isPieceSelected() {
        return !!this.pieceSelectedPosition
    },

    changePieceSelected() {
        this.pieceSelectedPosition = pieceSelectedPosition
    },

    resetPieceSelected() {
        this.changePieceSelected = null
    },

    isOnPieceSelected(pieceBoxPosition) {
        return pieceBoxPosition === this.pieceSelectedPosition
    },

    isNotOnPieceSelected(pieceBoxPosition) {
        return !this.isOnPieceSelected(pieceBoxPosition)
    },


    ...handlePieceEventsMethods,
    ...handlePieceStatesMethods,
}