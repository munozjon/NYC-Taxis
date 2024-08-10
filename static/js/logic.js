
// Initialize the map
mapboxgl.accessToken = 'pk.eyJ1IjoiY21kdXJhbiIsImEiOiJjbHpseXRldXQwODFjMm1vYzRuNnZhdjg0In0.09gQaWtNV7hLGC67Fd7R4w';
const map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v9',
    projection: 'globe', // Display the map as a globe, since satellite-v9 defaults to Mercator
    zoom: 11,
    center: [-73.96, 40.78] // starting position [lng, lat]
});

// TESTING
// geoJson = 'https://data.cityofnewyork.us/api/geospatial/d3c5-ddgc?method=export&format=GeoJSON'
// json = 'http://127.0.0.1:5000/coordinates.json'
// fetch(json)
//     .then((response) => console.log(response))
//     .then((json) => console.log(json));

// Add map controls
map.addControl(new mapboxgl.NavigationControl());
map.scrollZoom.disable();

map.on('style.load', () => {
    map.setFog({}); // Set the default atmosphere style

    map.addSource('taxi-zones', {
        type: 'geojson',
        data: 'https://data.cityofnewyork.us/api/geospatial/d3c5-ddgc?method=export&format=GeoJSON'
    });

    // // Border around the polygons
    map.addLayer({
        'id': 'taxi-zones-outline',
        'type': 'line',
        'source': 'taxi-zones',
        'layout': {},
        'paint': {
            'line-color': '#000000',
            'line-width': 1,
            'fill-color': {
                property: 'frequency',
                stops: [[2, '#fff'], [5, '#f00']]
                }
        }
    });




});


// Initial page load function
function init() {
    
    const room_url = "http://127.0.0.1:5000/heatmap";
    fetch(room_url)
        .then(function(response) {
            return response.text();
        }).then(function(data) {
            document.getElementById("heatmap")
            .innerHTML += data;
        });    
    
        
    const histUrl = "http://127.0.0.1:5000/histogram";
    fetch(histUrl)
        .then(function(response) {
            return response.text();
        }).then(function(data) {
            document.getElementById("histogram")
            .innerHTML += data;
        });    

        
    const pltUrl = "http://127.0.0.1:5000/matplotlib";
    fetch(pltUrl)
        .then(function(response) {
            return response.text();
        }).then(function(data) {
            document.getElementById("bar")
            .innerHTML += data;
        });    
    
    };

init();
    