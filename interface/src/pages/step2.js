import React, {useState, useEffect} from 'react'

const Step2 = () => {
	const [data, setData] = useState({}) 
    useEffect(() => {
    // Using fetch to fetch the api from
    // flask server it will be redirected to proxy
    fetch("/data").then((res) =>
        res.json().then((data_in) => {
            // Setting a data from api
            setData(data_in);
            console.log(data_in)
        })
        );
    }, []);

	console.log(data.length)
	var output = ""
	if (data.length) {
		output = data.map((row, i) => (
			<div key={i}>
				<p>{row.important_combo}</p>
				<p>{row.combo_length}</p>
				<p>{row.pos_count}</p>
				<p>{row.neg_count}</p>
			</div>
		))
	}
	
	// for (index = 0; index <)
    return (
        <div>
            <p>{output}</p>
        </div>
    )
	// return (
	// 	<div>
	// 		<h1>Step2</h1>
	// 	</div>
	// );
};

export default Step2;
