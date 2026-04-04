import React, { useEffect, useState } from "react";
import useGlobalReducer from "../hooks/useGlobalReducer";

export const Private = () => {
    const {store, dispatch} = useGlobalReducer()
    const [favoriteCharacters, setFavoriteCharacters] = useState([])
    const [favoritePlanets, setFavoritePlanets] = useState([])
    const BASE_URL = import.meta.env.VITE_BACKEND_URL

    const handleGettingFavorites = async() => {
        const token = localStorage.getItem("token")
        if(!token){
            return
        }
        const response = await fetch(BASE_URL + "/users/favorites", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            }
        })
        if(!response.ok){
            console.log("User could not be authenticated")
            dispatch({type: "set_user", payload: null})
            return
        }
        const data = await response.json()
        if(!store.user) {
            dispatch({type: "set_user", payload: data.email})
        }
        setFavoriteCharacters(data.favorite_characters)
        setFavoritePlanets(data.favorite_planets)
        return data
    }

    useEffect(() => {
        handleGettingFavorites()
    },[])

    return (
        <>
            <div className="text-center">
                <h1>{store.user? `Welcome to the private page ${store.user}` : "You must be signed in to view this page"}</h1>
                <ul>
                    {favoriteCharacters?.map((character) => (
                        <li key={character.id}>{character.name}</li>
                    ))}
                </ul>
                <ul>
                    {favoritePlanets?.map((planet) => (
                        <li key={planet.id}>{planet.name}</li>
                    ))}
                </ul>
            </div>
        </>
    )
    
}