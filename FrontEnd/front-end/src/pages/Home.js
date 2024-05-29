import React, { useEffect, useState } from "react";
import Ranking from "../components/Ranking";
import Profile1 from "../static/images/profile1.png"
import Profile2 from "../static/images/profile2.png"
import Profile3 from "../static/images/profile3.png"
import Profile4 from "../static/images/profile4.png"

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

    // Aixo es temporal mentre no tinguem crides a la BBDD
    const rankings = [
        {
            "title": "Top Big Black Cocks que he probat",
            "description": "No em puc decidir, totes estàven boníssimes.",
            "userpic": Profile1,
            "username": "gerard",
            "stars": 4
        },
        {
            "title": "Best Indie Tracks",
            "description": "Discover hidden gems and unique musical experiences from independent artists. These indie songs showcase creativity and originality.",
            "userpic": Profile2,
            "username": "indiemusicfan",
            "stars": 5
        },
        {
            "title": "Classic Rock Anthems",
            "description": "Relive the magic of timeless rock songs. From 'Stairway to Heaven' to 'Bohemian Rhapsody,' this ranking takes you on a nostalgic musical journey.",
            "userpic": Profile3,
            "username": "rocknrollfanatic",
            "stars": 4
        },
        {
            "title": "Electronic Dance Hits",
            "description": "Get ready to dance! These electrifying tracks will make you move. From pulsating beats to euphoric drops, this ranking is a party on your playlist.",
            "userpic": Profile4,
            "username": "raveenthusiast",
            "stars": 1
        },
        {
            "title": "Soulful R&B Grooves",
            "description": "Let the smooth rhythms and heartfelt lyrics of R&B songs wash over you. From old-school legends to contemporary crooners, this ranking celebrates soulful vibes.",
            "userpic": Profile1,
            "username": "rnblover2024",
            "stars": 5
        },
        {
            "title": "Country Ballads",
            "description": "Grab your cowboy boots! These country songs tell stories of love, heartache, and wide-open spaces. Yeehaw!",
            "userpic": Profile2,
            "username": "countrymusicfan",
            "stars": 2
        },
        {
            "title": "Pop Chart-Toppers",
            "description": "Sing along to the catchiest pop tunes. These songs dominate the charts and keep us humming all day long.",
            "userpic": Profile4,
            "username": "popmusiclover",
            "stars": 4
        },
        {
            "title": "Hip-Hop Bangers",
            "description": "From gritty street anthems to club-ready tracks, this ranking showcases the best of hip-hop. Turn up the volume and feel the rhythm.",
            "userpic": Profile3,
            "username": "hiphophead",
            "stars": 3
        }
        ];


    return (
    <div className="flex flex-wrap justify-center items-center">
        {rankings.map((ranking, index) => (
        <div key={index} className="mt-6 mx-4">
            <Ranking ranking={ranking} />
        </div>
        ))}    
    </div>
);

}

export default Home;