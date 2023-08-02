
// import * as vega from "vega";
// import VegaLite from "react-vega-lite";
// import { createClassFromSpec } from "react-vega";
import * as d3 from "d3";
import React, {useState, useEffect} from 'react'
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

      if (!plotData) {
        // append the svg object to the body of the page
        const svg = d3.select("#complexityChart")
        .append("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
        .append("g")
          .attr("transform", `translate(${margin.left},${margin.top})`);

        // d3.csv("/Users/lilyge/Downloads/gRIPS23/gRIPS-Fujitsu-2023/flask-server/step4_plot_data.csv").then(function(data){ console.log(data)});

        //Read the data
        d3.csv("https://raw.githubusercontent.com/holtzy/data_to_viz/master/Example_dataset/3_TwoNumOrdered_comma.csv",

        // When reading the csv, I must format variables:
        function(d){
          return { date : d3.timeParse("%Y-%m-%d")(d.date), value : d.value }
        }).then(

        // Now I can use this dataset:
        function(data) {
          console.log(data)
          // Add X axis --> it is a date format
          const x = d3.scaleTime()
            .domain(d3.extent(data, function(d) { return d.date; }))
            .range([ 0, width ]);
          svg.append("g")
            .attr("transform", `translate(0, ${height})`)
            .call(d3.axisBottom(x));

          // Add Y axis
          const y = d3.scaleLinear()
            .domain([0, d3.max(data, function(d) { return +d.value; })])
            .range([ height, 0 ]);
          svg.append("g")
            .call(d3.axisLeft(y));

          // Add the line
          svg.append("path")
            .datum(data)
            .attr("fill", "none")
            .attr("stroke", "steelblue")
            .attr("stroke-width", 1.5)
            .attr("d", d3.line()
              .x(function(d) { return x(d.date) })
              .y(function(d) { return y(d.value) })
              )

        })
          setPlotData(true)
      }
      

    }
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

    return (
      <div id="complexityChart">
        <button onClick={showChart}>click</button>
        {/* <VegaLite spec={spec} data={{ values: barData }} />; */}
      </div>
    )

};
export default DisplayChart;