import React, { useEffect, useState } from "react";
import Card from "../components/Card";

function Upload() {
    const [uploadMessage, setUploadMessage] = useState("");
    const [error, setError] = useState("");

    useEffect(() => {
        fetch("/upload")
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
        <div className="flex justify-center items-center">
            <div className="max-w-6xl w-full">
                <Card></Card>
            </div>
        </div>
    );
}

export default Upload;
