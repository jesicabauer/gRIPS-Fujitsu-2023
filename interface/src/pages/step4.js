import React from 'react';

const Step4 = () => {
	const table_element = document.getElementById("combo_table")
	if (table_element) {
		table_element.remove()
	}
	return (
		<div>
			<h1>Step4</h1>
		</div>
	);
};

export default Step4;
