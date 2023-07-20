import React, { useState, useEffect } from 'react';
import $ from 'jquery';

const Step4 = () => {
	const table_element = document.getElementById("combo_table")
	if (table_element) {
		table_element.remove()
	}
	const table3_element = document.getElementById("table_step3")
	if (table3_element) {
		table3_element.remove()
	}

	const features_set = ["feature1", "feature2", "feature3", "feature4", "feature5", "feature6"]

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

	const [selectedFeature, setSelectedFeature] = useState("");
	console.log("here??")
	useEffect(() => {
		console.log("in use effect")
		if (selectedFeature) {
			console.log(selectedFeature)
			fetch("/step4_select", {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
	
				},
				body: JSON.stringify(selectedFeature)
			})
			.then((res) => {
				if (!res.ok) return Promise.reject(res);
				return res.json();
			  })
			  .then((data) => {
				// do something with data ¯\_(ツ)_/¯
				console.log("data??")
				console.log(data)
				fetch("/step4_select").then((res) =>
					res.json().then((data_in) => {
						// Setting a data from api
						// setData(data_in);
						console.log(data_in)
					})
					);
				}, [])
			  .catch(console.error);
		  }
		}, [selectedFeature]);

		// const selectedData = (x) => {
		// 	// e.preventDefault()
		// 	// setSelectedFeature()
		// 	console.log("???")
		// 	console.log(x)
		// 	let feature_name = document.getElementById("")
		// }

		function selectedData(featureButton) {
			if (featureButton) {
				console.log(featureButton.value)
			}
			
			
		}
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
				{/* <form method='post' action='/step4_select'> */}
					{features_set.map(x =>
						<button type="button" id='startDate' name='startDate' value={x} onClick={() => setSelectedFeature(x)}>{x}</button>
					)}
                    
                    <input type='submit' value='submit' />
                {/* </form> */}
            </div>
			{/* <p>{displayData}</p> */}
			{/* <button onClick={submitData}> testing</button> */}
			{/* <p>{data_select}</p> */}
		</div>
	);
};

export default Step4;
