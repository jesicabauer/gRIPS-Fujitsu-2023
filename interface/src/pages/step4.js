import React, {useState, useEffect} from 'react'

const Step4 = () => {
	const table_element = document.getElementById("combo_table")
	if (table_element) {
		table_element.remove()
	}
	const table3_element = document.getElementById("table_step3")
	if (table3_element) {
		table3_element.remove()
	}
	const model_metrics_table_element = document.getElementById("model_metrics_table")
	if (model_metrics_table_element) {
		model_metrics_table_element.remove()
	}

	const [modelMetrics, setModelMetrics] = useState({}) 
    useEffect(() => {
        // Using fetch to fetch the api from
        // flask server it will be redirected to proxy
        fetch("/model_accuracy_complexity").then((res) =>
            res.json().then((data_in) => {
                // Setting a data from api
                setModelMetrics(data_in);
                console.log(data_in)
            })
            );
        }, []);

    console.log(modelMetrics)
    console.log(modelMetrics.length)
	// var output = "Loading learned weights ..."

	let table_container = document.getElementById("tableContainer")
    if (modelMetrics.length) {
        const data_table = document.createElement("table");
		data_table.setAttribute("id", "model_metrics_table")
		const table_header = document.createElement("thead");
        const table_header_row = document.createElement("tr");

        for (var column_key in modelMetrics[0]) {
            console.log(column_key)
            const new_header = document.createElement("th")
            const header_text = document.createTextNode(column_key);
            new_header.setAttribute("id", "column_"+column_key)
            new_header.appendChild(header_text)
            table_header_row.appendChild(new_header)
        }
		table_header.appendChild(table_header_row)
        const table_body = document.createElement("tbody");
        for (let i = 0; i < modelMetrics.length; i += 1) {
			const table_row = document.createElement("tr")
			// console.log(data[0])
			// const div_container = document.createElement("div")
			// div_container.setAttribute("id", "row_div")
			for (let col in modelMetrics[i]) {
				console.log(modelMetrics[i][col])
                const table_cell = document.createElement("td")
				const cell_text = document.createTextNode(modelMetrics[i][col]);
				table_cell.appendChild(cell_text);
				// div_container.appendChild(table_cell);
				table_row.appendChild(table_cell);
            }
           table_body.appendChild(table_row); 
        }


        data_table.appendChild(table_header);
		data_table.appendChild(table_body);
        // let table_container = document.getElementById("tableContainer")
		table_container.appendChild(data_table);
	}

	// if (data3.length) {
	// 	const data_table = document.createElement("table");
	// 	data_table.setAttribute("id", "table_step3")
	// 	const table_header = document.createElement("thead");
	// 	const table_header_row = document.createElement("tr");
	// 	const header_1 = document.createElement("th")
	// 	const header_text_1 = document.createTextNode("Combination of Important Items");
	// 	header_1.setAttribute("id", "step3_column1")
	// 	const header_2 = document.createElement("th")
	// 	const header_text_2 = document.createTextNode("Weights from LASSO");
	// 	header_2.setAttribute("id", "step3_column2")

	// 	header_1.appendChild(header_text_1);
	// 	header_2.appendChild(header_text_2);
	// 	table_header_row.appendChild(header_1)
	// 	table_header_row.appendChild(header_2)
	// 	table_header.appendChild(table_header_row)
	// 	const table_body = document.createElement("tbody");

	// 	for (let i = 0; i < data3.length; i += 1) {
	// 		const table_row = document.createElement("tr")
	// 		// console.log(data[0])
	// 		// const div_container = document.createElement("div")
	// 		// div_container.setAttribute("id", "row_div")
	// 		for (let col in data3[i]) {
	// 			console.log(data3[i][col])
	// 			const table_cell = document.createElement("td")
	// 			const cell_text = document.createTextNode(data3[i][col]);
	// 			table_cell.appendChild(cell_text);
	// 			// div_container.appendChild(table_cell);
	// 			table_row.appendChild(table_cell);
	// 		}
	// 		// div_container)
	// 		// output = data.map((row, i) => (
	// 		// 	<tr key={i}>
	// 		// 		<td>{document.createTextNode(row.important_combo)}</td>
	// 		// 		<td>{document.createTextNode(row.combo_length)}</td>
	// 		// 		<td>{document.createTextNode(row.pos_count)}</td>
	// 		// 		<td>{document.createTextNode(row.neg_count)}</td>
	// 		// 	</tr>
	// 		// ))
	// 		table_body.appendChild(table_row);
	// 		output = ""
	// 	}
		
	// 	data_table.appendChild(table_header);
	// 	data_table.appendChild(table_body);
	// 	document.body.appendChild(data_table);

	// }
	return (
		<div>
			<div class="tableContainer" id="tableContainer"></div>
            {/* <p>{output}</p> */}
			{/* [list of models + LASSO with feature selection] */}
        </div>
	);
};

export default Step4;
