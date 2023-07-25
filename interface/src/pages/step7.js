import React, {useState, useEffect} from 'react';

const Step7 = () => {
	const table_element = document.getElementById("combo_table")
	if (table_element) {
		table_element.remove()
	}
	const table3_element = document.getElementById("table_step3")
	if (table3_element) {
		table3_element.remove()
	}

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
        }
    };

	return (
		// <form>
		<div class="fileUpload">
		<label>
        <input
            type="file" onChange={uploadTestingFile}/>
            Click here to upload testing data
        {/* <input type="submit" value="Submit" onClick={uploadFile}></input> */}
		</label>
        </div>
	);
};

export default Step7;
