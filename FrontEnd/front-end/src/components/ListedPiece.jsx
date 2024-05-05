import React from 'react'
import Image1 from '../static/images/pdf_icon.png'
import Image2 from '../static/images/http_icon.png'

const ListedPiece = ({title, type, size}) => {
  return (
    <div className='flex flex-row my-4 ml-6'>
      <div className='flex mr-4'>
        {type === 'pdf' ? <img src={Image1} alt='imageNotFound' className='size-14'></img> : <img src={Image2} alt='imageNotFound' className='size-14'></img>}
      </div>
      <div className='flex flex-col'>
        <p className='font-roboto font-medium'>{title}</p>
        <p className='font-roboto text-sm'>{size}</p>
      </div>
    </div>
  )
}

export default ListedPiece