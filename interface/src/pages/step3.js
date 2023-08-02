import React, {useState, useEffect} from 'react'
import $ from 'jquery';
import { useNavigate } from "react-router-dom";

const Step3 = () => {
	const table_element = document.getElementById("combo_table")
	if (table_element) {
		table_element.remove()
	}
	const table3_element = document.getElementById("table_step3")
	if (table3_element) {
		table3_element.remove()
	}
	const [data3, setData3] = useState({}) 
	const [modelMetrics, setModelMetrics] = useState({}) 
	const [stepStatus, setStepStatus] = useState(false) 
	const navigate = useNavigate();
    // useEffect(() => {
    // // Using fetch to fetch the api from
    // // flask server it will be redirected to proxy
    // fetch("/step3").then((res) =>
    //     res.json().then((data_in) => {
    //         // Setting a data from api
    //         setData3(data_in);
    //         console.log(data_in)
    //     })
    //     );
    // }, []);
    useEffect(() => {
        // Using fetch to fetch the api from
        // flask server it will be redirected to proxy
		console.log(stepStatus)
		// if (stepStatus == false) {
		fetch("/step4_data").then((res) =>
			res.json().then((data_in) => {
				// Setting a data from api
				// setModelMetrics(data_in);
				console.log(data_in[0])
				setStepStatus(true)
				let chosen_model = data_in[0]
				for (let m_dict in data_in) {
					console.log(data_in[m_dict])
					if (data_in[m_dict]["accuracy"] > chosen_model["accuracy"]) {
						chosen_model = data_in[m_dict]
					} else if (data_in[m_dict]["accuracy"] == chosen_model["accuracy"]) {
						if (data_in[m_dict]["complexity"] < chosen_model["complexity"]) {
							chosen_model = data_in[m_dict]
						}
					}
				}
				setData3(chosen_model);
				
			})
			);
        }, []);

	console.log(data3)
	var output = "Loading learned weights ..."
	console.log(stepStatus)

	if (stepStatus) {
		console.log("???")
		// navigate("/step3_model_selected", {state: {model_info: [data3]}});
		const data_table = document.createElement("table");
		data_table.setAttribute("id", "table_step3")
		const table_header = document.createElement("thead");
        const table_header_row = document.createElement("tr");
        // let hover_tracker = {}
        // let table_container = document.getElementById("tableContainer")
        const container_element = document.getElementById("step3container")

		for (var column_key in data3[0]) {
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
        for (let i = 0; i < data3.length; i += 1) {
			const table_row = document.createElement("tr")
			// console.log(data[0])
			// const div_container = document.createElement("div")
			// div_container.setAttribute("id", "row_div")
			let col_index = 0
			for (let col in data3[i]) {
				// console.log(trainingData[i][col])
                const table_cell = document.createElement("td")
				let new_text_node = data3[i][col]
				if (col_index == 0) {
					console.log(data3[i][col])
					let combo_list = data3[i][col].split("∧")
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
		document.body.appendChild(data_table);

		for (var column_key in data3[0]) {
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
		// const header_text_1 = document.createTextNode("Combination of Important Items");
		// header_1.setAttribute("id", "step3_column1")
		// const header_2 = document.createElement("th")
		// const header_text_2 = document.createTextNode("Weights from LASSO");
		// header_2.setAttribute("id", "step3_column2")

		// header_1.appendChild(header_text_1);
		// header_2.appendChild(header_text_2);
		// table_header_row.appendChild(header_1)
		// table_header_row.appendChild(header_2)
		// table_header.appendChild(table_header_row)
		// const table_body = document.createElement("tbody");

		// for (let i = 0; i < data3.length; i += 1) {
		// 	const table_row = document.createElement("tr")
		// 	// console.log(data[0])
		// 	// const div_container = document.createElement("div")
		// 	// div_container.setAttribute("id", "row_div")
		// 	for (let col in data3[i]) {
		// 		console.log(data3[i][col])
		// 		const table_cell = document.createElement("td")
		// 		const cell_text = document.createTextNode(data3[i][col]);
		// 		table_cell.appendChild(cell_text);
		// 		// div_container.appendChild(table_cell);
		// 		table_row.appendChild(table_cell);
		// 	}
			// div_container)
			// output = data.map((row, i) => (
			// 	<tr key={i}>
			// 		<td>{document.createTextNode(row.important_combo)}</td>
			// 		<td>{document.createTextNode(row.combo_length)}</td>
			// 		<td>{document.createTextNode(row.pos_count)}</td>
			// 		<td>{document.createTextNode(row.neg_count)}</td>
			// 	</tr>
			// ))
			// table_body.appendChild(table_row);
		// 	output = ""
		// }
		
		// data_table.appendChild(table_header);
		// data_table.appendChild(table_body);
		// document.body.appendChild(data_table);

	}

	const displayBestModel = async () => {
		// const file = e.target.files[0];
		// console.log(model_in)
		// if (model_in) {
			// console.log(model_in)
			// navigate("/step3_model_selected", {state: {model: model_in}});
		const data = new FormData();
		data.append('model_selected', data3["Model Name"]);
	// 	console.log(data)
		let response = await fetch('/step4_display_selected_model',
			{
			method: 'post',
			body: data,
			}
		);
		let res = await response.json();
		console.log(res.return)
		navigate("/step3_model_selected", {state: {model_info: res.return}});
		if (res.status !== 1){
			alert('Error selecting feature');
		}
		// }
	}; 
	return (
		<div>
			<div id = "step3container">
				
			</div>
			{/* <div class="loading">
				<p>{output}</p>
			</div> */}
			<button onClick={displayBestModel}>Click here to display weights from the "best" model</button>
		</div>
		
	);
};

export default Step3;
