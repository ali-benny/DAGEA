import os
import stream
import pythonModules.twitter.utils.folders as folders
import pythonModules.twitter.utils.filtersbar as filtersbar
import pythonModules.map.map as m
import time

try:
    from flask import Flask, render_template, request, session, redirect
    from flask_session import Session
    import chess
    import configparser  # Used for APIv1 initialization
except ModuleNotFoundError:
    os.system("pip install flask")
    os.system("pip install flask_session")
    os.system("pip install chess")
    os.system("pip install configparser")

import game
import chess.svg
from pythonModules.fantacitorio import FantacitorioAnalysis as FA
from pythonModules.fantacitorio import FantacitorioTeams as FT
from pythonModules.twitter.TweetSearch import TweetSearch
from pythonModules.twitter.SentimentalAnalysis import SentimentalAnalysis
import eredita
import time_chart

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

config = configparser.ConfigParser()
config.read(os.path.abspath("../config.ini"))

print(f"Start app.py")
TweetSearch.__init__(BEARER_TOKEN=config["twitter"]["bearer_token"])
SentimentalAnalysis.__init__(
    BEARER_TOKEN=config["twitter"]["bearer_token"],
    path="./static/img/graphs/",
)
FA.FantacitorioAnalysis.__init__(path="./pythonModules/fantacitorio/punti.xlsx", numberOfTurns=9)
#FA.FantacitorioAnalysis.updateGraphs()     # Eseguire questa riga solo se bisogna aggiornare le immagini dei grafici del Fantacitorio
filterDatas = filtersbar.initFilterDatas()

folders.deleteFolderFiles("./static/img/graphs/")


def renderSubmit(request, pageToRender: str):
    global filterDatas
    global data_time_chart
    whatBtn = request.form["btnradio"]
    filterDatas["tweetsLimit"] = request.form["tweetsLimit"]
    filterDatas["query"] = request.form["keyword"]
    filterDatas["currentResearchMethod"] = request.form.get("researchBy")
    filterDatas["dates"]["minDateValue"] = request.form["minDate"]
    filterDatas["dates"]["maxDateValue"] = request.form["maxDate"]
    if whatBtn == "Stream":
        stream.StreamByKeyword(filterDatas["query"], (int)(filterDatas["tweetsLimit"]))
        tweetCards = stream.MyStream.tweets
    elif whatBtn == "Search":
        TweetSearch.setDatas(
            query=filterDatas["query"],
            tweetsLimit=filterDatas["tweetsLimit"],
            start_time=filterDatas["dates"]["minDateValue"],
            end_time=filterDatas["dates"]["maxDateValue"],
        )
        tweetCards = loadResearch(researchMethod=filterDatas["currentResearchMethod"])
        sentimentalAnalysis = {"analysisReport": {}, "analysisDatas": {}}
        sentimentalAnalysis.update(
            {"analysisReport": SentimentalAnalysis.analysisReport}
        )
        sentimentalAnalysis.update({"analysisDatas": SentimentalAnalysis.analysisDatas})
    else:
        raise ValueError("ERROR: Unknown button")
    return render_template(
        pageToRender,
        tweetCards=tweetCards,
        filterDatas=filterDatas,
        sentimentalAnalysis=sentimentalAnalysis,
        time_chart = data_time_chart,
        document = pageToRender
    )

def loadResearch(researchMethod: str):
    global filterDatas
    global data_time_chart
    TweetSearch.researchDecree(researchType=researchMethod)
    SentimentalAnalysis.SentimentalAnalysis(TweetSearch.response)
    tweetCards = TweetSearch.createCard()
    data_time_chart = time_chart.time_chart(TweetSearch.response)
    filterDatas["SAGraphsVisibility"] = "visible"
    if TweetSearch.cardHaveCoordinates(tweetCards):
        filterDatas["mapVisibility"] = "visible"
        m.Map.__init__()
        m.Map.addMarkers(
            tweetCards
        )  # Vengono aggiunti i mark per ogni coordinata trovata
    else:
        filterDatas["mapVisibility"] = "hidden"
    return tweetCards


@app.route("/", methods=("GET", "POST"))
def homepage():
    filterDatas = filtersbar.initFilterDatas()
    if request.method == "POST":
        if "tweetResearchSubmit" in request.form:
            return renderSubmit(request=request, pageToRender="home.html")
    sentimentalAnalysis = {"analysisReport": {}, "analysisDatas": {}}
    sentimentalAnalysis.update(
        {"analysisReport": SentimentalAnalysis.analysisReport}
    )
    sentimentalAnalysis.update({"analysisDatas": SentimentalAnalysis.analysisDatas})
    return render_template(
        "home.html",
        tweetCards=[],
        filterDatas=filterDatas,
        sentimentalAnalysis=sentimentalAnalysis,
        document = 'home.html'
    )


@app.route("/eredita", methods=("GET", "POST"))
def leredita():
    """
    The eredita function is used to display the tweetCards of '#leredita' research.
    """
    global filterDatas
    global data_time_chart
    filterDatas = filtersbar.initFilterDatas()
    filterDatas["query"] = "#leredita"
    filterDatas["currentResearchMethod"] = "researchByKeyword"
    if request.method == "POST":
        return renderSubmit(request=request, pageToRender="eredita.html")
    else:
        TweetSearch.setDatas(
            query=filterDatas["query"], tweetsLimit=filterDatas["tweetsLimit"]
        )
        tweetCards = loadResearch(researchMethod=filterDatas["currentResearchMethod"])
        sentimentalAnalysis = {"analysisReport": {}, "analysisDatas": {}}
        sentimentalAnalysis.update(
            {"analysisReport": SentimentalAnalysis.analysisReport}
        )
        sentimentalAnalysis.update({"analysisDatas": SentimentalAnalysis.analysisDatas})
        parola = eredita.ghigliottina()
        spettatori = eredita.ereditiers(parola['vincente'])
        print('🌈spettatori=', spettatori)
        total = eredita.total()
        return render_template(
            "eredita.html",
            tweetCards=tweetCards,
            filterDatas=filterDatas,
            sentimentalAnalysis=sentimentalAnalysis,
            document = 'eredita.html',
            solution = parola,    # soluzione ultima puntata
            users = spettatori,
            total = total,
            time_chart = data_time_chart,
        )


@app.route("/reazioneacatena", methods=("GET", "POST"))
def reazioneacatena():
    """
    The reazioneacatena function is used to get the tweets from twitter API.
    It returns a list of cards with the tweets and their information.
    """
    global filterDatas
    global data_time_chart
    filterDatas = filtersbar.initFilterDatas()
    filterDatas["query"] = "#reazioneacatena"
    filterDatas["currentResearchMethod"] = "researchByKeyword"
    if request.method == "POST":
        return renderSubmit(request=request, pageToRender="reazioneacatena.html")
    else:
        TweetSearch.setDatas(
            query=filterDatas["query"], tweetsLimit=filterDatas["tweetsLimit"]
        )
        tweetCards = loadResearch(researchMethod=filterDatas["currentResearchMethod"])
        filterDatas["SAGraphsVisibility"] = "visible"
        sentimentalAnalysis = {"analysisReport": {}, "analysisDatas": {}}
        sentimentalAnalysis.update(
            {"analysisReport": SentimentalAnalysis.analysisReport}
        )
        sentimentalAnalysis.update({"analysisDatas": SentimentalAnalysis.analysisDatas})
        return render_template(
            "reazioneacatena.html",
            tweetCards=tweetCards,
            filterDatas=filterDatas,
            sentimentalAnalysis=sentimentalAnalysis,
            time_chart = data_time_chart,
            document = 'reazioneacatena.html'	
        )


@app.route("/fantacitorio", methods=("GET", "POST"))
def fantacitorio():
    numberOfGraphs = folders.numberOfFolderFiles(
        "./static/img/fantacitorio/politiciansGroups/"
    )
    folders.deleteFolderFiles(path="./static/img/fantacitorio/userTeam/")
    userTeamResearch = {"username": "", "imagePath": "./", "imageVisibility": "hidden"}
    if request.method == "POST":
        if "searchTeamByUserSubmit" in request.form:
            username = request.form["usernameTextInput"]
            userTeamPath = "./static/img/fantacitorio/userTeam/"
            imageHasBeenSaved = FT.saveUserTeamImage(user=username, path=userTeamPath)
            userTeamResearch = {
                "username": username,
                "imagePath": folders.getFolderFilesNames(userTeamPath),
                "imageVisibility": "visible" if imageHasBeenSaved else "hidden",
            }
            return render_template(
                "fantacitorio.html",
                numberOfTurns=FA.FantacitorioAnalysis.numberOfTurns,
                numberOfGraphs=numberOfGraphs,
                turnsDataTable=FA.FantacitorioAnalysis.turnsInTableFormat,
                fantacitorioStats=FA.FantacitorioAnalysis.getStats(),
                fantacitorioStandings=FA.FantacitorioAnalysis.getStandings(),
                teamsImagesNames=folders.getFolderFilesNames(
                    "./static/img/fantacitorio/teams/"
                ),
                userTeamResearch=userTeamResearch,
            )
        elif "politicianScoreUpdateSubmit" in request.form:
            politicianName = request.form["politicianName"]
            scoreToAdd = request.form["politicianScoreUpdate"]
            for politician in FA.FantacitorioAnalysis.simpleReport:
                if politicianName == politician["name"]:
                    politician["totalScore"] += int(scoreToAdd)
                    return render_template(
                        "fantacitorio.html",
                        numberOfTurns=FA.FantacitorioAnalysis.numberOfTurns,
                        numberOfGraphs=numberOfGraphs,
                        turnsDataTable=FA.FantacitorioAnalysis.turnsInTableFormat,
                        fantacitorioStats=FA.FantacitorioAnalysis.getStats(),
                        fantacitorioStandings=FA.FantacitorioAnalysis.getStandings(),
                        teamsImagesNames=folders.getFolderFilesNames(
                            "./static/img/fantacitorio/teams/"
                        ),
                        userTeamResearch=userTeamResearch,
                    )
    return render_template(
        "fantacitorio.html",
        numberOfTurns=FA.FantacitorioAnalysis.numberOfTurns,
        numberOfGraphs=numberOfGraphs,
        turnsDataTable=FA.FantacitorioAnalysis.turnsInTableFormat,
        fantacitorioStats=FA.FantacitorioAnalysis.getStats(),
        fantacitorioStandings=FA.FantacitorioAnalysis.getStandings(),
        teamsImagesNames=folders.getFolderFilesNames(
            "./static/img/fantacitorio/teams/"
        ),
        userTeamResearch=userTeamResearch,
    )


@app.route("/chess")
def chessPage():
    return render_template("chess.html")

@app.route('/game')
def chessGame():
	if not session.get("scacchiera"):
		board = chess.Board()
		session["scacchiera"] = board
	else:
		board = session["scacchiera"]
	
	table = chess.svg.board(board)

	f = open('./static/img/board.svg', 'w')
	f.write(table)
	f.close()

	return render_template('partita.html', table=table)

@app.route('/give_move', methods=['GET', 'POST'])
def WTurn():
	if not session.get("scacchiera"):
		board = chess.Board() #creo la scacchiera nel session storage se non è presente
		session["scacchiera"] = board
	else:
		board = session["scacchiera"] #prendo la scacchira nel session storage se presente
	
	move=request.form['move'] #prendo la mossa in notazione algebrica
	if(board.turn):
		s = chess.Move.from_uci(move) #Prendo la mossa in input
		if(s in board.legal_moves): #Controllo che possa essere eseguita e che sia il turno del bianco
			board.push(s)
			session["scacchiera"] = board #la eseguo, aggiorno la scacchiera e controllo se la partita è terminata
			if(board.outcome() != None):
				if(board.outcome().winner == None):
					return render_template('draw.html')
				elif(board.outcome().winner):
					return render_template('white.html')
				else:
					return render_template('black.html')
			#invio il tweet con la mossa fatta
			return redirect('https://twitter.com/intent/tweet?text=La%20mia%20mossa%20in%20notazione%20algebrica:%20'+move+"%0AIl%20mio%20fen:%0A"+str(board)+ "%0AInserire%20casella%20di%20partenza%20e%20casella%20di%20arrivo%20per%20giocare" +"%0A%23Ingsw2022")
	
	return render_template('partita.html')


@app.route('/get_move', methods=['GET', 'POST'])
def BTurn():
	if not session.get("scacchiera"):
		board = chess.Board() #creo la scacchiera nel session storage se non è presente
	else:
		board = session["scacchiera"] #prendo la scacchira nel session storage se presente

	account=request.form['account'] #prendo il nome dell'account per poter prendere il primo tweet

	if(board.turn):  #controllo che sia il turno del nero
		return render_template('partita.html')
	else:
		sit = game.__main__(board, account) #prendo la mossa più votata in risposta all'ultimo tweet e controllo se la partita è terminata
		if(sit == "Bianco"):
			return render_template("white.html")
		session["scacchiera"] = sit
	if(board.outcome() != None):
		if(board.outcome().winner == None):
			return render_template('draw.html')
		elif(board.outcome().winner):
			return render_template('white.html')
		else:
			return render_template('black.html')

@app.route("/map")
def mapInterface():
    return render_template("mapInterface.html")


@app.route("/credits", methods=("GET", "POST"))
def creditsPage():
    return render_template("credits.html")


# zip(), str(), ... are not defined in jinja2 templates so we add them to global jinja2 template via Flask.template_global() function
@app.template_global(name="zip")
def _zip(*args, **kwargs):  # to not overwrite builtin zip in globals
    return __builtins__.zip(*args, **kwargs)


@app.template_global(name="str")
def _str(*args, **kwargs):  # to not overwrite builtin str in globals
    return __builtins__.str(*args, **kwargs)


@app.template_global(name="type")
def _type(*args, **kwargs):  # to not overwrite builtin type in globals
    return __builtins__.type(*args, **kwargs)


@app.template_global(name="len")
def _len(*args, **kwargs):  # to not overwrite builtin len in globals
    return __builtins__.len(*args, **kwargs)


@app.template_global(name="enumerate")
def _enumerate(*args, **kwargs):  # to not overwrite builtin enumerate in globals
    return __builtins__.enumerate(*args, **kwargs)


if __name__ == "__main__":
    app.run(debug=True)
