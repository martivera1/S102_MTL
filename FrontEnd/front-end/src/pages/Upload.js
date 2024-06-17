import React, { useEffect, useState } from "react";
import Card from "../components/Card";
import { BACKEND_URL } from "../constants";

function Upload() {
    const [pieces, setPieces] = useState([]);
    const [error, setError] = useState("");

    useEffect(() => {
        fetch(`${BACKEND_URL}/get_links`)
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then((data) => setPieces(data.links.map((link, index) => ({ ...link, id: String(index) }))))
            .catch((error) => setError(error.message));
    }, []);

    const updatePieceStatus = (link, status) => {
        setPieces((prevPieces) => 
            prevPieces.map((piece) =>
                piece.link === link ? { ...piece, status: status } : piece
            )
        );
    };

    return (
        <div className="flex justify-center items-center">
            <div className="w-full">
                <Card pieces={pieces} updatePieceStatus={updatePieceStatus} />
            </div>
        </div>
    );
}

export default Upload;
