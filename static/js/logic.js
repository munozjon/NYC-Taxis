// Connect to Flask endpoint

function init() {
d3.image("http://127.0.0.1:5000/heatmap",  
    { crossOrigin: "anonymous" }).then((img) => {
        document.getElementById('pie').innerHTML = ""; 
        document.getElementById("pie").appendChild(img);; 
    });
};

init();
