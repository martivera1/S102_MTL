import React, { useEffect, useState } from "react";
import Ranking from "../components/Ranking";
import { BACKEND_URL } from "../constants";

function Home() {
    const [rankings, setRankings] = useState([]);
    const [error, setError] = useState("");

    useEffect(() => {
        fetch(`${BACKEND_URL}/get_rankings`)
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then((data) => setRankings(data))
            .catch((error) => setError(error.message));
    }, []);

    return (
        <div className="flex flex-wrap justify-center items-center">
            {rankings.map((ranking, index) => (
                <div key={index} className="mt-6 mx-4">
                    <Ranking ranking={ranking}/>
                </div>
            ))}    
        </div>
    );
}

export default Home;
