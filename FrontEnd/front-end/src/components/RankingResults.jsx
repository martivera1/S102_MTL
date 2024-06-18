import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { BACKEND_URL } from '../constants';
import Obra from './Obra';

const RankingResults = () => {
  const { rankingId } = useParams();
  const [results, setResults] = useState({});
  const [currentLevel, setCurrentLevel] = useState(0);
  const starLevels = Object.keys(results);

  useEffect(() => {
    fetch(`${BACKEND_URL}/get_ranking_results/${rankingId}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        setResults(data);
      })
      .catch(error => {
        console.error('Error fetching ranking results:', error);
      });
  }, [rankingId]);

  const handlePrevious = () => {
    setCurrentLevel((prevLevel) => (prevLevel > 0 ? prevLevel - 1 : starLevels.length - 1));
  };

  const handleNext = () => {
    setCurrentLevel((prevLevel) => (prevLevel < starLevels.length - 1 ? prevLevel + 1 : 0));
  };

  return (
    <div className='flex flex-col items-center bg-white rounded-3xl w-[70vw] max-w-[850px] mt-[3vh] font-roboto shadow-2xl px-6 py-2 pb-5'>
      {starLevels.length > 0 && (
        <>
          <div className='flex items-center justify-between w-full'>
            <button onClick={handlePrevious} className='text-2xl font-bold mt-3'>
              &lt;
            </button>
            <h2 className='text-lg font-medium mt-4 mb-3'>
              DIFFICULTY LEVEL {starLevels[currentLevel]}
            </h2>
            <button onClick={handleNext} className='text-2xl font-bold mt-3'>
              &gt;
            </button>
          </div>
          <div className='w-full h-[600px] overflow-y-auto px-2 bg-slate-100 rounded-lg'>
            {results[starLevels[currentLevel]].map(obra => (
              <Obra key={obra.id_obra} obra={obra} />
            ))}
          </div>
        </>
      )}
    </div>
  );
};

export default RankingResults;
