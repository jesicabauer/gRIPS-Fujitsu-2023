import React, {useState, useEffect} from 'react'

const Step2 = () => {
	const table_element = document.getElementById("combo_table")
	if (table_element) {
		table_element.remove()
	}
	const [data, setData] = useState({}) 
    useEffect(() => {
    // Using fetch to fetch the api from
    // flask server it will be redirected to proxy
    fetch("/data").then((res) =>
        res.json().then((data_in) => {
            // Setting a data from api
            setData(data_in);
            console.log(data_in)
        })
        );
    }, []);

	console.log(data.length)
	var output = "Loading important combinations from Wide Learning ..."


	if (data.length) {
		const data_table = document.createElement("table");
		data_table.setAttribute("id", "combo_table")
		const table_header = document.createElement("thead");
		const table_header_row = document.createElement("tr");
		const header_1 = document.createElement("th")
		const header_text_1 = document.createTextNode("Combination of Important Items");
		header_1.setAttribute("id", "column1")
		const p_tooltip = document.createElement("div")
		const header_1_tooltip = document.createTextNode("tooltip")
		p_tooltip.appendChild(header_1_tooltip)
		p_tooltip.setAttribute("id", "tooltip1")
		const header_2 = document.createElement("th")
		const header_text_2 = document.createTextNode("Combination Length");
		header_2.setAttribute("id", "column2")
		const header_3 = document.createElement("th")
		const header_text_3 = document.createTextNode("Occurrences of POS");
		header_3.setAttribute("id", "column3")
		const header_4 = document.createElement("th")
		const header_text_4 = document.createTextNode("Occurrences of NEG");
		header_4.setAttribute("id", "column4")
		header_1.appendChild(header_text_1);
		header_1.appendChild(p_tooltip);
		header_2.appendChild(header_text_2);
		header_3.appendChild(header_text_3);
		header_4.appendChild(header_text_4);
		table_header_row.appendChild(header_1)
		table_header_row.appendChild(header_2)
		table_header_row.appendChild(header_3)
		table_header_row.appendChild(header_4)
		table_header.appendChild(table_header_row)
		const table_body = document.createElement("tbody");
		for (let i = 0; i < data.length; i += 1) {
			const table_row = document.createElement("tr")
			// console.log(data[0])
			// const div_container = document.createElement("div")
			// div_container.setAttribute("id", "row_div")
			for (let col in data[i]) {
				console.log(data[i][col])
				const table_cell = document.createElement("td")
				const cell_text = document.createTextNode(data[i][col]);
				table_cell.appendChild(cell_text);
				// div_container.appendChild(table_cell);
				table_row.appendChild(table_cell);
			}
			// div_container)
			// output = data.map((row, i) => (
			// 	<tr key={i}>
			// 		<td>{document.createTextNode(row.important_combo)}</td>
			// 		<td>{document.createTextNode(row.combo_length)}</td>
			// 		<td>{document.createTextNode(row.pos_count)}</td>
			// 		<td>{document.createTextNode(row.neg_count)}</td>
			// 	</tr>
			// ))
			table_body.appendChild(table_row);
			output = ""
		}
		
		data_table.appendChild(table_header);
		data_table.appendChild(table_body);
		document.body.appendChild(data_table);

	}
	
	// for (index = 0; index <)
    return (
        <div class="loading">
			<div id="hoverTip">tooltip</div>
            <p>{output}</p>
        </div>
    )
	// return (
	// 	<div>
	// 		<h1>Step2</h1>
	// 	</div>
	// );
};

export default Step2;
