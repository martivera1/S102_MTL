import React, { useEffect, useState } from "react";
import LoginCard from "../components/LoginCard";

function Login() {
    const [loginMessage, setLoginMessage] = useState("");
    const [error, setError] = useState("");

    useEffect(() => {
        fetch("/login")
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then((data) => setLoginMessage(data.message))
            .catch((error) => setError(error.message));
    }, []);

    return (
    <div className="flex flex-wrap justify-center items-center">
        <LoginCard />
    </div>
);

}

export default Login;