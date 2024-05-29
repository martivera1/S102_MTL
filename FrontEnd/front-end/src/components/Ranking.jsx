import React from 'react';

const Ranking = ({ ranking }) => {
  const { title, description, userpic, username, stars } = ranking;

  const starElements = [];
  for (let i = 0; i < stars; i++) {
    starElements.push(<span key={i}>⭐</span>);
  }

  return (
    <div className='flex justify-center items-center bg-white flex-col text-center p-4 rounded-2xl shadow-md  hover:scale-105 hover:cursor-pointer'>
      <h1 className='text-xl font-bold'>{title}</h1>
      <p className="text-right text-gray-500">by {username}</p>
      <div className='bg-slate-200 w-full rounded-xl mt-1' style={{ height: '2px' }}></div>
      <p className='mt-2 w-full max-w-sm bg-slate-100 p-1 min-w-[380px] min-h-[80px]' style={{ overflowWrap: 'break-word' }}>
        {description}
      </p>
      <div className='flex items-center justify-between w-full mt-4'>
        <div className='flex items-center'>
          <img src={userpic} alt="Profile" className='h-10 mr-2 ml-2'/>
          <div className='flex'>
            {starElements}
          </div>
        </div>
        <button className='bg-blue-600 text-white px-4 py-1 rounded-lg mr-2'>See more</button>
      </div>
    </div>
  );
}

export default Ranking;
