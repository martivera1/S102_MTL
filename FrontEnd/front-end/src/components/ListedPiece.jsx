import React from 'react'
import PdfImage from '../static/images/pdf_icon.png'
import HttpImage from '../static/images/http_icon.png'
import UpArrow from '../static/images/up_arrow.svg'
import DownArrow from '../static/images/down_arrow.svg'

const ListedPiece = ({title, type, size, pos, total}) => {
  return (
    <div className='flex flex-row my-4 ml-6'>
      <div className='flex mr-4'>
        {type === 'pdf' ? <img src={PdfImage} alt='imageNotFound' className='size-14'></img> : <img src={HttpImage} alt='imageNotFound' className='size-14'></img>}
      </div>
      <div className='flex flex-col flex-grow'>
        <p className='font-roboto font-medium'>{title}</p>
        <p className='font-roboto text-sm'>{size}</p>
      </div>
       <div className="flex ml-auto font-roboto flex-row items-center mr-3">
        <button className='text-xl font-semibold mr-2 bg-white rounded-md shadow-sm hover:bg-slate-100'><img src={DownArrow} alt="down" className='size-6'/></button><p className='text-lg'>{pos}</p><p className='text-lg'>/</p><p className='text-lg '>{total}</p> <button className='text-xl ml-2 bg-white rounded-md shadow-sm hover:bg-slate-100'><img src={UpArrow} alt="up" className='size-6'/></button>
      </div>
    </div>
  )
}

export default ListedPiece