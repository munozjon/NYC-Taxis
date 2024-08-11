// Bins with color coordination for legend
const legendColors = {
    "Infrequent": "#ffee73",
    "Frequent": "#a1dab4",
    "Regular": "#41b6c4",
    "Common": "#2c7fb8",
    "Very Common": "#253494"
};

// Initialize the map
function createMap() {

    // Create the background layer for our map
    var standard = L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager_labels_under/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 20
    });    
    
    // Initialize the marker layer groups
    let taxiZones = L.layerGroup()
    let dropoffs = L.layerGroup()
    let pickups = L.layerGroup()

    // Load the taxi zone GeoJSON data
    d3.json("https://data.cityofnewyork.us/api/geospatial/d3c5-ddgc?method=export&format=GeoJSON")
    .then(function(zoneData){

        // Add the base zones to the layer group
        L.geoJson(zoneData, {
            color:"black"
        }).addTo(taxiZones),

        // Read the endpoint for binned pickup and dropoff zones and add to their layer groups
        d3.json("http://127.0.0.1:5000/pickup_zones.json").then((data) => {
            let pickupData = JSON.parse(data);
            pickupLayer(zoneData, pickupData).addTo(pickups);
        }),
        d3.json("http://127.0.0.1:5000/dropoff_zones.json").then((data) => {
            let dropoffData = JSON.parse(data);
            dropoffLayer(zoneData, dropoffData).addTo(dropoffs);
        })
    
    });

    // Create a baseMaps object to hold the background layer
    let baseMaps = {
        "Standard": standard,
    };
  
    // Create an overlayMaps object to hold the layer groups
    let overlayMaps = {
        "Taxi Zones": taxiZones,
        "Dropoffs": dropoffs,
        "Pickups": pickups
    };

    // Create the map object with options
    let myMap = L.map("map", {
      center: [40.78,-73.96],
      zoom: 11,
      layers: [standard, taxiZones]
    });
  
    // Add layer control to the map
    L.control.layers(baseMaps, overlayMaps, {
      collapsed: false
    }).addTo(myMap);


    // // Create the legend
    let legend = L.control({position: "bottomright"});
    // Function to add labels to the legend
    legend.onAdd = function (map) {
        var div = L.DomUtil.create('div', 'info legend');
        // Loop through the key-color object and return an HTML item
        for (const property in legendColors) {
            div.innerHTML +=
                '<i style="background:' + legendColors[property] + '"></i> ' +
                property + '<br>';
        }
        return div;
    };
    legend.addTo(myMap);
    };




// Match the zone ID for each feature in the geoJSON with its respective endpoint data to return its bin
function getBin(id, data) {
    for (let i=0; i<data.length; i++) {
        let zone = data[i];
        // Object.values() is used to be able to work for both pickups and dropoffs endpoints
        if (parseInt(id) === Object.values(zone)[0]) {
            return getColor(Object.values(zone)[1])
        }
    };
};

// Matches the bin with its corresponding color code
function getColor(bin) {
    for (const property in legendColors) {
        if (bin === property) {
            return legendColors[property]
        }
    }
};

// Create the dropoffs layer
function dropoffLayer(zoneData, dropoffData) {
    function style(feature) {
        return {
            fillColor: getBin(feature.properties.location_id, dropoffData),
            weight: 2,
            opacity: 1,
            color: 'white',
            fillOpacity: 0.7
        }
    }
    // Return the layer, including a popup for the name of the zone and the borough
    return L.geoJson(zoneData, {
        onEachFeature: function (feature,layer) {
            layer.bindPopup(`<h3>${feature.properties.zone}</h3> <hr> <h5>${feature.properties.borough}</h5>`);
        },
        style: style})
    };

// Create the pickups layer
function pickupLayer(zoneData, pickupData) {
    function style(feature) {
        return {
            fillColor: getBin(feature.properties.location_id, pickupData),
            weight: 2,
            opacity: 1,
            color: 'grey',
            fillOpacity: 0.7
        }
    }
    return L.geoJson(zoneData, {
        onEachFeature: function (feature,layer) {
            layer.bindPopup(`<h3>${feature.properties.zone}</h3> <hr> <h5>${feature.properties.borough}</h5>`);
        },
        style: style})
    };

// Initialize the map
createMap();


// Initial page load function to load all the visualizations
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
