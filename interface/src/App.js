// import React, {useState, useEffect} from 'react'

// function App() {
//   const [data, setData] = useState({}) 
//   useEffect(() => {
//   // Using fetch to fetch the api from
//   // flask server it will be redirected to proxy
//   fetch("/data").then((res) =>
//       res.json().then((data) => {
//           // Setting a data from api
//           setData(data);
//           console.log(data)
//       })
//     );
//   }, []);
//   return (
//     <div>
//         <p>{data.data}</p>
//     </div>
//   )
// }

// export default App

import React from 'react';
import './App.css';
import Navbar from './components/NavBar';
import { BrowserRouter as Router, Routes, Route }
	from 'react-router-dom';
import Home from './pages';
import Step1 from './pages/step1';
import Step1_training_data from './pages/step1-training-data';
import Step2 from './pages/step2';
import Step3 from './pages/step3';
import Step3_model_selected from './pages/step3-model-selected';
import Step4 from './pages/step4';
import DisplayChart from './pages/step4-chart';
import Step5 from './pages/step5';
import Step6 from './pages/step6';
import Step7 from './pages/step7';
import Step7_testing_data from './pages/step7-testing-data';
import Step8 from './pages/step8';

function App() {
	return (
		<Router>
			<Navbar />
			<Routes>
				<Route exact path='/' element={<Home />} />
				<Route path='/step1' element={<Step1 />} />
        		<Route path='/step1-training-data' element={<Step1_training_data />} />
				<Route path='/step2' element={<Step2 />} />
				<Route path='/step3' element={<Step3 />} />
				<Route path='/step3_model_selected' element={<Step3_model_selected />} />
				<Route path='/step4' element={<Step4 />} />
				<Route path='/step4-chart' element={<DisplayChart />} />
				<Route path='/step5' element={<Step5 />} />
				<Route path='/step6' element={<Step6 />} />
				<Route path='/step7' element={<Step7 />} />
				<Route path='/step7-testing-data' element={<Step7_testing_data />} />
				<Route path='/step8' element={<Step8 />} />
			</Routes>
		</Router>
	);
}

export default App;
