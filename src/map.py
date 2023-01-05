import folium 
import shutil
import os

class Map:
    #myMap = None

    @classmethod
    def __init__(cls):
        cls.myMap = folium.Map(
            location=[44.494951765822265, 11.342572166862746],      # Bologna is the start location
            zoom_start=13,
            tiles="CartoDB dark_matter"
        )
        cls._saveMap()

    @classmethod
    def _saveMap(cls):
        cls.myMap.save("map.html")
        try:
            shutil.move("./map.html", "./templates/components")
        except shutil.Error:
            os.remove('./templates/components/map.html')
            shutil.move("./map.html", "./templates/components")

    @classmethod
    def addMarkers(cls, tweets):
        for tweet in tweets:
            folium.Marker(
                [tweet['latitude'], tweet['longitude']],
                # Vengono mostrati: posto taggato, nome utente e testo del tweet 
                popup="<h5>" + tweet['taggedPlace'] + "</h5><h6>" + tweet['username'] + "</h6><p>" + tweet['text'] + "</p>"
            ).add_to(cls.myMap)
        cls._saveMap()