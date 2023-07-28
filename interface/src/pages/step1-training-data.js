
import React, {useState, useEffect} from 'react'
import $ from 'jquery';

const Step1_training_data = () => {

    const table_element = document.getElementById("training_table")
	if (table_element) {
		table_element.remove()
	}

    const [trainingData, setTrainingData] = useState({}) 
    useEffect(() => {
        // Using fetch to fetch the api from
        // flask server it will be redirected to proxy
        fetch("/step1_display").then((res) =>
            res.json().then((data_in) => {
                // Setting a data from api
                setTrainingData(data_in);
                console.log(data_in)
            })
            );
        }, []);

    console.log(trainingData)
    console.log(trainingData.length)
    let output = "Loading training data ..."
    
    if (trainingData.length) {

        const data_table = document.createElement("table");
		data_table.setAttribute("id", "training_table")
		const table_header = document.createElement("thead");
        const table_header_row = document.createElement("tr");
        let hover_tracker = {}
        let table_container = document.getElementById("tableContainer")
        const container_element = document.getElementById("step1container")
        for (var column_key in trainingData[0]) {
            console.log(column_key)
            const new_header = document.createElement("th")
            const header_text = document.createTextNode(column_key);
            let column_str = column_key.replace(/[^a-z0-9]/gi, '').replace(/\s/g, '')
            new_header.setAttribute("id", "column_"+column_str)
            let hover_key = "hover_"+column_str

            new_header.appendChild(header_text)
            table_header_row.appendChild(new_header)
        }

        table_header.appendChild(table_header_row)
        const table_body = document.createElement("tbody");
        for (let i = 0; i < trainingData.length; i += 1) {
			const table_row = document.createElement("tr")
			// console.log(data[0])
			// const div_container = document.createElement("div")
			// div_container.setAttribute("id", "row_div")
			for (let col in trainingData[i]) {
				// console.log(trainingData[i][col])
                const table_cell = document.createElement("td")
				const cell_text = document.createTextNode(trainingData[i][col]);
				table_cell.appendChild(cell_text);
				// div_container.appendChild(table_cell);
				table_row.appendChild(table_cell);
            }
           table_body.appendChild(table_row); 
        //    output = ""
        }


        data_table.appendChild(table_header);
		data_table.appendChild(table_body);
        // let table_container = document.getElementById("tableContainer")
		table_container.appendChild(data_table);


        for (var column_key in trainingData[0]) {
            console.log("ever here???")
            const new_hover = document.createElement("div")
            let column_hover_str = column_key.replace(/[^a-z0-9]/gi, '').replace(/\s/g, '')
            new_hover.setAttribute("id", "hover_"+column_hover_str)
            let new_hover_text = document.createTextNode("testing"+column_key)
            new_hover.classList.add("displayNone")
            new_hover.appendChild(new_hover_text)
            container_element.appendChild(new_hover)
            const get_header = document.getElementById("column_"+column_hover_str)
            let hover_key = "#hover_"+column_hover_str
            get_header.addEventListener("mouseover", function(e) {
                // document.getElementById("hover_"+column_key).classList.remove("displayNone")
                console.log(e.pageX+20)
                $(hover_key).css({
                    display: 'block',
                    left: e.pageX+10,
                    top: e.pageY,
                    position: 'absolute',
                    width: '10rem',
                    height: '5rem',
                    background: 'black',
                    color: 'white',
                    textAlign: 'center',
                    padding: '1rem'
                    
                })
            })
    
            get_header.addEventListener("mouseout", function(e) {
                $(hover_key).css({
                    display: 'None',
                })
            })
            // hover_tracker[hover_key] = 1
        }
        
    }

    return (
		<div >
            <div id="step1container">

            </div>
            <div class="tableContainer" id="tableContainer">

            </div>
			{/* <div id="header1Hover">testing hover 1</div>
			<div id="header2Hover">testing hover 2</div>
			<div id="header3Hover">testing hover 3</div>
			<div id="header4Hover">testing hover 4</div>
			<p id="explanationStep2">Wide Learning generates all possible combinations of variables. The combinations in this table are the most important combinations of features to determine whether or not an animal is a mammal. The importance of a combination is measured by the length of the combination and the number of positive and negative occurrences for the animals in the training dataset that have that combination of features. The table below will only show feature combinations with a maximum length of three, however, important feature combinations that are longer than three may exist.</p>
        <div class="loading">
            <p>{output}</p>
        </div> */}
		</div>
    )
};

export default Step1_training_data;