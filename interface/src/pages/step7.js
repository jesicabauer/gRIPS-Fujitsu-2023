import React, {useState, useEffect} from 'react';
import { useNavigate } from "react-router-dom";

const Step7 = () => {
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

	const navigate = useNavigate();

	const [dataUploaded, setDataUploaded] = useState(false) 
    console.log(dataUploaded)

	// the react post request sender
    const uploadTestingFile = async (e) => {
        const file = e.target.files[0];
        console.log(file)
        if (file != null) {
            const data = new FormData();
            data.append('file_from_react', file);
            console.log(data)
            let response = await fetch('/testing_file_upload',
                {
                method: 'post',
                body: data,
                }
            );
            let res = await response.json();
            if (res.status !== 1){
                alert('Error uploading file');
            }
			setDataUploaded(true)
        }
    };

	const redirect = () => {
        navigate("/step7-testing-data");
    }

	return (
		<div>
			<div class="fileUpload">
			<label>
			<input
				type="file" onChange={uploadTestingFile}/>
				{dataUploaded? 'File ready! Click "Upload" below to display data or click here to upload another' : 'Click here to upload testing data'}
			</label>
			</div>
			<button class="uploadButton" onClick={redirect}>Upload</button>
		</div>
	);
};

export default Step7;
