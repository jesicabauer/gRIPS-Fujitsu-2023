import React, {useState, useEffect} from 'react'
import $ from 'jquery';
import {useLocation} from 'react-router-dom';
import { useNavigate } from "react-router-dom";

const Step3_model_selected = () => {
    // console.log(props.st)
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
    const navigate = useNavigate();
    useEffect(() => {
        // console.log(location.state.model)
        // Using fetch to fetch the api from
        // flask server it will be redirected to proxy
        // fetch("/step4_display_selected_model").then((res) =>
        //     res.json().then((data_in) => {
        //         // Setting a data from api
        //         setSelectedModelData(data_in);
        //         console.log(data_in)
                
        //     })
        //     );
        setSelectedModelData(location.state.model_info)
    }, []);

    // setSelectedModelData(location.state.model_info)
    // console.log(selectedModelData.length)
    var output = "Loading learned weights ..."

    var model_names = {"Lasso": "Lasso", "SVM": "Support Vector Machine", "RF": "Random Forest", "DT2": "Decision Tree (depth = 2)", "DT3": "Decision Tree (depth = 3)", "DT5": "Decision Tree (depth = 5)", "DT10": "Decision Tree (depth = 10)", "LR2": "Logistic Regression", "PT": "Perceptron", "NB": "Gaussian Naive Bayes"}

    let table_container = document.getElementById("insertTable")
    if (selectedModelData) {
        console.log(location.state)
		const data_table = document.createElement("table");
		data_table.setAttribute("id", "table_step3")
		const table_header = document.createElement("thead");
        const table_header_row = document.createElement("tr");
        // let hover_tracker = {}
        // let table_container = document.getElementById("tableContainer")
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
			// console.log(data[0])
			// const div_container = document.createElement("div")
			// div_container.setAttribute("id", "row_div")
			let col_index = 0
			for (let col in selectedModelData[i]) {
				// console.log(trainingData[i][col])
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
                    console.log(new_text_node)
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
        // let table_container = document.getElementById("insertTable")
		document.body.appendChild(data_table);

        let column_hover_texts = {"Feature Combination": "Combinations important for model", "Weight": "A higher numerical value indicates a more important feature"}

		for (var column_key in selectedModelData[0]) {
            console.log("ever here???")
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
                // document.getElementById("hover_"+column_key).classList.remove("displayNone")
                console.log(e.pageX+20)
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
            // hover_tracker[hover_key] = 1
        }

        
    }
    var model_explanations = {"Lasso": "The Lasso model assigns weights to each of the feature combinations generated by Wide Learning. Lasso automatically performs feature selection by assigning some of the feature combinations a weight of 0, which excludes them from the final model.", 
                            "SVM": "Support Vector Machine (SVM) is one of the well-known algorithms in machine learning. This method finds a hyperplane that maximally separates the data so that the two classes are farthest from each other, effectively separating the data into two classes.", 
                            "RF": "Random forests combine the outputs of multiple decision trees into a single prediction. Combining multiple results enables highly accurate predictions.", 
                            "DT2": "Decision Tree is a model that decomposes data like a tree and makes predictions. It is a very easy-to-understand model because it makes predictions by repeatedly asking ‘yes’ and ‘no’ questions.", 
                            "DT3": "Decision Tree is a model that decomposes data like a tree and makes predictions. It is a very easy-to-understand model because it makes predictions by repeatedly asking ‘yes’ and ‘no’ questions.", 
                            "DT5": "Decision Tree is a model that decomposes data like a tree and makes predictions. It is a very easy-to-understand model because it makes predictions by repeatedly asking ‘yes’ and ‘no’ questions.", 
                            "DT10": "Decision Tree is a model that decomposes data like a tree and makes predictions. It is a very easy-to-understand model because it makes predictions by repeatedly asking ‘yes’ and ‘no’ questions.", 
                            "LR2": "Logistic regression is a machine learning algorithm used for classification problems that estimates the probability of classifying data into two classes.", 
                            "PT": "Perceptron is a basic algorithm in machine learning that performs classification by multiplying input features with weights and then summing them up.", 
                            "NB": "Gaussian Naive Bayes is a machine learning algorithm used for classification problems. It assumes that each class's feature values follow a Gaussian distribution and utilizes Bayes' theorem to compute conditional probabilities. It learns the mean and variance for each class from the training data and predicts the class of new data."}
        
    const lassoFeatureSelectionButton = () => {
        document.getElementById("step4Div").classList.add("stepDivBackground")

        navigate("/step5");
    }
    
	
	return (
		<div>
			<div id = "step3container">
				{/* {location.state.model} */}
			</div>
			<div class="loading">
				{/* <p>{output}</p> */}
			</div>
            <div>
                <div id="step3selectedModelExplanation">
                The table shows the weights from <b>{model_names[location.state.model_name]}</b>. {model_explanations[location.state.model_name]}
                </div>
                {(location.state.model_name == "Lasso") ? <button class="step4LassoButotn" onClick={lassoFeatureSelectionButton}>Click here to select your own features for Lasso</button> : ""}
                <div id="insertTable">

                </div>
            </div>
            
            
		</div>
		
	);
};

export default Step3_model_selected;
