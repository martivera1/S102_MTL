import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { BACKEND_URL } from '../constants';
import Obra from './Obra';

const RankingResults = () => {
  const { rankingId } = useParams();
  const [results, setResults] = useState({});

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

  return (
    <div className='flex bg-white rounded-3xl md:w-[500px] sm:w-[400px] mx-auto my-[8vh] flex-col font-roboto shadow-2xl p-8'>
      {Object.keys(results).map(starLevel => (
        <div key={starLevel}>
          <h2 className='text-xl font-bold mt-4'>Dificulty Level {starLevel}</h2>
          {results[starLevel].map(obra => (
            <Obra key={obra.id_obra} obra={obra} />
          ))}
        </div>
      ))}
    </div>
  );
};

export default RankingResults;
