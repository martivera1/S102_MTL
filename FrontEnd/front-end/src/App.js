import React, { useEffect, useState } from "react"
import "./App.css"
import Card from "./components/Card"

function App() {
    const [message, setMessage] = useState("")
    const [error, setError] = useState("")

    useEffect(() => {
        fetch("http://localhost:5000/")
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Network response was not ok")
                }
                return response.json()
            })
            .then((data) => setMessage(data.message))
            .catch((error) => setError(error.message))
    }, [])

    return (
        <div>
            <h1>{message}</h1>
        </div>
    )
}

export default App
