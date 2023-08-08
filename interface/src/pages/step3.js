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

	const updated_weights_table_element = document.getElementById("step6_updated_weights")
	if (updated_weights_table_element) {
		updated_weights_table_element.remove()
	}
	
	const [data3, setData3] = useState({}) 
	const [modelMetrics, setModelMetrics] = useState({}) 
	const [stepStatus, setStepStatus] = useState(false) 
	const navigate = useNavigate();

    useEffect(() => {
        // Using fetch to fetch the api from
        // flask server it will be redirected to proxy
		console.log(stepStatus)
	
		fetch("/step4_data").then((res) =>
			res.json().then((data_in) => {
	
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

		const data_table = document.createElement("table");
		data_table.setAttribute("id", "table_step3")
		const table_header = document.createElement("thead");
        const table_header_row = document.createElement("tr");
    
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
		
			let col_index = 0
			for (let col in data3[i]) {
			
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

				table_row.appendChild(table_cell);
				col_index += 1
            }
           table_body.appendChild(table_row); 
           output = ""
        }

		data_table.appendChild(table_header);
		data_table.appendChild(table_body);
      
		document.body.appendChild(data_table);

		for (var column_key in data3[0]) {

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

	const displayBestModel = async () => {
	
		const data = new FormData();
		data.append('model_selected', data3["Model Name"]);
	
		let response = await fetch('/step4_display_selected_model',
			{
			method: 'post',
			body: data,
			}
		);
		let res = await response.json();
		console.log(res.return)
		navigate("/step3_model_selected", {state: {model_info: res.return, model_name: data3["Model Name"]}});
		if (res.status !== 1){
			alert('Error selecting feature');
		}
		// }
	}; 
	return (
		<div>
			<div id = "step3container">
				
			</div>
		
			<div class="step3explanations">
				After training various possible models (will show in <b>Step 4</b>), we show weights from the model that has the <b>highest training accuracy and lowest complexity</b> (referred to as "best" model). Click on the button below to display the learned weights.
			</div>
			<button id="step3_dsplay_button" onClick={displayBestModel}>Click here to display weights from the "best" model</button>
		</div>
		
	);
};

export default Step3;
