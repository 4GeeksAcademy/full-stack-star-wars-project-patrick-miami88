import { Link } from "react-router-dom";
import useGlobalReducer from "../hooks/useGlobalReducer";

export const Navbar = () => {
	const {store, dispatch} = useGlobalReducer()

	const handleSignOut = () => {
		dispatch({type: "set_user", payload: null})
		localStorage.removeItem("token")
		return
	}

	return (
		<nav className="navbar navbar-light bg-light">
			<div className="container">
				<Link to="/">
					<span className="navbar-brand mb-0 h1">React Boilerplate</span>
				</Link>
				<div className="ml-auto">
					{store.user ?
					<div> 
						<button className="btn btn-danger" type="button" onClick={handleSignOut}>Sign Out</button>
						<Link to="/private">
								<button className="btn-primary btn" type="button">Profile</button>
						</Link>
					</div>	
					:
						<div>
							<Link to="/signup">
								<button className="btn-secondary btn" type="button">Sign Up</button>
							</Link>
							<Link to="/login">
								<button className="btn-primary btn" type="button">Log In</button>
							</Link>
						</div>		
				}
				</div>
			</div>
		</nav>
	);
};