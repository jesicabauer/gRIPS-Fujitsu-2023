
// import * as vega from "vega";
// import VegaLite from "react-vega-lite";
// import { createClassFromSpec } from "react-vega";
import * as d3 from "d3";
import React, {useState, useEffect} from 'react'
// import { Line } from 'react-chartjs-2';
// import { CubejsApi } from '@cubejs-client/core';

// import {vl} from '@vega/vega-lite-api'

const DisplayChart = () => {

  // df = [
  //   {"city": "Seattle",  "month": "Apr", "precip": 2.68},
  //   {"city": "Seattle",  "month": "Aug", "precip": 0.87},
  //   {"city": "Seattle",  "month": "Dec", "precip": 5.31},
  //   {"city": "New York", "month": "Apr", "precip": 3.94},
  //   {"city": "New York", "month": "Aug", "precip": 4.13},
  //   {"city": "New York", "month": "Dec", "precip": 3.58},
  //   {"city": "Chicago",  "month": "Apr", "precip": 3.62},
  //   {"city": "Chicago",  "month": "Aug", "precip": 3.98},
  //   {"city": "Chicago",  "month": "Dec", "precip": 2.56},
  // ];

  // vega.markPoint()
  // .data(df)
  // .render()
    // set the dimensions and margins of the graph
    const margin = {top: 10, right: 30, bottom: 30, left: 60},
    width = 460 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

    const [plotData, setPlotData] = useState(false)

    const showChart = () => {
      const xValues = [50,60,70,80,90,100,110,120,130,140,150];
      const yValues = [7,8,8,9,9,9,10,11,14,14,15];

      // new Chart("myChart", {
      //   type: "line",
      //   data: {
      //     labels: xValues,
      //     datasets: [{
      //       fill: false,
      //       lineTension: 0,
      //       backgroundColor: "rgba(0,0,255,1.0)",
      //       borderColor: "rgba(0,0,255,0.1)",
      //       data: yValues
      //     }]
      //   },
      //   options: {
      //     legend: {display: false},
      //     scales: {
      //       yAxes: [{ticks: {min: 6, max:16}}],
      //     }
      //   }
      // });
    }

      // if (!plotData) {
      //   // append the svg object to the body of the page
      //   const svg = d3.select("#complexityChart")
      //   .append("svg")
      //     .attr("width", width + margin.left + margin.right)
      //     .attr("height", height + margin.top + margin.bottom)
      //   .append("g")
      //     .attr("transform", `translate(${margin.left},${margin.top})`);

      //   // d3.csv("/Users/lilyge/Downloads/gRIPS23/gRIPS-Fujitsu-2023/flask-server/step4_plot_data.csv").then(function(data){ console.log(data)});

      //   //Read the data
      //   d3.csv("https://raw.githubusercontent.com/holtzy/data_to_viz/master/Example_dataset/3_TwoNumOrdered_comma.csv",

      //   // When reading the csv, I must format variables:
      //   function(d){
      //     return { date : d3.timeParse("%Y-%m-%d")(d.date), value : d.value }
      //   }).then(

      //   // Now I can use this dataset:
      //   function(data) {
      //     console.log(data)
      //     // Add X axis --> it is a date format
      //     const x = d3.scaleTime()
      //       .domain(d3.extent(data, function(d) { return d.date; }))
      //       .range([ 0, width ]);
      //     svg.append("g")
      //       .attr("transform", `translate(0, ${height})`)
      //       .call(d3.axisBottom(x));

      //     // Add Y axis
      //     const y = d3.scaleLinear()
      //       .domain([0, d3.max(data, function(d) { return +d.value; })])
      //       .range([ height, 0 ]);
      //     svg.append("g")
      //       .call(d3.axisLeft(y));

      //     // Add the line
      //     svg.append("path")
      //       .datum(data)
      //       .attr("fill", "none")
      //       .attr("stroke", "steelblue")
      //       .attr("stroke-width", 1.5)
      //       .attr("d", d3.line()
      //         .x(function(d) { return x(d.date) })
      //         .y(function(d) { return y(d.value) })
      //         )

      //   })
      //     setPlotData(true)
      // }
      

    // }
    // (async function() {
    //   const data = [
    //     { year: 2010, count: 10 },
    //     { year: 2011, count: 20 },
    //     { year: 2012, count: 15 },
    //     { year: 2013, count: 25 },
    //     { year: 2014, count: 22 },
    //     { year: 2015, count: 30 },
    //     { year: 2016, count: 28 },
    //   ];
    
    //   new Chart(
    //     document.getElementById('complexityChart'),
    //     {
    //       type: 'bar',
    //       data: {
    //         labels: data.map(row => row.year),
    //         datasets: [
    //           {
    //             label: 'Acquisitions by year',
    //             data: data.map(row => row.count)
    //           }
    //         ]
    //       }
    //     }
    //   );
    // })();
    // const spec = {
    //   description: "A simple bar chart with embedded data.",
    //   // width: "container",
    //   // height: 400,
    //   mark: "bar",
    //   encoding: {
    //     x: { field: "a", type: "ordinal" },
    //     y: { field: "b", type: "quantitative" }
    //   }
    // };

    const data = {
      labels: [1, 2, 3, 4, 5, 6],
      datasets: [
        {
          // label: "First dataset",
          data: [33, 53, 85, 41, 44, 65],
          // fill: true,
          // backgroundColor: "rgba(75,192,192,0.2)",
          // borderColor: "rgba(75,192,192,1)"
        }
        // {
        //   label: "Second dataset",
        //   data: [33, 25, 35, 51, 54, 76],
        //   fill: false,
        //   borderColor: "#742774"
        // }
      ]
    };


    return (
      <div>
        {/* <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.4/Chart.js"></script>
        <canvas id="myChart" style="width:100%;max-width:700px"></canvas>
        <button onClick={showChart}>click</button> */}
        {/* <Line data={data} /> */}
        {/* <VegaLite spec={spec} data={{ values: barData }} />; */}
        {/* <div id="fig_el831643170172804879151470"></div> */}


      </div>
    )

};
export default DisplayChart;