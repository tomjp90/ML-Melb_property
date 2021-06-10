

var bedrooms= [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
var baths = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
var cars = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
var pType = ['House', 'Unit', "Townhouse"];

var size = [];
var num = 0
var iterate = 25 
for (var i = 0; i < 42; i++){      
      size.push(num)
      num = num + iterate

}

var distCBD = [];
for (var i = 0; i < 50; i++){
      distCBD.push(i)      
}

// Create empty array to push into
var HTMLdistCBD = [];
var HTMLbedrooms = [];
var HTMLbaths = [];
var HTMLcars = [];
var HTMLpType = [];
var HTMLsize = []

//loop over each array length and add drop down option

// DISTANCE TO CBD
for (var i = 0; i < distCBD.length; i++) {
      HTMLdistCBD.push("<option>" + distCBD[i] + "</option>")
}
document.getElementById("dist").innerHTML = HTMLdistCBD.join("");

//BEDROOMS
for (var i = 0; i < bedrooms.length; i++) {
      HTMLbedrooms.push("<option>" + bedrooms[i] + "</option>")
}
document.getElementById("bed").innerHTML = HTMLbedrooms.join("");

//BATHS
for (var i = 0; i < baths.length; i++) {
      HTMLbaths.push("<option>" + baths[i] + "</option>")
}
document.getElementById("bath").innerHTML = HTMLbaths.join("");

//CARS
for (var i = 0; i < cars.length; i++) { 
      HTMLcars.push("<option>" + cars[i] + "</option>")
}
document.getElementById("car").innerHTML = HTMLcars.join("");

//PROPERTY TYPE
for (var i = 0; i < pType.length; i++) {
      HTMLpType.push("<option>" + pType[i] + "</option>")
}
document.getElementById("pType").innerHTML = HTMLpType.join("");

//LANDSIZE
for (var i = 0; i < size.length; i++) {
      HTMLsize.push("<option>" + size[i] + "</option>")
}
document.getElementById("landsize").innerHTML = HTMLsize.join("");


//FIND USER INPUT FROM DROPDOWN LIST-----------------------------------------

//select the button using D3
var button = d3.select("#filter-btn");
//on click run resetTable function
button.on("click", doPredict);
 
function doPredict() {

      d3.event.preventDefault();

      d3.select("#prediction").style("display", "none");
      
      let distanceCBD = d3.select("#dist").node().value;
      let beds = d3.select("#bed").node().value;
      let baths = d3.select("#bath").node().value;
      let cars = d3.select("#car").node().value;
      let propType = d3.select("#pType").node().value;
      let landsize = d3.select("#landsize").node().value;

      let data = {
          "dist_cbd": distanceCBD,
          "beds": parseInt(beds),
          "baths": parseInt(baths),
          "cars": parseInt(cars),
          "prop_type": propType,
          "landsize": parseInt(landsize)

      }

      d3.json(
            "/user_predict", {
                method: "POST",
                body: JSON.stringify(data),
                headers: {
                    "Content-type": "application/json; charset=UTF-8"
                }
            }
        ).then(
            (data) => showResult(data)
        );
    
    }

      function numberWithCommas(x) {
            return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
      }

      function showResult(data) {
            predict_price = numberWithCommas(Math.round(data.result))
            // PREDICTED VALUE --------------------------------------------------------------------------------------------
            document.getElementById("predict").innerHTML =  "Predicted Value: <br> $" + predict_price

            // SUBURBS -----------------------------------------------------------------------------------------------------      
            let HTMLsuburbs = []
            let url = "https://www.domain.com.au/sale/?excludeunderoffer=1&street="

            for (var i = 0; i < data.suburbs.length; i++) {
                  suburb = data.suburbs[i]                  
                  sub_string = " "

                  if (suburb.includes(sub_string)) {
                        splitSub = suburb.split(' ').join('+')
                        HTMLsuburbs.push("<a href=" + url + splitSub + "> " + suburb + "</a>")
                  } else {                  
                        HTMLsuburbs.push("<a href=" + url + suburb + "> " + suburb + "</a>")
                  }
            }
            document.getElementById("suburbs").innerHTML = "Suburbs within" + data.dist_cbd + " ±1km of selected distance: <br>" + HTMLsuburbs;
  
      }
      // ? suburb.split(' ').join('+') : suburb

