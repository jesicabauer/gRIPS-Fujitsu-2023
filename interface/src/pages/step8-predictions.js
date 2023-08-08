import React, {useState, useEffect} from 'react'
import $ from 'jquery';
import {useLocation} from 'react-router-dom';

const Step8_model_predictions = ({route,navigate}) => {
    const location = useLocation();


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

    const [selectedModelData, setSelectedModelData] = useState({}) 
    useEffect(() => {
        // Using fetch to fetch the api from
        // flask server it will be redirected to proxy
        fetch("/step4_display_selected_model").then((res) =>
            res.json().then((data_in) => {
                // Setting a data from api
                setSelectedModelData(data_in);
                console.log(data_in)
            })
            );
    }, []);

    console.log(selectedModelData.length)
    var output = "Loading learned weights ..."

    if (selectedModelData.length) {
        console.log(selectedModelData)
		const data_table = document.createElement("table");
		data_table.setAttribute("id", "table_step3")
		const table_header = document.createElement("thead");
        const table_header_row = document.createElement("tr");

        const container_element = document.getElementById("step3container")

		for (var column_key in selectedModelData[0]) {
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
        for (let i = 0; i < selectedModelData.length; i += 1) {
			const table_row = document.createElement("tr")

			let col_index = 0
			for (let col in selectedModelData[i]) {

                const table_cell = document.createElement("td")
				let new_text_node = selectedModelData[i][col]
				if (col_index == 0) {
					console.log(selectedModelData[i][col])
					let combo_list = selectedModelData[i][col].split("∧")
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

                if (col == "Score") {
                    new_text_node = new_text_node.toFixed(2)
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

		for (var column_key in selectedModelData[0]) {

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
	
	return (
		<div>
			<div id = "step8container">
			</div>
			<div class="loading">
			</div>
		</div>
		
	);
};

export default Step8_model_predictions;
