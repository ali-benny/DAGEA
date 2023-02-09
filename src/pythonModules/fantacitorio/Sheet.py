import pandas as pd


class Sheet:
    # Sheet parameters
    sheet_upperRow, sheet_lowerRow = 3, 7  # Range delle righe in
    sheet_columnsLimits = [29, 17, 22, 24, 25, 18, 16, 14, 15]
    sheet_path = ""
    sheet_namesRow = 1
    sheet_motivationsRow = 2
    sheet_scoresRow = 6

    # Other parameters (could be used in subclasses)
    columnsLimits = {}
    numberOfTurns = 0

    @classmethod
    def __init__(cls, path: str, numberOfTurns: int) -> None:
        if path[len(path) - 5 :] != ".xlsx":
            raise Exception(
                "Fantacitorio - Sheet.py - Incorrect input - __init__: Make sure the 'path' parameter ends with '.xlsx'"
            )
        if numberOfTurns < 0:
            raise Exception(
                "Fantacitorio - Sheet.py - Incorrect input - __init__: numberOfTurns can not be a negative number"
            )
        else:
            cls.sheet_path = path
            cls.numberOfTurns = numberOfTurns + 1
            cls.__init__ColumsLimit()

    @classmethod
    def __init__ColumsLimit(cls) -> None:
        # Se sheet_columnsLimits non e' aggiornato con i valori degli ultimi turni, si aggiungono limiti fittizzi
        while len(cls.sheet_columnsLimits) < cls.numberOfTurns:
            cls.sheet_columnsLimits.append(50)

        # Alla fine si avra': cls.columnsLimits = {'turn1': int, ...,'turnX': int }
        turnsIndexes = range(1, cls.numberOfTurns)
        for i, columnLimit in zip(turnsIndexes, cls.sheet_columnsLimits):
            cls.columnsLimits.update({"turn" + str(i): columnLimit})

    @classmethod
    # Ritorna un turno con tutti i suoi eventi in due possibili formati
    def getTurnFromSheet(cls, turn: str, tableFormat: bool = False) -> list | dict:
        """
        if tableFormat == True then return:
            {'names' : [str], 'motivations' : [str], 'scores' : [int]}  # All turn names, all turn motivations, ...
        else return:
            [
                {'name' : name, 'motivation' : motivation, 'score' : score},
                ...
                {'name' : name, 'motivation' : motivation, 'score' : score}
            ]
        """
        # Si estrapola il foglio 'sheetName' dal documento .xlsx
        sheet = pd.read_excel(
            io=cls.sheet_path,
            sheet_name=turn[len(turn) - 1] + "a",
            usecols=range(cls.sheet_upperRow, cls.columnsLimits[turn]),
            nrows=cls.sheet_lowerRow,
        )
        # Dal foglio si estraggono i dati che ci interessano, ovvero nomi, punteggi attribuiti e motivazioni
        names = sheet.iloc[cls.sheet_namesRow].to_list()
        motivations = sheet.iloc[cls.sheet_motivationsRow].to_list()
        scores = sheet.iloc[cls.sheet_scoresRow].to_list()
        if tableFormat:
            return {"names": names, "motivations": motivations, "scores": scores}
        else:
            # I dati estratti vengono salvati in dizionari dedicati. Verra' ritornata una lista di tali dizionari
            turn = []
            for name, motivation, score in zip(names, motivations, scores):
                turn.append({"name": name, "motivation": motivation, "score": score})
            return turn

    @classmethod
    # Ritorna i turni con tutti i loro eventi in due possibili formati
    def getTurnsFromSheet(cls, tableFormat: bool = False) -> list | dict:
        """
        Return examples:
            if tableFormat == False then return:
                {
                    'turn1' : [ {'score' : int, 'motivation' : str}, {'score' : int, 'motivation' : str},  ... ], ...,
                    'turnX' : [ {'score' : int, 'motivation' : str}, {'score' : int, 'motivation' : str}, ... ],
                }
            else return:
                {
                    'turn1' : [ {'names' : [str], 'motivations' : [str], 'scores' : [int]}},  ... ], ...,
                    'turnX' : [ {'names' : [str], 'motivations' : [str], 'scores' : [int]}},  ... ],
                }
        """
        turns = {}
        for i in range(1, cls.numberOfTurns):
            turns.update(
                {
                    "turn"
                    + str(i): cls.getTurnFromSheet(
                        "turn" + str(i), tableFormat=tableFormat
                    )
                }
            )
        return turns

    @classmethod
    # Ritorna una lista coi turni disputati finore
    def getPlayedTurns(cls) -> list:
        return list(cls.columnsLimits.keys())


if __name__ == "__main__":
    pass
