import React, { useState } from 'react';
import ListedPiece from './ListedPiece';
import { DragDropContext, Droppable } from 'react-beautiful-dnd';

const Card = ({ pieces: initialPieces }) => {
  const [pieces, setPieces] = useState(initialPieces);

  const handleDragEnd = (result) => {
    if (!result.destination) return;

    const items = Array.from(pieces);
    const [reorderedItem] = items.splice(result.source.index, 1);
    items.splice(result.destination.index, 0, reorderedItem);

    setPieces(items);
  };

  return (
    <DragDropContext onDragEnd={handleDragEnd}>
      <Droppable droppableId="pieces">
        {(provided) => (
          <div
            className='flex bg-white rounded-3xl lg:w-[800px] md:w-[600px] sm:w-[400px] mx-auto my-[8vh] flex-col font-roboto shadow-2xl'
            {...provided.droppableProps}
            ref={provided.innerRef}
          >
            <input
              type="text"
              placeholder='Paste Link...'
              className='bg-grey mt-[4vh] bg-slate-100 px-3 py-5 rounded-md mx-8 mb-[2vh] h-8 outline-none'
            />
            <div className='flex align-middle justify-center items-center flex-col'>
              <button className='bg-blue-600 rounded-lg px-8 py-1.5 text-white mr-4 mb-[2vh] hover:bg-blue-700 text-md'>
                Upload Video
              </button>
            </div>
            <div className='align-middle justify-center bg-slate-100 overflow-y-auto max-h-[40vh] mb-[3vh] mx-8 rounded-lg'>
              {pieces.map((piece, index) => (
                <ListedPiece
                  key={piece.id}
                  piece={piece}
                  index={index}
                  total={pieces.length}
                />
              ))}
              {provided.placeholder}
            </div>
            <div className='flex justify-center'>
              <button className='bg-black rounded-lg px-8 py-1.5 text-white ml-4 mb-[3vh] hover:bg-slate-700 shadow-md text-md'>
                Generate Personal Rank
              </button>
            </div>
          </div>
        )}
      </Droppable>
    </DragDropContext>
  );
}

export default Card;
