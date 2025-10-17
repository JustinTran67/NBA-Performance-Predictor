import React, { useState } from 'react';

//Figure out how all this works below!
export default function Predict() {
  const [predictedPoints, setPredictedPoints] = useState(null);

  const postPrediction = () => {
    //const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYwNjY4NDExLCJpYXQiOjE3NjA2NjgxMTEsImp0aSI6Ijc4N2QyOTdhZDEyOTQzNjJhNTkyYWE2ZDA1NGI5NzQzIiwidXNlcl9pZCI6IjEifQ.Kzv-IiFql-to5No7WAmSWwd898KizEgX7tvu4inOQxU";

    fetch('http://localhost:8000/api/predictions/predict/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        //'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({
        minutes: 35.0,
        fg_percent: 0.45,
        threep_percent: 0.38,
        ft_percent: 0.85,
        rebounds: 7.1,
        assists: 5.4,
        steals: 2.5,
        blocks: 1.4,
        turnovers: 3.6,
        personal_fouls: 2.1,
      }),
    })
      .then(res => {
        if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`);
        return res.json();
      })
      .then(data => {
        console.log("Predicted Points:", data.predicted_points);
        setPredictedPoints(data.predicted_points);
      })
      .catch(err => console.error("Prediction request failed:", err));
  };

  return (
    <div className='Predict'>
      <h1>Predict Component</h1>
      <p>This component sends a POST request to predict points per game based on player stats.</p>
      <button onClick={postPrediction}>Predict Points</button>
      <h2>Predicted Points: {predictedPoints}</h2>
    </div>
  );
}