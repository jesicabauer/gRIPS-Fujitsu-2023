import React, {useState, useEffect} from 'react'
import $ from 'jquery';
import { useNavigate } from "react-router-dom";

const Step4 = () => {
	const table_element = document.getElementById("combo_table")
	if (table_element) {
		table_element.remove()
	}
	const table3_element = document.getElementById("table_step3")
	if (table3_element) {
		table3_element.remove()
	}
	const model_metrics_table_element = document.getElementById("model_metrics_table")
	if (model_metrics_table_element) {
		model_metrics_table_element.remove()
	}

	const updated_weights_table_element = document.getElementById("step6_updated_weights")
	if (updated_weights_table_element) {
		updated_weights_table_element.remove()
	}

	const [modelMetrics, setModelMetrics] = useState({}) 
	const [stepStatus, setStepStatus] = useState(false) 
	const navigate = useNavigate();

	var model_names = {"Lasso": "Lasso", "SVM": "Support Vector Machine", "RF": "Random Forest", "DT2": "Decision Tree (depth = 2)", "DT3": "Decision Tree (depth = 3)", "DT5": "Decision Tree (depth = 5)", "DT10": "Decision Tree (depth = 10)", "LR2": "Logistic Regression", "PT": "Perceptron", "NB": "Gaussian Naive Bayes"}
	
    useEffect(() => {
        // Using fetch to fetch the api from
        // flask server it will be redirected to proxy
		console.log(stepStatus)

		fetch("/step4_data").then((res) =>
			res.json().then((data_in) => {
				// Setting a data from api
				setModelMetrics(data_in);
				console.log(data_in)
				setStepStatus(true)
			})
			);
	
        }, []);

    console.log(modelMetrics)
    console.log(modelMetrics.length)
	var output = "Loading model options and metrics ..."

	let table_container = document.getElementById("tableContainer")
	const models_set = []
    if (modelMetrics.length) {

        const data_table = document.createElement("table");
		data_table.setAttribute("id", "model_metrics_table")
		const table_header = document.createElement("thead");
        const table_header_row = document.createElement("tr");

		let display_columns = ["Model Name", "accuracy", "complexity"]

		const container_element = document.getElementById("step4container")
        for (var column_key in modelMetrics[0]) {
			if (display_columns.includes(column_key)) {
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
        for (let i = 0; i < modelMetrics.length; i += 1) {
			const table_row = document.createElement("tr")

			for (let col in modelMetrics[i]) {
				if (display_columns.includes(col)) {

					let text_node = modelMetrics[i][col]
					if (col == "Model Name") {
						console.log(modelMetrics[i][col])
						if (modelMetrics[i][col] != "NB") {
							models_set.push(modelMetrics[i][col])
						}
						text_node = model_names[modelMetrics[i][col]]
						
						
					} else {
						text_node = text_node.toFixed(2)
					}
					let cell_text = document.createTextNode(text_node);
					const table_cell = document.createElement("td")
					
					table_cell.appendChild(cell_text);
					table_row.appendChild(table_cell);
				}
            }
           table_body.appendChild(table_row); 
        }


        data_table.appendChild(table_header);
		data_table.appendChild(table_body);

		table_container.appendChild(data_table);
		output = ""

		let column_hover_texts = {"Model Name": "Model considered in the Rashomon Set", "accuracy": "Accuracy divides data given as training data, using one as training data and the other as test data, and evaluates how well the model trained on the training data predicts the test data, i.e., the percentage of correct answers", "complexity": "The higher the value, the more complexity the model, according to Rademacher Complexity"}

		for (var column_key in modelMetrics[0]) {

			if (display_columns.includes(column_key)) {
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

	const modelSelected = async (model_in) => {
		if (model_in) {
			const data = new FormData();
			data.append('model_selected', model_in);
			let response = await fetch('/step4_display_selected_model',
				{
				method: 'post',
				body: data,
				}
			);
			let res = await response.json();
			console.log(res.return)
			navigate("/step3_model_selected", {state: {model_info: res.return, model_name: model_in}});
			if (res.status !== 1){
				alert('Error selecting feature');
			}
		}
	}; 

	const reformat_model_name = (name_in) => {
		return model_names[name_in]
	}

	const displayChartButton = () => {
		navigate("/step4-chart");
	}


	return (
		<div>
			<div id="step4container">
				
			</div>
			<p>{output}</p>
			<div class="rashomonSetExplanation">Shown below are models considered in the Rashomon Set, which contains models with similar accuracy. Click on a model from the list on the right to display weights for relevant feature combinations.</div>
			<img id="step4chart" src="/step4Chart.png" alt="complexity chart" />

			<div class="modelContainer">
				<div class="tableContainer" id="tableContainer"></div>

				<div class="potentialList">
					{models_set.map(x =>
						<div id='modelSelect' class="featureOption stepDivBackground" name={'modelSelect'+x} value={x} onClick={() => modelSelected(x)}>{reformat_model_name(x)}</div>
					)}
				</div>
				

			</div>
			
        </div>
	);
};

export default Step4;
