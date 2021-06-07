// Initialising first plot of bedrooms
function init() {
  data = [{
    x: [1, 2, 3, 4, 5, 6],
    y: [435319, 790963, 1053469, 1381954, 1850381, 1937099],
    mode: 'lines',
    line: {
      color: 'rgb(0, 204, 153)',
      width: 3
    }
  
    }];

  layout = {
    title:  'Bedrooms Vs Average House Price',
    xaxis: {
      title: 'Number of Bedrooms',
      showgrid: false,
      tickmode: "linear", 
      tick0: 1,
      dtick: 1
    },
    yaxis: {
      title: 'Average House Price $m',
      showline: false
    },
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)'
  };


  Plotly.newPlot("lineplots", data, layout);
}

// Call updatePlotly() when a change takes place to the DOM
d3.selectAll("#selDataset").on("change", updatePlotly);

// This function is called when a dropdown menu item is selected
function updatePlotly() {
  var dropdownMenu = d3.select("#selDataset");
  var dataset = dropdownMenu.property("value");

  // Initialise 
  var x = [];
  var y = [];
  var title = "";
  var xaxis = "";
  var tick0, dtick; 
  

  // Bedrooms
  if (dataset === 'dataset1') {
    x = [1, 2, 3, 4, 5, 6];
    y = [435319, 790963, 1053469, 1381954, 1850381, 1937099];
    title = "Bedrooms Vs Average House Price";
    xaxis = "Number of Bedrooms";
    tick0 = 1;
    dtick = 1;
  }

  // Bathrooms
  else if (dataset === 'dataset2') {
    x = [1, 2, 3, 4, 5];
    y = [880595, 1196687, 1747261, 2636136, 2667488]; 
    title = "Bathrooms Vs Average House Price";
    xaxis = "Number of Bathrooms";
    tick0 = 1;
    dtick = 1;
  }

  // Distance
  else if (dataset === 'dataset3') {
    x = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50];
    y = [1185662, 1224077, 1046433, 958513, 808006, 661854, 560663, 735575, 571690, 720314];
    title = "Distance Vs Average House Price";
    xaxis = "Distance to CBD (km)";
    tick0 = 5;
    dtick = 5;
  }

  // Landsize
  else if (dataset === 'dataset4') {
    x = [200, 400, 600, 800, 1000, 1200, 1400];
    y = [796182, 1112400, 1067106, 1241597, 1465269, 1336483, 1834727];
    title = "Land Size Vs Average House Price";
    xaxis = "Land Size (m2)";
    tick0 = 200;
    dtick = 200;
  }
  
  // Restyle - rather than redrawing entire image, it just restyles an element of it
  Plotly.restyle("lineplots", "x", [x]); 
  Plotly.restyle("lineplots", "y", [y]);

  var update = {
    title: title,
    xaxis: {
      title: xaxis,
      tick0: tick0,
      dtick: dtick
    }
  };
  Plotly.relayout("lineplots", update) 
}

init();
