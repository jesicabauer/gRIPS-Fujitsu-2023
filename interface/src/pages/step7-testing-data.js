
import React, {useState, useEffect} from 'react'

const Step7_testing_data = () => {

    const table_element = document.getElementById("testing_table")
	if (table_element) {
		table_element.remove()
	}

    const updated_weights_table_element = document.getElementById("step6_updated_weights")
	if (updated_weights_table_element) {
		updated_weights_table_element.remove()
	}

    const [testingData, setTestingData] = useState({}) 
    useEffect(() => {
        // Using fetch to fetch the api from
        // flask server it will be redirected to proxy
        fetch("/step7_display").then((res) =>
            res.json().then((data_in) => {
                // Setting a data from api
                setTestingData(data_in);
                console.log(data_in)
            })
            );
        }, []);

    console.log(testingData)
    console.log(testingData.length)

    let table_container = document.getElementById("tableContainer")
    if (testingData.length) {
        const data_table = document.createElement("table");
		data_table.setAttribute("id", "testing_table")
		const table_header = document.createElement("thead");
        const table_header_row = document.createElement("tr");

        for (var column_key in testingData[0]) {
            console.log(column_key)
            const new_header = document.createElement("th")
            const header_text = document.createTextNode(column_key);
            new_header.setAttribute("id", "column_"+column_key)
            new_header.appendChild(header_text)
            table_header_row.appendChild(new_header)
        }

        table_header.appendChild(table_header_row)
        const table_body = document.createElement("tbody");
        for (let i = 0; i < testingData.length; i += 1) {
			const table_row = document.createElement("tr")
	
			for (let col in testingData[i]) {
				console.log(testingData[i][col])
                const table_cell = document.createElement("td")
				const cell_text = document.createTextNode(testingData[i][col]);
				table_cell.appendChild(cell_text);
	
				table_row.appendChild(table_cell);
            }
           table_body.appendChild(table_row); 
        }


        data_table.appendChild(table_header);
		data_table.appendChild(table_body);

		table_container.appendChild(data_table);

        
    }

    return (
		<div class="displayTrainingTable">
            <div class="tableContainer" id="tableContainer"></div>
			
            <div class="step7explanations">
                The testing data you uploaded is shown here and will be used to generate prediction scores from the potential models trained in Step 4. Scroll to check its contents and click on <b>Step 8</b> above to proceed.
            </div>
		</div>
    )
};

export default Step7_testing_data;