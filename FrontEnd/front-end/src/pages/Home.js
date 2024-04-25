import React, { useEffect, useState } from "react";
import Card from "../components/Card";

function Home() {
    const [homeMessage, setHomeMessage] = useState("");
    const [error, setError] = useState("");

    useEffect(() => {
        fetch("/home")
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then((data) => setHomeMessage(data.message))
            .catch((error) => setError(error.message));
    }, []);

    return (
        <div>
            
        </div>
    );
}

export default Home;
