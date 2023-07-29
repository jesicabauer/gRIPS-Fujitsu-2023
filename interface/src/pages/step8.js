import React, {useState, useEffect} from 'react';
import $ from 'jquery';

const Step8 = () => {
	const table_element = document.getElementById("combo_table")
	if (table_element) {
		table_element.remove()
	}
	const table3_element = document.getElementById("table_step3")
	if (table3_element) {
		table3_element.remove()
	}

	const [data6, setData6] = useState({}) 
    useEffect(() => {
    // Using fetch to fetch the api from
    // flask server it will be redirected to proxy
    fetch("/step6").then((res) =>
        res.json().then((data_in) => {
            // Setting a data from api
            setData6(data_in);
            console.log(data_in)
        })
        );
    }, []);

	console.log(data6.length)
	var output = "Loading prediction scores ..."

	if (data6.length) {
		const data_table = document.createElement("table");
		data_table.setAttribute("id", "table_step3")
		const table_header = document.createElement("thead");
        const table_header_row = document.createElement("tr");
        // let hover_tracker = {}
        // let table_container = document.getElementById("tableContainer")
        const container_element = document.getElementById("step8container")

		for (var column_key in data6[0]) {
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
        for (let i = 0; i < data6.length; i += 1) {
			const table_row = document.createElement("tr")
			// console.log(data[0])
			// const div_container = document.createElement("div")
			// div_container.setAttribute("id", "row_div")
			for (let col in data6[i]) {
				// console.log(trainingData[i][col])
                const table_cell = document.createElement("td")
				const cell_text = document.createTextNode(data6[i][col]);
				table_cell.appendChild(cell_text);
				// div_container.appendChild(table_cell);
				table_row.appendChild(table_cell);
            }
           table_body.appendChild(table_row); 
           output = ""
        }

		data_table.appendChild(table_header);
		data_table.appendChild(table_body);
        // let table_container = document.getElementById("tableContainer")
		document.body.appendChild(data_table);

		for (var column_key in data6[0]) {
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

		// const data_table = document.createElement("table");
		// data_table.setAttribute("id", "table_step3")
		// const table_header = document.createElement("thead");
		// const table_header_row = document.createElement("tr");
		// const header_1 = document.createElement("th")
		// const header_text_1 = document.createTextNode("Animal");
		// header_1.setAttribute("id", "step6_column1")
		// const header_2 = document.createElement("th")
		// const header_text_2 = document.createTextNode("Score from LASSO");
		// header_2.setAttribute("id", "step6_column2")
		// const header_3 = document.createElement("th")
		// const header_text_3 = document.createTextNode("Prediction");
		// header_3.setAttribute("id", "step6_column3")

		// header_1.appendChild(header_text_1);
		// header_2.appendChild(header_text_2);
		// header_3.appendChild(header_text_3);

		// table_header_row.appendChild(header_1)
		// table_header_row.appendChild(header_2)
		// table_header_row.appendChild(header_3)

		// table_header.appendChild(table_header_row)
		// const table_body = document.createElement("tbody");
		// for (let i = 0; i < data6.length; i += 1) {
		// 	const table_row = document.createElement("tr")
			// console.log(data[0])
			// const div_container = document.createElement("div")
			// div_container.setAttribute("id", "row_div")
			// for (let col in data6[i]) {
			// 	console.log(data6[i][col])
			// 	const table_cell = document.createElement("td")
			// 	const cell_text = document.createTextNode(data6[i][col]);
			// 	table_cell.appendChild(cell_text);
			// 	// div_container.appendChild(table_cell);
			// 	table_row.appendChild(table_cell);
			// }
			// div_container)
			// output = data.map((row, i) => (
			// 	<tr key={i}>
			// 		<td>{document.createTextNode(row.important_combo)}</td>
			// 		<td>{document.createTextNode(row.combo_length)}</td>
			// 		<td>{document.createTextNode(row.pos_count)}</td>
			// 		<td>{document.createTextNode(row.neg_count)}</td>
			// 	</tr>
			// ))
		// 	table_body.appendChild(table_row);
		// 	output = ""
		// }
		
		// data_table.appendChild(table_header);
		// data_table.appendChild(table_body);
		// document.body.appendChild(data_table);
	}

	return (
		<div>
			<div id = "step8container">
				
			</div>
			<div class="loading">
				<p>{output}</p>
			</div>
		</div>
		
	);
};

export default Step8;
