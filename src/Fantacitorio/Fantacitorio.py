from . import Sheet


class Fantacitorio(Sheet.Sheet):
    # Fantacitorio parameters
    turns, turnsInTableFormat = (
        {},
        {},
    )  # Dizionario contenente tutti i turni (le giornate) finora giocate
    names = set()  # Set contenente tutti i nomi dei politici presenti nelle giornate
    completeReport = (
        {}
    )  # Dizionario coi nomi dei politici come chiavi e i loro report come dati
    simpleReport = []

    @classmethod
    def __init__(cls, path: str, numberOfTurns: int):
        super().__init__(path, numberOfTurns)
        cls.turns = super().getTurnsFromSheet(tableFormat=False)
        cls.turnsInTableFormat = super().getTurnsFromSheet(tableFormat=True)
        cls.names = cls.getTurnsNames()
        cls.completeReport = cls.getCompleteReport()  # TODO: E' mica superfluo?
        cls.simpleReport = cls.getSimpleReport()

    @classmethod
    # Ritorna tutti i nomi (dei politici) presenti in un turno del Fantacitorio
    def getTurnNames(cls, turn: list) -> set:
        names = set()
        for event in turn:
            names.add(event["name"])
        return names

    @classmethod
    # Ritorna tutti i nomi (dei politici) presenti nei turni del Fantacitorio
    def getTurnsNames(cls) -> set:
        for turn in cls.turns.values():
            cls.names = cls.names.union(cls.getTurnNames(turn))
        return cls.names

    @classmethod
    # Ritorna tutte le attivita' di un politico (report) durante un turno (score e motivazioni)
    def getPoliticianTurnReport(cls, name: str, turn: list) -> list:
        """
        Return example:
             [{'score': int, 'motivation': str}, ... ]
        """
        report = []
        for event in turn:
            if name == event.get("name"):
                report.append(
                    {"score": event.get("score"), "motivation": event.get("motivation")}
                )
        return report

    @classmethod
    # Ritorna tutte le attivita' di un politico durante tutto il Fantacitorio
    def getPoliticianTurnsReport(cls, name: str) -> dict:
        """
        Return example:
            {
                'totalScore': int,
                'turn1': [{'score': int, 'motivation': str}, ...],
                ...,
                'turnX': [{'score': int, 'motivation': str}, ...],
            }
        """
        politicianReport = {"totalScore": 0}
        for i in range(1, cls.numberOfTurns):
            politicianReport.update({"turn" + str(i): []})
        for turn, i in zip(cls.turns.values(), range(1, cls.numberOfTurns)):
            totalScore = 0
            turnReport = cls.getPoliticianTurnReport(name, turn)
            politicianReport["turn" + str(i)] = turnReport
            for event in turnReport:
                totalScore += event["score"]
            politicianReport["totalScore"] += totalScore
        return politicianReport

    @classmethod
    # Ritorna tutte le attivita' di tutti i politici (compendio di report) di tutto il Fantacitorio
    def getCompleteReport(cls) -> dict:
        """
        Return example:
            {
                politicianName: {
                    'name' : str,
                    'report' : {
                        'totalScore' : int,
                        'turn1' : [ {'score' : int, 'motivation' : str},  ... ],
                        ...,
                        'turnX' : [ {'score' : int, 'motivation' : str},  ... ],
                    }
                }
            }
        """
        for name in cls.names:
            cls.completeReport.update(
                {name: {"name": name, "report": cls.getPoliticianTurnsReport(name)}}
            )
        return cls.completeReport

    @classmethod
    # Ritorna tutte le attivita' di tutti i politici (compendio di report) di tutto il Fantacitorio in forma "piu' semplice",
    # la quale si presta meglio ad una conversione in dataFrame
    def getSimpleReport(cls) -> list:
        """
        Return example:
        [
            {'name': str, 'totalScore': int, 'turn1': int, ..., 'turnX': int},
            ...
        ]
        """
        simpleReport = []
        for politician in cls.completeReport.values():
            name = politician["name"]
            totalScore = politician["report"]["totalScore"]
            turnsScore = cls.getPoliticianScoreReport(name, False)
            data = {"name": name, "totalScore": totalScore}
            for i in range(1, cls.numberOfTurns):
                field = "turn" + str(i)
                data.update({field: turnsScore[field]})
            simpleReport.append(data)
        return simpleReport

    ##############################  ##############################

    @classmethod
    # Ritorna lo score di un politico accumulato in un turno
    def getPoliticianTurnScore(cls, name: str, turn: list) -> int:
        turnScore = 0
        for event in turn:
            if name == event.get("name"):
                turnScore += event.get("score")
        return turnScore

    @classmethod
    # Ritorna il report dello score di un politico durante tutto il Fantacitorio
    def getPoliticianScoreReport(cls, name: str, accumulative: bool) -> dict:
        """
        It takes a politician's name and a boolean value, and returns a dictionary of the politician's
        score for each turn

        :param name: The name of the politician you want to get the score report for
        :param accumulative: if True, the score of each turn is added to the previous turn's score. If
            False, the score of each turn is the score of that turn only
        :return: A dictionary with the turn number as the key and the score as the value.
        Return example:
            {'turn1': int, ... 'turnX': int }
        """
        turnScore = 0
        scoreReport = {}
        for i in range(1, cls.numberOfTurns):
            scoreReport.update({"turn" + str(i): 0})
        for turn, i in zip(cls.turns.values(), range(1, cls.numberOfTurns)):
            politicianScore = cls.getPoliticianTurnScore(name, turn)
            if accumulative:
                turnScore += politicianScore
            else:
                turnScore = politicianScore
            scoreReport["turn" + str(i)] = turnScore
        return scoreReport


if __name__ == "__main__":
    pass
