import matplotlib.pyplot as plt
import pandas as pd

from ..fantacitorio import Fantacitorio

class FantacitorioAnalysis(Fantacitorio.Fantacitorio):
    graphsPath = ""

    @classmethod
    def __init__(cls, path: str, numberOfTurns: int, graphsPath: str = "./") -> None:
        super().__init__(path, numberOfTurns)
        cls.graphsPath = graphsPath

    @classmethod
    def getStandings(cls) -> list:
        # sorted() ritorna la lista cls.simpleReport ordinata in ordine crescente, e la funzione ritorna ritorna tale lista invertita
        sortedSimpleReport = sorted(cls.simpleReport, key=lambda i: i["totalScore"])
        sortedSimpleReport.reverse()
        return sortedSimpleReport

    @classmethod
    # Ritorna, sottoforma di dataFrame, il simpleReport
    def getDataFrame(cls):
        return pd.DataFrame(cls.simpleReport)

    ############################## GRAPHS METHODS ##############################

    @classmethod
    def updateGraphs(cls):
        cls.graph_politicians()
        cls.graph_turns(cls.turns)

    @classmethod
    # Funzione attualmente inutilizzata
    def graph_politician(cls, name: str) -> None:
        fig = plt.figure()
        turns = cls.getPlayedTurns()
        scores = list(cls.getPoliticianScoreReport(name, True).values())
        plt.plot(turns, scores, label=name, marker="o")
        cls._saveGraph(
            fig,
            yLabel="score",
            xLabel="turns",
            fileName="graph_politician_" + name.replace(" ", "-"),
            savePath=".static/img/fantacitorio/"
        )

    @classmethod
    # Data  lista di nomi, mostra un grafico dell'andamento dello score di ogni nome passato alla funzione
    def graph_politicians(cls, plotsPerGraph: int = 5) -> None:
        turns = cls.getPlayedTurns()
        standings = cls.getStandings()
        standingsLen = len(standings)
        numberOfGraphs = standingsLen - (
            standingsLen % plotsPerGraph
        )  # Ogni immagine di un grafico avra' 5 plot di 5 politi diversi
        graphIndex = 0
        while graphIndex < numberOfGraphs + plotsPerGraph:
            fig = plt.figure()
            for place in standings[graphIndex : graphIndex + plotsPerGraph]:
                scores = list(
                    cls.getPoliticianScoreReport(place["name"], True).values()
                )
                plt.plot(turns, scores, label=place["name"], marker="o")
            cls._saveGraph(
                fig,
                yLabel="score",
                xLabel="turns",
                fileName="graph_politicians_" + str(int(graphIndex / plotsPerGraph)),
                savePath="./static/img/fantacitorio/politiciansGroups/"
            )
            plt.clf()
            graphIndex += plotsPerGraph

    @classmethod
    # Data una lista di turni, mostra un grafico con le variazioni di punteggio che vi sono state in ogni turno della lista
    def graph_turns(cls, turns: list) -> None:
        """
        It takes a list of turns, and for each turn, it gets the scores for that turn, and then plots
        the scores on a graph

        :param cls: the class that the method is being called from
        :param turns: list of strings
        """
        dataFrame = cls.getDataFrame()
        fig = plt.figure()
        for turn in turns:
            accumulativeScore = 0
            turnScores = [0]
            for score in list(dataFrame[turn]):
                if score > 0:
                    accumulativeScore += score
                    turnScores.append(accumulativeScore)
            plt.plot(range(0, len(turnScores)), turnScores, label=turn, marker="o")
        cls._saveGraph(
            fig, yLabel="score", xLabel="times", fileName="graph_turns_allTurns", savePath="./static/img/fantacitorio/"
        )

    @classmethod
    def _saveGraph(cls, fig, yLabel, xLabel, fileName: str, savePath: str = None):
        if savePath == None:
            savePath = cls.graphsPath
        plt.ylabel(yLabel)
        plt.xlabel(xLabel)
        plt.legend()
        fig.savefig(savePath + fileName + ".svg")

    ############################## STATS METHODS ##############################

    @classmethod
    # Data una lista di turni, trova il best climber di un turno fra piu' turni e ritorna nome e punteggio vincente
    def getBestClimber(cls, turns: list = None, getBest: bool = True) -> dict:
        """
        It takes the list of turns and for each turn it finds the best climber, then it compares the
        best climber of each turn and returns the best climber of the whole championship

        :param turns: list of the turns of the championship
        :return: A dictionary with the name and the score of the best climber of the championship
        """
        if turns == None:
            turns = Fantacitorio.Fantacitorio.getPlayedTurns()
        bestClimbererName, highScore = "", 0  # Dati del bestPlayer del campionato
        for turn in turns:
            turnBestClimberName, turnHighScore = (
                "",
                0,
            )  # Dati del bestPlayer del turno in analisi
            for politician in cls.simpleReport:
                for keys, data in zip(politician.keys(), politician.values()):
                    if keys == turn:
                        if data > turnHighScore:
                            turnHighScore = data
                            turnBestClimberName = politician["name"]
            if turnHighScore > highScore:
                highScore = turnHighScore
                bestClimbererName = turnBestClimberName
            # print(f"{turnBestClimberName}    {turnHighScore}")      # Uncomment to see the best climber of each turn
        return {"name": bestClimbererName, "score": highScore}

    @classmethod
    # Data una lista di turni, ritorna il {miglior | peggior} single score fatto nei turni passati alla funzione
    def getBWSingleScore(cls, turns: list = None, getBest: bool = True) -> dict:
        """
        It takes a list of turns, and returns the name of the politician with the highest or lowest
        score in the passed turns

        :param turns: list of turns to check
        :param getBest: True if you want to get the best score, False if you want to get the worst
        score, defaults to True
        :return: A dictionary with the name of the politician and the score of the event
        """
        if turns == None:
            turns = Fantacitorio.Fantacitorio.getPlayedTurns()
        winnerName, winnerSingleScore = "", 0
        if getBest == False:
            winnerSingleScore = 10000
        for politician in cls.completeReport.values():
            scoreReport = politician["report"]
            for key, turnReport in zip(scoreReport.keys(), scoreReport.values()):
                if key != "totalScore" and key in turns:
                    for event in turnReport:
                        if getBest:
                            if event["score"] > winnerSingleScore:
                                winnerSingleScore = event["score"]
                                winnerName = politician["name"]
                        else:
                            if event["score"] < winnerSingleScore:
                                winnerSingleScore = event["score"]
                                winnerName = politician["name"]
        # print(f"{winnerName}    {winnerSingleScore}")
        return {"name": winnerName, "score": winnerSingleScore}

    @classmethod
    # Ritorna il {miglior | peggior} politico del fantacitorio (in termini di score)
    def getBWPlayer(cls, getBest: bool = True) -> dict:
        """
        :param getBest: If True, the function will return the player with the highest score. If False,
        it will return the player with the lowest score, defaults to True
        :return: A dictionary of the best or worst player.
        """
        winner = {}
        bestScore = 0
        if getBest == False:
            bestScore = 10000
        for politician in cls.simpleReport:
            if getBest:
                if bestScore < politician["totalScore"]:
                    bestScore = politician["totalScore"]
                    winner = politician
            else:
                if bestScore > politician["totalScore"]:
                    bestScore = politician["totalScore"]
                    winner = politician
        return winner

    @classmethod
    # Ritorna il politico con la piu' alta media di punteggio ottenuta per turno
    def getBWAverage(cls, getBest=True) -> dict:
        """
        It loops through the class's simpleReport attribute, and returns a dictionary with
        the name and score of the politician with the highest average score

        :return: A dictionary with the name of the politician with the highest average score and the
        score itself.
        """
        winnerName, bestAverage = "", 0
        if getBest == False:
            bestAverage = 10000
        for politician in cls.simpleReport:
            average = 0
            for key, data in zip(politician.keys(), politician.values()):
                if key != "name" and key != "totalScore":
                    average += data
            average /= len(politician.keys()) - 2
            if getBest:
                if average > bestAverage:
                    bestAverage = round(average, 2)  # Approssimazione a 2 decimali
                    winnerName = politician["name"]
            else:
                if average < bestAverage:
                    bestAverage = round(average, 2)  # Approssimazione a 2 decimali
                    winnerName = politician["name"]
        # print(f"{winnerName}    {bestAverage}")
        return {"name": winnerName, "score": bestAverage}

    @classmethod
    # Ritorna il turno del Fantacitorio in cui sono stati fatti {piu' | meno} punti
    def getBWTurn(cls, getBest: bool = True) -> dict:
        """
        It returns the turn with the highest score if getBest is True, and the turn with the
        lowest score if getBest is False

        :param getBest: If True, the function will return the turn with the highest score. If
        False, it will return the turn with the lowest score, defaults to True
        :return: A dictionary with the turn with the highest score and the score itself.
        """
        winnerTurn, winnerScore = "", 0
        if getBest == False:
            winnerScore = 10000
        dataFrame = cls.getDataFrame()
        for i in range(1, cls.numberOfTurns):
            turnScore = sum(list(dataFrame["turn" + str(i)]))
            if getBest:
                if turnScore > winnerScore:
                    winnerScore = turnScore
                    winnerTurn = "turn " + str(i)
            else:
                if turnScore < winnerScore:
                    winnerScore = turnScore
                    winnerTurn = "turn " + str(i)
        return {"turn": winnerTurn, "score": winnerScore}

    @classmethod
    def getStats(cls):
        turnsKeys = cls.getPlayedTurns()
        stats = {"allTurns": {}}
        for turn in turnsKeys:
            stats.update({turn: {}})

        for turn in turnsKeys:
            stats[turn].update({"bestClimber": cls.getBestClimber(turns=[turn])})
            stats[turn].update({"bestSingleScore": cls.getBWSingleScore(turns=[turn])})
            stats[turn].update(
                {"worstSingleScore": cls.getBWSingleScore(turns=[turn], getBest=False)}
            )

        stats["allTurns"].update({"bestClimber": cls.getBestClimber()})
        stats["allTurns"].update({"bestAverage": cls.getBWAverage()})
        stats["allTurns"].update({"worstAverage": cls.getBWAverage(getBest=False)})
        stats["allTurns"].update({"bestSingleScore": cls.getBWSingleScore()})
        stats["allTurns"].update(
            {"worstSingleScore": cls.getBWSingleScore(getBest=False)}
        )
        stats["allTurns"].update({"bestPlayer": cls.getBWPlayer()})
        stats["allTurns"].update({"worstPlayer": cls.getBWPlayer(getBest=False)})
        stats["allTurns"].update({"bestTurn": cls.getBWTurn()})
        stats["allTurns"].update({"worstTurn": cls.getBWTurn(getBest=False)})

        return stats


if __name__ == "__main__":
    pass
