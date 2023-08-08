import React, {useState, useEffect} from 'react'
import $ from 'jquery';
import {useLocation} from 'react-router-dom';

const Step8_model_selected = ({route,navigate}) => {
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
    
        setSelectedModelData(location.state.model_info)
    }, []);


    var output = "Loading learned weights ..."

    var model_names = {"Lasso": "Lasso", "SVM": "Support Vector Machine", "RF": "Random Forest", "DT2": "Decision Tree (depth = 2)", "DT3": "Decision Tree (depth = 3)", "DT5": "Decision Tree (depth = 5)", "DT10": "Decision Tree (depth = 10)", "LR2": "Logistic Regression", "PT": "Perceptron", "NB": "Gaussian Naive Bayes", "LassoFeatureSelection": "Lasso with Feature Selection"}


    if (selectedModelData) {
        console.log(selectedModelData)
		const data_table = document.createElement("table");
		data_table.setAttribute("id", "table_step3")
		const table_header = document.createElement("thead");
        const table_header_row = document.createElement("tr");

        const container_element = document.getElementById("step8container")

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

        let column_hover_texts = {"Data": "Testing data", "Prediction": "Model prediction: 0 means a negative classification and 1 means a positive classification", "Score": "The probability for each test data point is the probability that it belongs to the positive class. Therefore a probability score greater than 0.5 leads to a positive classification, and a probability score less than 0.5 leads to a negative classification"}

		for (var column_key in selectedModelData[0]) {

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
	
	return (
		<div>
			<div id = "step8container">
		
			</div>
			<div class="loading">
			</div>
            <div class="step8explanations">
                Shown below are the prediction scores generated by the <b>{model_names[location.state.model_name]}</b> model.
            </div>
		</div>
		
	);
};

export default Step8_model_selected;
