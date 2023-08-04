import React, { useState, useEffect } from 'react';
import $ from 'jquery';
import { useNavigate } from "react-router-dom";

const Step5 = () => {
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

	// const features_set = ["feature1", "feature2", "feature3", "feature4", "feature5", "feature6", "feature1", "feature2", "feature3", "feature4", "feature5", "feature6"]

	const [featuresList, setFeaturesList] = useState({})
	const [weights_info, setWeightsInfo] = useState({})
	const [step5Status, setStep5Status] = useState(false) 
	const [selectedFeature, setSelectedFeature] = useState("")
	const [reformattedStatus, setReformattedStatus] = useState(false) 
	// const [reformatted, setReformatted] = useState(false) 
	const navigate = useNavigate();
	
	useEffect(() => {
		document.getElementById("step5Div").classList.add("onclickColor")
		document.getElementById("step5Div").classList.remove("stepDivBackground")
		
        // Using fetch to fetch the api from
        // flask server it will be redirected to proxy
		// console.log(stepStatus)
		// if (stepStatus == false) {
		fetch("/step5_features_selection").then((res) =>
			res.json().then((data_in) => {
				// Setting a data from api
				setFeaturesList(data_in);
				console.log(data_in)
				setStep5Status(true)
				console.log("ready")
			
			})
			);
			// if (!reformattedStatus) {
			// 	let reformatted_combos = []
			// 	// console.log(data_in)
			// 	for (let combo in featuresList) {
			// 		// console.log("in loop")
			// 		// console.log(combo)
			// 		let combo_list = featuresList[combo].split("∧")
			// 		console.log(combo_list)
			// 		let new_feature_str = ""
			// 		for (let j = 0; j < combo_list.length; j += 1) {
			// 			console.log(combo_list[j])
			// 			let feature_detail = combo_list[j].split("_")
			// 			console.log(feature_detail)
			// 			if (feature_detail.length > 1) {
			// 				let feature_str = feature_detail[1].trim() + " " + feature_detail[0].trim()
			// 				console.log(feature_str)
			// 				if (j < combo_list.length - 1) {
			// 					new_feature_str += '"' + feature_str + '" and '
			// 				} else {
			// 					new_feature_str += '"' + feature_str + '"'
			// 				}
							
			// 			} else {
			// 				if (j < combo_list.length - 1) {
			// 					new_feature_str += '"' + feature_detail[0].trim() + '" and '
			// 				} else {
			// 					new_feature_str += '"' + feature_detail[0].trim() + '"'
			// 				}
							
			// 			}
						
			// 		}
			// 		reformatted_combos.push(new_feature_str)
			// 		console.log(reformatted_combos)
					
			// 	}
			// 	setFeaturesList(reformatted_combos);
			// 	setReformattedStatus(true);
			// }
			
	
        }, []);

	// if (step5Status) {
	// 	console.log("ready")
	// 	let reformatted_combos = []
	// 		// console.log(data_in)
	// 		for (let combo in featuresList) {
	// 			// console.log("in loop")
	// 			// console.log(combo)
	// 			let combo_list = featuresList[combo].split("∧")
	// 			console.log(combo_list)
	// 			let new_feature_str = ""
	// 			for (let j = 0; j < combo_list.length; j += 1) {
	// 				console.log(combo_list[j])
	// 				let feature_detail = combo_list[j].split("_")
	// 				console.log(feature_detail)
	// 				if (feature_detail.length > 1) {
	// 					let feature_str = feature_detail[1].trim() + " " + feature_detail[0].trim()
	// 					console.log(feature_str)
	// 					if (j < combo_list.length - 1) {
	// 						new_feature_str += '"' + feature_str + '" and '
	// 					} else {
	// 						new_feature_str += '"' + feature_str + '"'
	// 					}
						
	// 				} else {
	// 					if (j < combo_list.length - 1) {
	// 						new_feature_str += '"' + feature_detail[0].trim() + '" and '
	// 					} else {
	// 						new_feature_str += '"' + feature_detail[0].trim() + '"'
	// 					}
						
	// 				}
					
	// 			}
	// 			reformatted_combos.push(new_feature_str)
	// 			console.log(reformatted_combos)
	// 			setFeaturesList(reformatted_combos)
				
	// 		}
	// }

	const format_combo = (combo_in) => {
		let combo_list = combo_in.split("∧")
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
		return new_feature_str

	}

	// 	// if (reformatted) {

	// 	// }
	// 	// setStep5Status(reformatted_combos)
	// }

	

	// const [selection, setSelection] = useState()
	// const submitData = async () => {
	// 	console.log("here")
	// 	const the_data = {
	// 		testinig: "testing!"
	// 	}

	// 	const result = await fetch("/step4_select", {
	// 		method: 'POST',
	// 		headers: {
	// 			'Content-Type': 'application/json',

	// 		},
	// 		body: JSON.stringify(the_data)
	// 	})

	// 	console.log(result)
	// 	const json_result = await result.json()
	// 	console.log(json_result)
	// 	setSelection(result.testinig)
	// }

	// const [data_select, setData] = useState({}) 
	// useEffect(() => {
	// // Using fetch to fetch the api from
	// // flask server it will be redirected to proxy
	// 	fetch("/step4_select").then((res) =>
	// 		res.json().then((data_in) => {
	// 			// Setting a data from api
	// 			setData(data_in);
	// 			console.log(data_in)
	// 		})
	// 		);
	// }, []);

	// // const displayData = () => {
		
		
	// // }
	

	// console.log(data_select)
	// onSubmit={(event) => event.preventDefault()

		const featureSelected = async (feature_in) => {
			// const file = e.target.files[0];
			console.log(feature_in)
			if (feature_in) {
				setSelectedFeature(feature_in)
				const data = new FormData();
				data.append('feature_selected', feature_in);
			// 	console.log(data)
				let response = await fetch('/user_feature_selection',
					{
					method: 'post',
					body: data,
					}
				);
				let res = await response.json();
				console.log(res.return)

				navigate("/step6", {state: {weights_info: res.return, addFeature: feature_in}});
				setWeightsInfo(res.return)
				if (res.status !== 1){
					alert('Error selecting feature');
				}
			}
		}; 

		var output = "Loading updated weights ..."

		let table_container = document.getElementById("tableContainer")
		if (weights_info.length) {
			console.log("ready to create weights table")
			const data_table = document.createElement("table");
			data_table.setAttribute("id", "step6_updated_weights")
			const table_header = document.createElement("thead");
			const table_header_row = document.createElement("tr");
			// let hover_tracker = {}
			// let table_container = document.getElementById("tableContainer")
			const container_element = document.getElementById("step6container")

			for (var column_key in weights_info[0]) {
				// console.log(column_key)
				const new_header = document.createElement("th")
				const header_text = document.createTextNode(column_key);
				let column_str = column_key.replace(/[^a-z0-9]/gi, '').replace(/\s/g, '')
				new_header.setAttribute("id", "column_"+column_str)
				new_header.appendChild(header_text)
				table_header_row.appendChild(new_header)
			}
			table_header.appendChild(table_header_row)
			const table_body = document.createElement("tbody");
			for (let i = 0; i < weights_info.length; i += 1) {
				const table_row = document.createElement("tr")
				// console.log(data[0])
				// const div_container = document.createElement("div")
				// div_container.setAttribute("id", "row_div")
				let col_index = 0
				for (let col in weights_info[i]) {
					// console.log(trainingData[i][col])
					const table_cell = document.createElement("td")
					let new_text_node = weights_info[i][col]
					console.log(weights_info[i][col])
					console.log(selectedFeature)
					// if (weights_info[i][col] == selectedFeature) {
					// 	table_cell.classList.add("addedCombo")
					// }
					if (col_index == 0) {
						console.log(weights_info[i][col])
						let combo_list = weights_info[i][col].split("∧")
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
								new_feature_str += '"' + feature_detail[0] + '"'
							}
							
						}
						new_text_node = new_feature_str
					}

					if (col == "Weight") {
						new_text_node = new_text_node.toFixed(2)
					}
					
					const cell_text = document.createTextNode(new_text_node);
					table_cell.appendChild(cell_text);
					// div_container.appendChild(table_cell);
					table_row.appendChild(table_cell);
					col_index += 1
				}
			table_body.appendChild(table_row); 
			output = ""
			}
		
			data_table.appendChild(table_header);
			data_table.appendChild(table_body);
			// let table_container = document.getElementById("tableContainer")
			// document.body.appendChild(data_table);
			table_container.appendChild(data_table);

			for (var column_key in weights_info[0]) {
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

			}
		}

		// const selectedData = (x) => {
		// 	// e.preventDefault()
		// 	// setSelectedFeature()
		// 	console.log("???")
		// 	console.log(x)
		// 	let feature_name = document.getElementById("")
		// }

		// $("button").on("click", function() {
		// 	console.log("???")
		// 	var fired_button = $(this).val();
		// 	alert(fired_button);
		// 	console.log(selectedFeature)
		// 	setSelectedFeature(() => selectedFeature)
		// 	console.log(selectedFeature)
		// });

	return (
		<div>
			{/* <h1>{selection}</h1> */}
			<div id="step6container">

			</div>
			<div class="featureSelectionContainer">
				<div class="featureSelectionExplanations">The following is a list of some of the feature combinations from step 2 that were assigned a weight of 0 by Lasso and were therefore not included in the final model. By selecting one of these feature combinations, it will be reassigned a new nonzero weight. One of the feature combinations with a nonzero weight from the original Lasso model will be taken out of the model by reassigning it a weight of 0.</div>
				<form method='post' action='/user_feature_selection' class="">
					<div class="featuresContainer">
						{(step5Status) ? featuresList.map(x =>
							// <label>
								// <input type="button" id='startDate' name={'startDate'+x} value={x} onClick={() => featureSelected(x)}/>
							// {/* </label> */}
							<div id='featureSelect' class="featureOption stepDivBackground" name={'featureSelect'+x} value={x} onClick={() => featureSelected(x)}>{format_combo(x)}</div>
						) : ""}
					</div>
					
                    
                    {/* <input type='submit' value='submit' /> */}
                </form>
				{/* <div class="tableContainer" id="tableContainer">

				</div> */}
				
            </div>
			{/* <p>{displayData}</p> */}
			{/* <button onClick={submitData}> testing</button> */}
			{/* <p>{data_select}</p> */}
		</div>
	);
};

export default Step5
;
