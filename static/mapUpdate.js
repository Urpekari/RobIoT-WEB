let selectedDroneID = -1;

const pastPositions = [];
const waypoints = [];
const bannedAreas = [];

let prevPosition = null;



try{
    if (typeof(document.getElementById("droneID").innerHTML)!=null){
        selectedDroneID = document.getElementById("droneID").innerHTML;
        
    }
    else{
        selectedDroneID = -1;
    }    
}
catch(err){
    document.getElementById("droneID").innerHTML = err.message;
    selectedDroneID = -1;
}

if (selectedDroneID > 0){
    autoUpdater(selectedDroneID);
}

//console.log(selectedDroneID)


var map = L.map('map').setView([parseFloat("43.262361"), parseFloat("-2.949067")], 15);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);



//===============================================================================================

var apiWorking = 0;
function autoUpdater(droneJSON){
    var refreshMap = setInterval(
        function(){
            getEpicThing();
            console.log(apiWorking)
            if(apiWorking < 0){
                console.log("Cocking nora");
                clearInterval(refreshMap);
            }
        }, 1000);
}

async function getEpicThing(){
    let url = 'http://localhost:5000/getLiveData';

    //console.log(JSON.stringify({droneID : selectedDroneID}))
    try{
        await fetch(url, {
            method: 'POST',
            headers:{
                'Content-Type':'application/json;charset=utf-8'
            },
            body: JSON.stringify({droneID : selectedDroneID})
        })
        .then(res => res.json())
        .then(obj => extractLiveCoords(JSON.stringify(obj)))
        apiWorking = 0;
    }
    catch(err){
        console.log("bonk")
        console.log(err.message)
        apiWorking = -1;
    }

}

function extractLiveCoords(coordsJSON){
    //console.log(coordsJSON)
    var data = JSON.parse(coordsJSON)
    
    //map.removeLayer(marker)

    var marker;
    if(pastPositions[pastPositions.length -1] !=  [parseFloat(data.GPSPos.lat), parseFloat(data.GPSPos.lng)]){

        console.log("These are definitely different:")
        console.log(pastPositions[pastPositions.length - 1])
        console.log([parseFloat(data.GPSPos.lat), parseFloat(data.GPSPos.lng)])
        document.getElementById("JSTEST").innerHTML = pastPositions

        currentPosition = [parseFloat(data.GPSPos.lat), parseFloat(data.GPSPos.lng)]
        pastPositions.push(currentPosition)

        prevPosition = pastPositions[-2]
        console.log("Previous Position:")
        console.log(prevPosition)
        console.log("Current Position:")
        console.log(currentPosition)
        
        L.marker(currentPosition).addTo(map)

        map.panTo(currentPosition, 10);
    }

    document.getElementById("liveLat").innerHTML = data.GPSPos.lat
    document.getElementById("liveLng").innerHTML = data.GPSPos.lng
    document.getElementById("livetime").innerHTML = data.GPSPos.cur
    
    document.getElementById("nextWPlat").innerHTML = data.NextWaypoint.lat
    document.getElementById("nextWPlng").innerHTML = data.NextWaypoint.lng
    document.getElementById("nextWPETA").innerHTML = data.NextWaypoint.eta
    
    document.getElementById("goalWPlat").innerHTML = data.Destination.lat
    document.getElementById("goalWPlng").innerHTML = data.Destination.lng
    document.getElementById("goalWPETA").innerHTML = data.Destination.eta
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function getAllPastData(droneID){

}