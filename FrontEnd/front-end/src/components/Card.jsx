import React, { useState } from 'react'
import ListedPiece from './ListedPiece'
import { DragDropContext, Droppable } from 'react-beautiful-dnd';

const Card = ({pieces: initialPieces}) => {
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
          <div className='flex bg-white rounded-3xl mx-32 my-20 flex-col font-roboto shadow-2xl' {...provided.droppableProps} ref={provided.innerRef}>
            <input type="text" placeholder='Paste Link...' className='bg-grey mt-12 bg-slate-100 px-3 py-5 rounded-md mx-12 mb-8 h-8 outline-none'/>
            <div className='flex align-middle justify-center items-center flex-col'>
                <p className='mb-3'>Select the type of Link you want to load:</p>
                <div className='flex'>
                    <button className='bg-blue-600 rounded-lg px-12 py-1.5 text-white mr-4 mb-6 hover:bg-blue-700 text-lg'>PDF File</button>
                    <button className='bg-blue-600 rounded-lg px-12 py-1.5 text-white ml-4 mb-6 hover:bg-blue-700 text-lg'>Video File</button>
                </div>
            </div>
            <div className='align-middle justify-center bg-slate-100 overflow-y-auto max-h-96 mb-8 mx-12 rounded-lg'>
              {pieces.map((piece, index) => (
                <ListedPiece 
                  key={piece.id}
                  piece={piece}
                  index={index}
                  total = {pieces.length}
                />
              ))}
              {provided.placeholder}
            </div>
            <div className='flex justify-center'>
              <button className='bg-white rounded-lg px-12 py-1.5 text-blue-600 font-semibold ml-4 mb-6 hover:bg-slate-100 shadow-md text-lg'>Generate Personal Rank</button>
            </div>
          </div>
        )}
      </Droppable>
    </DragDropContext>
  )
}

export default Card;
