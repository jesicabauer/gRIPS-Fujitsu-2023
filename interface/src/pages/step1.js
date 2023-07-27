// import React from "react";
import { data } from 'jquery';
import React, {useState, useEffect} from 'react'
import $ from 'jquery';
import { useNavigate } from "react-router-dom";

const Step1 = () => {
    const table_element = document.getElementById("combo_table")
	if (table_element) {
		table_element.remove()
	}
    const table3_element = document.getElementById("table_step3")
	if (table3_element) {
		table3_element.remove()
	}

    const navigate = useNavigate();

    const [dataUploaded, setDataUploaded] = useState(false) 
    console.log(dataUploaded)

    // the react post request sender
    const uploadTrainingFile = async (e) => {
        const file = e.target.files[0];
        console.log(file)
        if (file != null) {
            const data = new FormData();
            data.append('file_from_react', file);
            console.log(data)
            let response = await fetch('/training_file_upload',
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


    // console.log(dataUploaded)
    // const [step1Data, setStep1Data] = useState({}) 
    // useEffect(() => {
    //     // Using fetch to fetch the api from
    //     // flask server it will be redirected to proxy
    //     fetch("/step1_display").then((res) =>
    //         res.json().then((data_in) => {
    //             // Setting a data from api
    //             setStep1Data(data_in);
    //             console.log(data_in)
    //         })
    //         );
    //     }, []);

    const redirect = () => {
        navigate("/step1-training-data");
    }
    // if (dataUploaded) {
        
    //     console.log(step1_data)
    // }


    // const [data, setData] = useState({}) 
    // useEffect(() => {
    // // Using fetch to fetch the api from
    // // flask server it will be redirected to proxy
    // fetch("/data").then((res) =>
    //     res.json().then((data) => {
    //         // Setting a data from api
    //         setData(data);
    //         console.log(data)
    //     })
    //     );
    // }, []);
    // return (
    //     <div>
    //         <p>{data.data}</p>
    //     </div>
    // )
	return (
        // the react form
        <div>
            <div class="fileUpload">
                <label>
                    {/* <form> */}
                    <input 
                        type="file" onChange={uploadTrainingFile}/>
                        {dataUploaded? 'File ready! Click "Upload" below to display data or click here to upload another' : 'Click here to upload training data'}
                    {/* <input type="submit" value="Submit" onClick={uploadFile}></input> */}
                    {/* </form> */}
                </label>
            
            </div>
            <button class="uploadButton" onClick={redirect}>Upload</button>
         </div>
        
	// 	<div>
	// 		<h1>
	// 			GeeksforGeeks is a Computer
	// 			Science portal for geeks.
	// 		</h1>
	// 	</div>
	);
};

export default Step1;
