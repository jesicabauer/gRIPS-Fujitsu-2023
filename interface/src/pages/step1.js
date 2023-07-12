// import React from "react";
import React, {useState, useEffect} from 'react'

const Step1 = () => {
    const table_element = document.getElementById("combo_table")
	if (table_element) {
		table_element.remove()
	}
    const table3_element = document.getElementById("table_step3")
	if (table3_element) {
		table3_element.remove()
	}
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
	// return (
	// 	<div>
	// 		<h1>
	// 			GeeksforGeeks is a Computer
	// 			Science portal for geeks.
	// 		</h1>
	// 	</div>
	// );
};

export default Step1;
