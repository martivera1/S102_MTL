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

    // Aixo es temporal mentre no tinguem crides a la BBDD
    const pieces = [{
            title: "Song.pdf",
            size: "1.2 KB",
            type: "pdf"
        },
        {
            title: "Video.mp4",
            size: "4.7 MB",
            type: "video"
        },
        {
            title: "https://www.youtube.com/",
            size: "watch?v=dQw4w9WgXcQ&ab_channel=RickAstley",
            type: "url"
        }, {
            title: "Song.pdf",
            size: "1.2 KB",
            type: "pdf"
        }, {
            title: "Video.mp4",
            size: "4.7 MB",
            type: "video"
        }, {
            title: "https://www.youtube.com/",
            size: "watch?v=dQw4w9WgXcQ&ab_channel=RickAstley",
            type: "url"
        }
    ].map((piece, index) => ({ ...piece, id: String(index) }));;

    return (
        <div className="flex justify-center items-center">
            <div className="max-w-6xl w-full">
                <Card pieces={pieces} />
            </div>
        </div>
    );
}

export default Upload;
