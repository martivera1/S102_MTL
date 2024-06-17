import React, { useEffect, useState } from "react";
import Card from "../components/Card";
import { BACKEND_URL } from "../constants";

function Upload() {

    return (
        <div className="flex justify-center items-center">
            <div className="w-full">
                <Card/>
            </div>
        </div>
    );
}

export default Upload;
