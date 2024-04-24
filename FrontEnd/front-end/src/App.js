import React from "react";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import Home from "./pages/Home";
import Upload from "./pages/Upload";
import "./static/styles/App.css";

function App() {
    return (
        <Router>
            <div>
                {/* Header Component Here */}
                
                <Routes>
                    <Route path="/" element={<Navigate to="/home" />} />
                    <Route path="/home" element={<Home />} />
                    <Route path="/upload" element={<Upload />} />
                    {/* Add other routes here */}
                </Routes>
                
                {/* Footer Component Here */}
            </div>
        </Router>
    );
}

export default App;
