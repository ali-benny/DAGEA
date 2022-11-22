// const popup = L.popup()
// 	.setLatLng([44.4311, 11.3], 10)
// 	.setContent("I am a standalone popup.")
// 	.openOn(map);

// marker([44.491026, 11.335586], 10)
// 	.addTo(map)
// 	.bindPopup("<b>Hello world!</b><br />I am a popup.")
// 	.openPopup();

var db = require('database');
var con = db.createConnection({
  host: "localhost",
  user: "yourusername",
  password: "yourpassword",
  database: "mydb"
});
con.connect(function(err) {
  if (err) throw err;
  con.query("SELECT * FROM customers", function (err, result, fields) {
    if (err) throw err;
	console.log(result);
  });
});