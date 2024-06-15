import React, { useEffect, useState } from "react";
import Card from "../components/Card";
import { BACKEND } from "../constants";

function Upload() {
    const [uploadMessage, setUploadMessage] = useState("");
    const [error, setError] = useState("");

    useEffect(() => {
        fetch(BACKEND + "/upload")
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then((data) => setUploadMessage(data.message))
            .catch((error) => setError(error.message));
    }, []);

    // Aixo es temporal mentre no tinguem crides a la BBDD
    const pieces = [{
            title: "Youtube Song Example",
            size: "https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley",
        },
        {
            title: "Youtube Song Example",
            size: "https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley",
        },
        {
            title: "Youtube Song Example",
            size: "https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley",
        }, {
            title: "Youtube Song Example",
            size: "https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley",
        }, {
            title: "Youtube Song Example",
            size: "https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley",
        }, {
            title: "Youtube Song Example",
            size: "https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley",
        }
    ].map((piece, index) => ({ ...piece, id: String(index) }));;

    return (
        <div className="flex justify-center items-center">
            <div className=" w-full">
                <Card pieces={pieces} />
            </div>
        </div>
    );
}

export default Upload;
