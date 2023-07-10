import React from 'react';

const Step6 = () => {
	const table_element = document.getElementById("combo_table")
	if (table_element) {
		table_element.remove()
	}
	return (
		<div>
			<h1>Step6</h1>
		</div>
	);
};

export default Step6;
