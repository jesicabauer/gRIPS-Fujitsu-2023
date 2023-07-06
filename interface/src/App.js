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
import Step2 from './pages/step2';
import Step3 from './pages/step3';
import Step4 from './pages/step4';
import Step5 from './pages/step5';
import Step6 from './pages/step6';

function App() {
	return (
		<Router>
			<Navbar />
			<Routes>
				<Route exact path='/' element={<Home />} />
				<Route path='/step1' element={<Step1 />} />
				<Route path='/step2' element={<Step2 />} />
				<Route path='/step3' element={<Step3 />} />
				<Route path='/step4' element={<Step4 />} />
        <Route path='/step5' element={<Step5 />} />
        <Route path='/step6' element={<Step6 />} />
			</Routes>
		</Router>
	);
}

export default App;
