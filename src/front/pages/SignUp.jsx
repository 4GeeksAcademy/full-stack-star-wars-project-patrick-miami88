import React, { useState } from "react";
import useGlobalReducer from "../hooks/useGlobalReducer";

export const SignUp = () => {
    const BASE_URL = import.meta.env.VITE_BACKEND_URL
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [signUpFailed, setSignUpFailed] = useState(false)

    const handleSignUp = async() => {
        const response = await fetch(BASE_URL + "/signup", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(
                {
                    "email": email,
                    "password": password
                }
            )
        })
        if(!response.ok) {
            setSignUpFailed(true)
            return
        }
        const data = await response.json()
        return data
    }

     return (
       <>
            <h1 className="mx-auto text-center p-4">Welcome to the sign up page</h1>
            <div className="d-flex container">
                
                {signUpFailed ? <h3 className="text-danger">Sign up failed!</h3>: null}
                <div className="form-control row">
                    <div className="col-3"></div>
                    <div className="col-6 p-3">
                        <div className="ms-5">
                            <label for="email" className="pe-2">Email</label>
                            <input type="text" name="email" className="rounded-2" onChange={e => setEmail(e.target.value)} value={email} />
                        </div>
                        <div className="p-3">
                            <label for="password" className="pe-2">Password</label>
                            <input type="text" name="password" className="rounded-2" onChange={e => setPassword(e.target.value)} value={password} />
                        </div>
                    </div>
                    <div className="col-3"></div>
                </div>
                
            </div>
            <div className="container p-3">
            <button className="btn btn-info" onClick={handleSignUp}>Sign Up</button>
            </div>
        </>
    )
}
