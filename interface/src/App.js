import React, {useState, useEffect} from 'react'

function App() {
  const [data, setData] = useState({}) 
  useEffect(() => {
  // Using fetch to fetch the api from
  // flask server it will be redirected to proxy
  fetch("/data").then((res) =>
      res.json().then((data) => {
          // Setting a data from api
          setData(data);
          console.log(data)
      })
    );
  }, []);
  return (
    <div>
        <p>{data.data}</p>
    </div>
  )
}

export default App
