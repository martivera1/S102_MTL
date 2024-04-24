import React, { useEffect, useState } from "react";

function Upload() {
    const [uploadMessage, setUploadMessage] = useState("");
    const [error, setError] = useState("");

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
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then((data) => setUploadMessage(data.message))
            .catch((error) => setError(error.message));
    }, []);

    return (
        <div>
            <h1>/upload Message: {uploadMessage}</h1>
            {error && <p>Error: {error}</p>}
        </div>
    );
}

export default Upload;
