import React, { useState, useEffect } from "react";

function App() {
	const [data, setData] = useState([{}]);

	useEffect(() => {
		fetch("/members")
			.then((res) => res.json())
			.then((data) => {
				setData(data);
				console.log(data);
			});
	}, []);
	return (
		<>
			{typeof data.building === "undefined" ? (
				<p>Loading...</p>
			) : (
				data.building.map((corner, i) => <p key={i}>{corner}</p>)
			)}
		</>
	);
}

export default App;
