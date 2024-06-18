import React from 'react';
import { useLocation, Link } from 'react-router-dom';

const Ranking = ({ ranking }) => {
  const { name, description, id, username, stars } = ranking;

  const starElements = [];
  for (let i = 0; i < stars; i++) {
    starElements.push(<span key={i}>⭐</span>);
  }

  return (
    <Link to={`/ranking/${id}`}>
      <div className='flex justify-center items-center bg-white flex-col text-center p-4 rounded-2xl shadow-md hover:scale-105 hover:cursor-pointer transition-transform duration-300 ease-in-out'>
        <h1 className='text-xl font-bold'>{name}</h1>
        <div className='bg-slate-200 w-full rounded-xl mt-1' style={{ height: '2px' }}></div>
        <p className='mt-2 w-full max-w-sm bg-slate-100 p-1 min-w-[380px] min-h-[80px]' style={{ overflowWrap: 'break-word' }}>
          {description}
        </p>
        <div className='flex items-center justify-between w-full mt-4'>
          <div className='flex items-center'>
            <img src="usericon.png" alt="Profile" className='h-10 mr-2 ml-2'/>
            <div className='flex'>
              <p className="text-right text-gray-500 w-[100px]">by {username}</p>
            </div>
          </div>
            <button className='bg-blue-600 text-white px-4 py-1 rounded-lg mr-2'>Show Full Ranking</button>
        </div>
      </div>
    </Link>
  );
}

export default Ranking;
