import handlePieceClick from './handlePieceEvent/handlePieceClick.js'
import handlePieceMouseenter from './handlePieceEvent/handlePieceMouseenter.js'
import handlePieceMouseleave from './handlePieceEvent/handlePieceMouseleave.js'

export default {
    ...handlePieceClick,
    ...handlePieceMouseenter,
    ...handlePieceMouseleave,
}