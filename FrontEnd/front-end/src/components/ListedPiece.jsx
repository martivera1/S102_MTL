// ListedPiece.jsx
import React from 'react'
import PdfImage from '../static/images/pdf_icon.png'
import HttpImage from '../static/images/http_icon.png'
import { Draggable } from 'react-beautiful-dnd';

const ListedPiece = ({piece, index, total}) => {
  return (
    <Draggable draggableId={piece.id} index={index}>
      {(provided) => (
        <div className='flex flex-row my-4 ml-6' ref={provided.innerRef} {...provided.draggableProps} {...provided.dragHandleProps}>
          <div className='flex mr-4'>
            {piece.type === 'pdf' ? <img src={PdfImage} alt='imageNotFound' className='size-14'></img> : <img src={HttpImage} alt='imageNotFound' className='size-14'></img>}
          </div>
          <div className='flex flex-col flex-grow'>
            <p className='font-roboto font-medium'>{piece.title}</p>
            <p className='font-roboto text-sm'>{piece.size}</p>
          </div>
          <div className="flex ml-auto font-roboto flex-row items-center mr-3">
            <p className='text-lg'>{index + 1}</p><p className='text-lg'>/</p><p className='text-lg '>{total}</p>
          </div>
        </div>
      )}
    </Draggable>
  )
}

export default ListedPiece;
