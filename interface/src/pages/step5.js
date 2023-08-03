import React, { useState, useEffect } from 'react';
import $ from 'jquery';

const Step5 = () => {
	const table_element = document.getElementById("combo_table")
	if (table_element) {
		table_element.remove()
	}
	const table3_element = document.getElementById("table_step3")
	if (table3_element) {
		table3_element.remove()
	}

	// const features_set = ["feature1", "feature2", "feature3", "feature4", "feature5", "feature6", "feature1", "feature2", "feature3", "feature4", "feature5", "feature6"]

	const [featuresList, setFeaturesList] = useState({})
	const [step5Status, setStep5Status] = useState(false) 
	// const [reformatted, setReformatted] = useState(false) 
	
	useEffect(() => {
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
				// let reformatted_combos = []
				// for (let combo in featuresList) {
				// 	console.log(featuresList[combo])
				// 	let combo_list = featuresList[combo].split("∧")
				// 	console.log(combo_list)
				// 	let new_feature_str = ""
				// 	for (let j = 0; j < combo_list.length; j += 1) {
				// 		console.log(combo_list[j])
				// 		let feature_detail = combo_list[j].split("_")
				// 		console.log(feature_detail)
				// 		if (feature_detail.length > 1) {
				// 			let feature_str = feature_detail[1].trim() + " " + feature_detail[0].trim()
				// 			console.log(feature_str)
				// 			if (j < combo_list.length - 1) {
				// 				new_feature_str += '"' + feature_str + '" and '
				// 			} else {
				// 				new_feature_str += '"' + feature_str + '"'
				// 			}
							
				// 		} else {
				// 			new_feature_str += '"' + feature_detail[0] + '"'
				// 		}
						
				// 	}
				// 	reformatted_combos.push(new_feature_str)
				// 	console.log(reformatted_combos)
					
				// }
				// setFeaturesList(reformatted_combos);
			})
			);
	
        }, []);

	// if (step5Status) {
	// 	console.log("ready")
	// 	let reformatted_combos = []
	// 	for (let combo in featuresList) {
	// 		console.log(featuresList[combo])
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
	// 				new_feature_str += '"' + feature_detail[0] + '"'
	// 			}
				
	// 		}
	// 		reformatted_combos.push(new_feature_str)
	// 		console.log(reformatted_combos)
			
	// 	}

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
				if (res.status !== 1){
					alert('Error selecting feature');
				}
			}
		}; 

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
			<div>
				<form method='post' action='/user_feature_selection' class="">
					<div class="featuresContainer">
						{(step5Status) ? featuresList.map(x =>
							// <label>
								// <input type="button" id='startDate' name={'startDate'+x} value={x} onClick={() => featureSelected(x)}/>
							// {/* </label> */}
							<div id='featureSelect' class="featureOption stepDivBackground" name={'featureSelect'+x} value={x} onClick={() => featureSelected(x)}>{x}</div>
						) : ""}
					</div>
					
                    
                    {/* <input type='submit' value='submit' /> */}
                </form>
            </div>
			{/* <p>{displayData}</p> */}
			{/* <button onClick={submitData}> testing</button> */}
			{/* <p>{data_select}</p> */}
		</div>
	);
};

export default Step5
;
