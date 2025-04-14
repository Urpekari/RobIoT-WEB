autoUpdater(2)

function autoUpdater(droneJSON){
    console.log(droneJSON)
    setInterval(getEpicThing, 1000);
}

// function getTest(){
//     const url = 'http://localhost:5000/testApi'
//     fetch(url)
//     .then(response => response.json())
//     .then(json=>{
//         console.log(json)
//     })
// }

async function getEpicThing(){
    let url = 'http://localhost:5000/getLivePos';

    console.log(JSON.stringify({droneID : 2}))

    await fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json;charset=utf-8'
        },
        body: JSON.stringify({droneID : 2})
    })
    .then(res => res.json())
    .then(obj => extractCoords(JSON.stringify(obj)))
    //.then(obj => console.log(obj));
    //console.log(obj)
}

function extractCoords(coordsJSON){
    console.log(coordsJSON)
    var data = JSON.parse(coordsJSON)
    console.log(data.lat)
    console.log(data.lng)
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}