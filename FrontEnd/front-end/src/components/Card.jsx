import React, { useState, useEffect } from 'react';
import ListedPiece from './ListedPiece';
import { DragDropContext, Droppable } from 'react-beautiful-dnd';
import { BACKEND_URL } from '../constants';

const Card = () => {
  const [levels, setLevels] = useState(Array.from({ length: 10 }, () => []));
  const [link, setLink] = useState('');
  const [pieces, setPieces] = useState([]);

  useEffect(() => {
    const distributedPieces = levels.map((level, index) => {
      return pieces.filter((_, pieceIndex) => pieceIndex % 10 === index);
    });
    setLevels(distributedPieces);
  }, [pieces]);

  const handleDragEnd = (result) => {
    if (!result.destination) return;

    const sourceLevel = parseInt(result.source.droppableId);
    const destLevel = parseInt(result.destination.droppableId);

    if (sourceLevel === destLevel && result.source.index === result.destination.index) {
      return; // No hacer nada si se suelta en la misma posición
    }

    const sourceItems = Array.from(levels[sourceLevel]);
    const [movedItem] = sourceItems.splice(result.source.index, 1);

    const destItems = Array.from(levels[destLevel]);
    destItems.splice(result.destination.index, 0, movedItem);

    const newLevels = [...levels];
    newLevels[sourceLevel] = sourceItems;
    newLevels[destLevel] = destItems;

    setLevels(newLevels);
  };

  const handleUploadClick = async () => {
    if (link.trim() === '') return;

    const newPiece = {
      id: link,
      link: link,
      title: link,
      status: 'processing...',
    };

    setPieces((prevPieces) => [...prevPieces, newPiece]);
    setLink('');

    try {
      const response = await fetch(`${BACKEND_URL}/upload_link`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ link }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      setPieces((prevPieces) =>
        prevPieces.map((piece) =>
          piece.id === link ? { ...piece, id: data.link, status: 'completed' } : piece
        )
      );

    } catch (error) {
      console.error('Error uploading link:', error);
      setPieces((prevPieces) =>
        prevPieces.map((piece) =>
          piece.id === link ? { ...piece, status: 'error' } : piece
        )
      );
    }
  };

  const handleGenerateRankingClick = async () => {
    const rankedLinks = levels.reduce((acc, level, index) => {
      level.forEach(piece => {
        acc.push({ link: piece.link, grade: index + 1 });
      });
      return acc;
    }, []);

    try {
      const response = await fetch(`${BACKEND_URL}/generate_ranking`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ links: rankedLinks, user: 1}),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      alert('Ranking generated successfully!');

    } catch (error) {
      console.error('Error generating ranking:', error);
      alert('Failed to generate ranking');
    }
  };

  return (
    <DragDropContext onDragEnd={handleDragEnd}>
      <div className='flex bg-white rounded-3xl lg:w-[800px] md:w-[600px] sm:w-[400px] mx-auto my-[8vh] flex-col font-roboto shadow-2xl'>
        <input
          type="text"
          placeholder='Paste Link...'
          className='bg-grey mt-[4vh] bg-slate-100 px-3 py-5 rounded-md mx-8 mb-[2vh] h-8 outline-none'
          value={link}
          onChange={(e) => setLink(e.target.value)}
        />
        <div className='flex align-middle justify-center items-center flex-col'>
          <button
            className='bg-blue-600 rounded-lg px-8 py-1.5 text-white mr-4 mb-[2vh] hover:bg-blue-700 text-md'
            onClick={handleUploadClick}
          >
            Upload Video
          </button>
        </div>
        <div className='align-middle justify-center bg-slate-100 overflow-y-auto max-h-[40vh] mb-[3vh] mx-8 rounded-lg'>
          {levels.map((level, levelIndex) => (
            <Droppable key={levelIndex} droppableId={String(levelIndex)}>
              {(provided) => (
                <div
                  className='mb-4 p-2 border rounded'
                  {...provided.droppableProps}
                  ref={provided.innerRef}
                >
                  <h3>Level {levelIndex + 1}</h3>
                  {level.map((piece, index) => (
                    <ListedPiece
                      key={piece.id}
                      piece={piece}
                      index={index}
                    />
                  ))}
                  {provided.placeholder}
                </div>
              )}
            </Droppable>
          ))}
        </div>
        <div className='flex justify-center'>
          <button
            className='bg-black rounded-lg px-8 py-1.5 text-white ml-4 mb-[3vh] hover:bg-slate-700 shadow-md text-md'
            onClick={handleGenerateRankingClick}
          >
            Generate Personal Rank
          </button>
        </div>
      </div>
    </DragDropContext>
  );
};

export default Card;
