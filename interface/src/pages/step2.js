import React, {useState, useEffect} from 'react'
import $ from 'jquery';

const Step2 = () => {
	const table_element = document.getElementById("combo_table")
	if (table_element) {
		table_element.remove()
	}
	const table3_element = document.getElementById("table_step3")
	if (table3_element) {
		table3_element.remove()
	}

	const updated_weights_table_element = document.getElementById("step6_updated_weights")
	if (updated_weights_table_element) {
		updated_weights_table_element.remove()
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
			
			let col_index = 0
			for (let col in data[i]) {
				console.log(data[i][col])
				const table_cell = document.createElement("td")
				let new_text_node = data[i][col]
				if (col_index == 0) {
				
					let combo_list = data[i][col].split("∧")
					console.log(combo_list)
					let new_feature_str = ""
					for (let j = 0; j < combo_list.length; j += 1) {
						console.log(combo_list[j])
						let feature_detail = combo_list[j].split("_")
						console.log(feature_detail)
						if (feature_detail.length > 1) {
							let feature_str = feature_detail[1].trim() + " " + feature_detail[0].trim()
							console.log(feature_str)
							if (j < combo_list.length - 1) {
								new_feature_str += '"' + feature_str + '" and '
							} else {
								new_feature_str += '"' + feature_str + '"'
							}
							
						} else {
							if (j < combo_list.length - 1) {
								new_feature_str += '"' + feature_detail[0].trim() + '" and '
							} else {
								new_feature_str += '"' + feature_detail[0].trim() + '"'
							}
							
						}
						
					}
					new_text_node = new_feature_str
				}
				const cell_text = document.createTextNode(new_text_node);
				table_cell.appendChild(cell_text);
			
				table_row.appendChild(table_cell);
				col_index += 1
			}
		
			table_body.appendChild(table_row);
			output = ""
		}
		
		data_table.appendChild(table_header);
		data_table.appendChild(table_body);
		document.body.appendChild(data_table);

		let columnHeader1 = document.getElementById("column1")
		columnHeader1.addEventListener("mouseover", function(e) {

			$('#header1Hover').css({
				display: 'block',
				left: e.pageX+10,
				top: e.pageY,
				position: 'absolute',
				width: '10rem',
				height: 'auto',
				background: 'black',
				color: 'white',
				textAlign: 'center',
				padding: '1rem'
				
			})
		})

		columnHeader1.addEventListener("mouseout", function(e) {
			$('#header1Hover').css({
				display: 'None',
			})
		})

		let columnHeader2 = document.getElementById("column2")
		columnHeader2.addEventListener("mouseover", function(e) {
			console.log(e.pageX+20)
			$('#header2Hover').css({
				display: 'block',
				left: e.pageX+10,
				top: e.pageY,
				position: 'absolute',
				width: '10rem',
				height: 'auto',
				background: 'black',
				color: 'white',
				textAlign: 'center',
				padding: '1rem'
				
			})
		})

		columnHeader2.addEventListener("mouseout", function(e) {
			$('#header2Hover').css({
				display: 'None',
			})
		})

		let columnHeader3 = document.getElementById("column3")
		columnHeader3.addEventListener("mouseover", function(e) {
			console.log(e.pageX+20)
			$('#header3Hover').css({
				display: 'block',
				left: e.pageX+10,
				top: e.pageY,
				position: 'absolute',
				width: '10rem',
				height: 'auto',
				background: 'black',
				color: 'white',
				textAlign: 'center',
				padding: '1rem'
				
			})
		})

		columnHeader3.addEventListener("mouseout", function(e) {
			$('#header3Hover').css({
				display: 'None',
			})
		})

		let columnHeader4 = document.getElementById("column4")
		columnHeader4.addEventListener("mouseover", function(e) {
			$('#header4Hover').css({
				display: 'block',
				left: e.pageX+10,
				top: e.pageY,
				position: 'absolute',
				width: '10rem',
				height: 'auto',
				background: 'black',
				color: 'white',
				textAlign: 'center',
				padding: '1rem'
				
			})
		})

		columnHeader4.addEventListener("mouseout", function(e) {
			$('#header4Hover').css({
				display: 'None',
			})
		})

	}
	

    return (
		<div>
			<div id="header1Hover">Feature combinations deemed important from Wide Learning, based on combination's length, number of positive classifications and number of negative classifications.</div>
			<div id="header2Hover">Length of the combinations. The maximum length shown in this table is 3.</div>
			<div id="header3Hover">Number of positive classifications for each combination.</div>
			<div id="header4Hover">Number of negative classifications for each combination.</div>
			<p id="explanationStep2">Wide Learning generates all possible combinations of variables. The combinations in this table are the most important combinations of features to determine whether or not an animal is a mammal. The importance of a combination is measured by the length of the combination and the number of positive and negative occurrences for the animals in the training dataset that have that combination of features. The table below will only show feature combinations with a maximum length of three, however, important feature combinations that are longer than three may exist.</p>
        <div class="loading">
            <p>{output}</p>
        </div>
		</div>
    )

};

export default Step2;
