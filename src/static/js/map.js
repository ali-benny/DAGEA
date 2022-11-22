const map = L.map("map").setView([44.491026, 11.335586], 10);

const tiles = L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
	maxZoom: 19,
	attribution:
		'&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map);

const marker = L.marker([44.491026, 11.335586], 10)
	.addTo(map)
	.bindPopup("<b>Hello world!</b><br />I am a popup.")
	.openPopup();

map.on("click", onMapClick);
