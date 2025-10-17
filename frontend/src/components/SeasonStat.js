import React, { useEffect, useState } from 'react';

export default function SeasonStat() {
    
    fetch("http://127.0.0.1:8000/api/stats/")
        .then(res => res.json())
        .then(data => console.log(data))

    return (
        <div className="SeasonStat">
            <h1>Season Statistics</h1>
            <p>Display season statistics here.</p>
        </div>
    )
}