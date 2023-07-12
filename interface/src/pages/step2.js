import React, {useState, useEffect} from 'react'

const Step2 = () => {
	const table_element = document.getElementById("combo_table")
	if (table_element) {
		table_element.remove()
	}
	const table3_element = document.getElementById("table_step3")
	if (table3_element) {
		table3_element.remove()
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
		// const explanation = document.createElement("div");
		// const explanation_text = document.createTextNode("Wide Learning generates all possible combinations of variables. The combinations in this table are the most important combinations of features to determine whether or not an animal is a mammal. The importance of a combination is measured by the length of the combination and the number of positive and negative occurrences for the animals in the training dataset that have that combination of features. This table (link to a larger version) only shows feature combinations with a maximum length of three, however, important feature combinations that are longer than three may exist.")
		// explanation.setAttribute("id", "explanationStep2")
		// explanation.appendChild(explanation_text)
		// document.body.appendChild(explanation)
		const data_table = document.createElement("table");
		data_table.setAttribute("id", "combo_table")
		const table_header = document.createElement("thead");
		// const table_tooltip_row = document.createElement("tr");
		// table_tooltip_row.setAttribute("id", "tooltipRow")
		// const tooltip_1 = document.createElement("th")
		// const tooltip_text_1 = document.createTextNode("Combination of Important Items");
		// tooltip_1.setAttribute("id", "tooltip1")
		// const tooltip_2 = document.createElement("th")
		// const tooltip_text_2 = document.createTextNode("Combination Length");
		// tooltip_2.setAttribute("id", "tooltip2")
		// const tooltip_3 = document.createElement("th")
		// const tooltip_text_3 = document.createTextNode("Occurrences of POS");
		// tooltip_3.setAttribute("id", "tooltip3")
		// const tooltip_4 = document.createElement("th")
		// const tooltip_text_4 = document.createTextNode("Occurrences of NEG");
		// tooltip_4.setAttribute("id", "tooltip4")
		// tooltip_1.appendChild(tooltip_text_1);
		// tooltip_2.appendChild(tooltip_text_2);
		// tooltip_3.appendChild(tooltip_text_3);
		// tooltip_4.appendChild(tooltip_text_4);
		// table_tooltip_row.appendChild(tooltip_1)
		// table_tooltip_row.appendChild(tooltip_2)
		// table_tooltip_row.appendChild(tooltip_3)
		// table_tooltip_row.appendChild(tooltip_4)
		// table_header.appendChild(table_tooltip_row)

		const table_header_row = document.createElement("tr");
		const header_1 = document.createElement("th")
		const header_text_1 = document.createTextNode("Combination of Important Items");
		header_1.setAttribute("id", "column1")
		const p_tooltip = document.createElement("div")
		const header_1_tooltip = document.createTextNode("Combinations deemed important based on 'length of combinations', 'number of positive classifications', and 'number of negative classifications'")
		p_tooltip.appendChild(header_1_tooltip)
		p_tooltip.setAttribute("id", "tooltip1")
		const header_2 = document.createElement("th")
		const header_text_2 = document.createTextNode("Combination Length");
		header_2.setAttribute("id", "column2")
		const p_tooltip2 = document.createElement("div")
		const header_2_tooltip = document.createTextNode("Length of combinations; maximum length is 3")
		p_tooltip2.appendChild(header_2_tooltip)
		p_tooltip2.setAttribute("id", "tooltip2")
		const header_3 = document.createElement("th")
		const header_text_3 = document.createTextNode("Occurrences of POS");
		header_3.setAttribute("id", "column3")
		const p_tooltip3 = document.createElement("div")
		const header_3_tooltip = document.createTextNode("Mammal classifications for each combination")
		p_tooltip3.appendChild(header_3_tooltip)
		p_tooltip3.setAttribute("id", "tooltip3")
		const header_4 = document.createElement("th")
		const header_text_4 = document.createTextNode("Occurrences of NEG");
		header_4.setAttribute("id", "column4")
		const p_tooltip4 = document.createElement("div")
		const header_4_tooltip = document.createTextNode("Non-mammal classifications for each combination")
		p_tooltip4.appendChild(header_4_tooltip)
		p_tooltip4.setAttribute("id", "tooltip4")
		header_1.appendChild(header_text_1);
		header_1.appendChild(p_tooltip);
		header_2.appendChild(header_text_2);
		header_2.appendChild(p_tooltip2);
		header_3.appendChild(header_text_3);
		header_3.appendChild(p_tooltip3);
		header_4.appendChild(header_text_4);
		header_4.appendChild(p_tooltip4);
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
		<div>
			<p id="explanationStep2">Wide Learning generates all possible combinations of variables. The combinations in this table are the most important combinations of features to determine whether or not an animal is a mammal. The importance of a combination is measured by the length of the combination and the number of positive and negative occurrences for the animals in the training dataset that have that combination of features. The table below will only show feature combinations with a maximum length of three, however, important feature combinations that are longer than three may exist.</p>
        <div class="loading">
            <p>{output}</p>
        </div>
		</div>
    )
	// return (
	// 	<div>
	// 		<h1>Step2</h1>
	// 	</div>
	// );
};

export default Step2;
