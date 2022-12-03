const map = L.map("map").setView([44.491026, 11.335586], 1);

const tiles = L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
	maxZoom: 19,
	attribution:
		'&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map);

// connecting to database
exports.select = function (callback){
    var db = new sqlite3.Database("../../database.db");           
    db.all("SELECT * FROM all_tweets", function(err,rows){
         if(err) return callback(err);
         rows.forEach(function (row) { 
			if (row.location != null) {
				addMarker(row.location, row.tweet, row.user);
			}
		});
        db.close();a
        return callback(null);
	}); 
}

function addMarker(coordinate, tweet, user) {
	const marker = L.marker(coordinate).addTo(map);
	marker.bindPopup("<b>" + user + "</b><br>" + tweet);
}
// for (const row in tweets) {
// 	marker.append(L.marker([tweet.lat, tweet.lon]).addTo(map).bindPopup(tweet.tweet));
// }
// map.on("click", onMapClick);
