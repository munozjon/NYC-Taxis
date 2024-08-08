
// Initial page load function
function init() {
    
    const room_url = "http://127.0.0.1:5000/seaborn";
    fetch(room_url)
        .then(function(response) {
            return response.text();
        }).then(function(data) {
            document.getElementById("pie")
            .innerHTML += data;
        });    
    
        
    const histUrl = "http://127.0.0.1:5000/histogram";
    fetch(histUrl)
        .then(function(response) {
            return response.text();
        }).then(function(data) {
            document.getElementById("bar")
            .innerHTML += data;
        });    

        
    const pltUrl = "http://127.0.0.1:5000/matplotlib";
    fetch(pltUrl)
        .then(function(response) {
            return response.text();
        }).then(function(data) {
            document.getElementById("box")
            .innerHTML += data;
        });    
    
    };

    init();
    