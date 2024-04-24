import React, { useEffect, useState } from "react";
import Card from "../components/Card";

function Home() {
    const [homeMessage, setHomeMessage] = useState("");
    const [error, setError] = useState("");

    useEffect(() => {
<<<<<<< HEAD
        fetch("/home")
=======
        fetch("http://localhost:5000/home")
>>>>>>> 78d7a46286421e4d321fb988c8d86fa7a83c63c3
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
            <Card></Card>
        </div>
    );
}

export default Home;
