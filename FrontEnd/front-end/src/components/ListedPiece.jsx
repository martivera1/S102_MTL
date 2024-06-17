import React from 'react';
import HttpImage from '../static/images/http_icon.png';
import { Draggable } from 'react-beautiful-dnd';

const ListedPiece = ({ piece, index }) => {
  return (
    <Draggable draggableId={piece.id} index={index}>
      {(provided) => (
        <div className='flex flex-row my-4 ml-6' ref={provided.innerRef} {...provided.draggableProps} {...provided.dragHandleProps}>
          <div className='flex mr-4'>
            <img src={HttpImage} alt='imageNotFound' className='size-14'></img>
          </div>
          <div className='flex flex-col flex-grow'>
            <p className='font-roboto font-medium'>{piece.title}</p>
            <p className='font-roboto text-sm'>{piece.status}</p>
          </div>
        </div>
      )}
    </Draggable>
  );
};

export default ListedPiece;
