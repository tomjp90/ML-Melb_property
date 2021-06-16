

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
            
            // PREDICTED VALUE --------------------------------------------------------------------------------------------
            predict_price = numberWithCommas(Math.round(data.result))
            document.getElementById("predict").innerHTML =  "<b> Predicted Value: </b><br>" + predict_price 

            // PREDICTION WARNING --------------------------------------------------------------------------------------------
            console.log(data.landsize)
            if (data.landsize == 0){
                  document.getElementById("warning").innerHTML = "No landsize selected. Prediction is less accurate"
            } else { 
                  document.getElementById("warning").innerHTML = ""                  
            }

            // PROPERTY GROWTH FOR DISTANCE
            toDecimal = data.dist_inc - 1
            inc_rounded = parseFloat(toDecimal).toFixed(2)
            inc_formatted = inc_rounded 
           
            document.getElementById("inc").innerHTML = "There is an average property value growth of <b>" + inc_formatted + "%</b> per year at the selected distance for all types of property"


            // SELECTED FEATURES
            document.getElementById("data1").innerHTML = "<b>Prediction Date Used:</b> " + data.date[0] + "/" + data.date[1] + "/" + data.date[2] + "<br><br><b>Selected:</b> <br> Ditance to CBD: " + data.dist_cbd + "<br> Bedrooms: " + data.beds + "<br> Bathrooms: " + data.baths 
            document.getElementById("data2").innerHTML = "<br><br><br>Cars: " + data.cars + "<br> Property Type: " + data.prop_type + "<br> Landsize: " + data.landsize
         

            // SUBURBS -----------------------------------------------------------------------------------------------------      
            let HTMLsuburbs = []
            let url = "https://www.domain.com.au/sale/?excludeunderoffer=1&street="

            for (var i = 0; i < data.suburbs.length; i++) {
                  suburb = data.suburbs[i]                  
                  sub_string = " "

                  if (suburb.includes(sub_string)) {
                        splitSub = suburb.split(' ').join('+')
                        HTMLsuburbs.push("<a href=" + url + splitSub + " target='_blank'> " + suburb + "</a>")
                  } else {                  
                        HTMLsuburbs.push("<a href=" + url + suburb + " target='_blank'> " + suburb + "</a>")
                  }
            }
            document.getElementById("suburbs").innerHTML = "<b>Suburbs within <b>" + data.dist_cbd + "</b> ± 1km: </b> <br>" + HTMLsuburbs;
           
}
    

