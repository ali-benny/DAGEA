console.log("🧪map.js loaded");
const map = L.map("map").setView([44.491026, 11.335586], 1);
L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
	maxZoom: 19,
	attribution:
		'&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map);
console.log("before");

console.log('inside')
var db = new sqlite3.Database("../../marks.db");
var db = new sqlite3.Database("../../topiBastardi.db");
db.all("SELECT * FROM marks", function(err,rows) {
		if (err) return callback(err);
		rows.forEach(function (row) { 
			if (!(row.lat == 0.0 && row.lon == 0.0)) {
				//addMarker(row.lat, row.lon, row.user, row.text);
				addMarker(row.lat, row.lon, 'row.user', 'row.text');
			}
		});
	db.close();
	return callback(null);
}); 

/*
exports.select =function (callback) {
	console.log('inside')
	var db = new sqlite3.Database("../../marks.db");
	var db = new sqlite3.Database("../../topiBastardi.db");
	db.all("SELECT * FROM marks", function(err,rows) {
			if (err) return callback(err);
			rows.forEach(function (row) { 
				if (!(row.lat == 0.0 && row.lon == 0.0)) {
					//addMarker(row.lat, row.lon, row.user, row.text);
					addMarker(row.lat, row.lon, 'row.user', 'row.text');
				}
			});
		db.close();
		return callback(null);
	}); 
}
*/
function addMarker(lat, lon, user, tweet) {
	const marker = L.marker([lat, lon]).addTo(map);
	marker.bindPopup("<b>" + user + "</b><br>" + tweet);

	// var c1 = 44.491026; var c2 = 11.335586
	//tmp = L.marker([c1, c2]).addTo(map)
	//tmp.bindPopup("<b>" + 'Nome Utente 1' + "</b><br>" + 'Testo del tweet 1');
}

// for (const row in tweets) {
// 	marker.append(L.marker([tweet.lat, tweet.lon]).addTo(map).bindPopup(tweet.tweet));
// }
// map.on("click", onMapClick);
