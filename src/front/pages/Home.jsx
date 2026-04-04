import React, { useEffect } from "react"
import rigoImageUrl from "../assets/img/rigo-baby.jpg";
import useGlobalReducer from "../hooks/useGlobalReducer.jsx";

export const Home = () => {

	const { store, dispatch } = useGlobalReducer()

	useEffect(() => {
	}, [])

	return (
		<div className="text-center mt-5">
			{store.user ? <h1 className="display-2 fst-italic">Welcome {store.user}!</h1> : <h1 className="display-2 fw-semibold">Welcome to the home page!</h1>}
		</div>
	);
}; 