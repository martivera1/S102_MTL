import React, { useEffect, useState } from "react"
import "./App.css"
import Card from "./components/Card"

function App() {
    const [homeMessage, setHomeMessage] = useState("")
    const [uploadMessage, setUploadMessage] = useState("")
    const [error, setError] = useState("")

    // Fetch data for /home endpoint
    useEffect(() => {
        fetch("http://localhost:5000/home")
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Network response was not ok")
                }
                return response.json()
            })
            .then((data) => setHomeMessage(data.message))
            .catch((error) => setError(error.message))
    }, [])

    // Fetch data for /upload endpoint
    useEffect(() => {
        fetch("http://localhost:5000/upload", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({}),
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Network response was not ok")
                }
                return response.json()
            })
            .then((data) => setUploadMessage(data.message))
            .catch((error) => setError(error.message))
    }, [])

    return (
        <div>
            <h1>/home Message: {homeMessage}</h1>
            <h1>/upload Message: {uploadMessage}</h1>
            {error && <p>Error: {error}</p>}
        </div>
    )
}

export default App
