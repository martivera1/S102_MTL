import React from "react";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import Home from "./pages/Home";
import Upload from "./pages/Upload";
import "./static/styles/App.css";
import Header from "./components/Header";
import Login from "./pages/Login";
import Ranking from "./pages/Ranking";  // Import Ranking component

function App() {
    return (
        <Router>
            <div>
                <Header />
                <Routes>
                    <Route path="/" element={<Navigate to="/home" />} />
                    <Route path="/home" element={<Home />} />
                    <Route path="/upload" element={<Upload />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/ranking/:rankingId" element={<Ranking />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
