let selectedDroneID = -1;

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

var apiWorking = 0;

function autoUpdater(droneJSON){
    //console.log(droneJSON)
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

    console.log(JSON.stringify({droneID : selectedDroneID}))
    try{
        await fetch(url, {
            method: 'POST',
            headers:{
                'Content-Type':'application/json;charset=utf-8'
            },
            body: JSON.stringify({droneID : selectedDroneID})
        })
        .then(res => res.json())
        .then(obj => extractCoords(JSON.stringify(obj)))
        apiWorking = 0;
    }
    catch(err){
        console.log("bonk")
        console.log(err.message)
        apiWorking = -1;
    }

}

function extractCoords(coordsJSON){
    //console.log(coordsJSON)
    var data = JSON.parse(coordsJSON)
    //console.log(data.lat)
    //console.log(data.lng)
    document.getElementById("liveLat").innerHTML = data.GPSPos.lat
    document.getElementById("liveLng").innerHTML = data.GPSPos.lng
    
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