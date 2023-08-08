import React, { useState, useEffect } from 'react';
import {useLocation} from 'react-router-dom';
import $ from 'jquery';
import { useNavigate } from "react-router-dom";


const Step6 = () => {
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

	const location = useLocation();
	const [selectedModelWeightsData, setSelectedModelWeightsData] = useState({})
	const [selectedFeature, setSelectedFeature] = useState("")
	const navigate = useNavigate();

	useEffect(() => {
        
		document.getElementById("step6Div").classList.add("onclickColor");
		document.getElementById("step6Div").classList.remove("stepDivBackground")
		document.getElementById("step5Div").classList.add("stepDivBackground")
        setSelectedModelWeightsData(location.state.weights_info)
    }, []);

	var output = "Loading updated weights ..."

	if (selectedModelWeightsData.length) { 
		const data_table = document.createElement("table");
		data_table.setAttribute("id", "step6_updated_weights")
		const table_header = document.createElement("thead");
        const table_header_row = document.createElement("tr");
        
		let no_display_columns = ["Old"]
        const container_element = document.getElementById("step6container")

		for (var column_key in selectedModelWeightsData[0]) {
			if (!no_display_columns.includes(column_key)) {
				const new_header = document.createElement("th")
				const header_text = document.createTextNode(column_key);
				let column_str = column_key.replace(/[^a-z0-9]/gi, '').replace(/\s/g, '')
				new_header.setAttribute("id", "column_"+column_str)
				new_header.appendChild(header_text)
				table_header_row.appendChild(new_header)
			}
		}
		table_header.appendChild(table_header_row)
		const table_body = document.createElement("tbody");
		for (let i = 0; i < selectedModelWeightsData.length; i += 1) {
			const table_row = document.createElement("tr")
		
			let col_index = 0
			for (let col in selectedModelWeightsData[i]) {
				if (!no_display_columns.includes(col)) {
		
					const table_cell = document.createElement("td")
					let new_text_node = selectedModelWeightsData[i][col]
					
					if (col_index == 0) {
						console.log(selectedModelWeightsData[i][col])
						console.log(selectedFeature)
						if (selectedModelWeightsData[i][col] == location.state.addFeature) {
							table_cell.classList.add("addedCombo")
						}
						console.log(selectedModelWeightsData[i])
						if (selectedModelWeightsData[i]["Old"] == true) {
				
								table_cell.classList.add("removedCombo")

						}
						console.log(selectedModelWeightsData[i][col])
						let combo_list = selectedModelWeightsData[i][col].split("∧")
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
					
					if (col == "Weight") {
						new_text_node = new_text_node.toFixed(2)
					}
					const cell_text = document.createTextNode(new_text_node);
					table_cell.appendChild(cell_text);
					table_row.appendChild(table_cell);
					col_index += 1
				}
			}
			
		table_body.appendChild(table_row); 
		output = ""
		}
	
		data_table.appendChild(table_header);
		data_table.appendChild(table_body);
		document.body.appendChild(data_table);

		let column_hover_texts = {"Feature Combination": "Combinations important for model", "Weight": "A higher numerical value indicates a more important feature. The feature combination with a 0 weight got replaced by the user selected combination"}


		for (var column_key in selectedModelWeightsData[0]) {
			if (!no_display_columns.includes(column_key)) {

				const new_hover = document.createElement("div")
				let column_hover_str = column_key.replace(/[^a-z0-9]/gi, '').replace(/\s/g, '')
				new_hover.setAttribute("id", "hover_"+column_hover_str)
				let new_hover_text = document.createTextNode(column_hover_texts[column_key])
				new_hover.classList.add("displayNone")
				new_hover.appendChild(new_hover_text)
				container_element.appendChild(new_hover)
				const get_header = document.getElementById("column_"+column_hover_str)
				let hover_key = "#hover_"+column_hover_str
				get_header.addEventListener("mouseover", function(e) {

			
					$(hover_key).css({
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

				get_header.addEventListener("mouseout", function(e) {
					$(hover_key).css({
						display: 'None',
					})
			})
		}

		}
	}

	const toStep5 = () => {
		navigate("/step5")
	}


	return (
		<div>
			<div id="step6container">
				
			</div>
			<p>{output}</p>
			<div class="step6explanation">The feature combination with a 0.00 weight was replaced by the feature selected by the user from Step 5.</div>
			<button id="step6selectAnotherButton" onClick={toStep5}>Select another feature combination</button>
		
		</div>
	);
};

export default Step6;
