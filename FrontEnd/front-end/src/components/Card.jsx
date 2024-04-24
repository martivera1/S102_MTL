import React from 'react'
import ListedPiece from './ListedPiece'

const Card = () => {
  return (
    <div className='flex bg-white rounded-3xl mx-32 my-20 flex-col font-roboto max-w-4xl'>
        <input type="text" placeholder='Paste Link...' className='bg-grey mt-12 bg-slate-100 px-3 rounded-md mx-12 mb-8 h-8 outline-none'/>
        <div className='flex align-middle justify-center items-center flex-col'>
            <p className='mb-3'>Select the type of Link you want to load:</p>
            <div className='flex'>
                <button className='bg-blue-600 rounded-lg px-8 py-2 text-white mr-8 mb-6 hover:bg-blue-700'>PDF File</button>
                <button className='bg-blue-600 rounded-lg px-8 py-2 text-white ml-8 mb-6 hover:bg-blue-700'>Video File</button>
            </div>
        </div>
        <div className='align-middle justify-center bg-slate-100 overflow-y-auto max-h-72 mb-8 mx-12 rounded-lg'>
            <ListedPiece title={"Song.pdf"} size={"1.2 KB"} type={"pdf"}/>
            <ListedPiece title={"Song.pdf"} size={"1.2 KB"} type={"pdf"}/>
            <ListedPiece title={"https://www.youtube.com/"} size={"watch?v=dQw4w9WgXcQ&ab_channel=RickAstley"} type={"url"}/>
            <ListedPiece title={"Song.pdf"} size={"1.2 KB"} type={"pdf"}/>
            <ListedPiece title={"Song.pdf"} size={"1.2 KB"} type={"pdf"}/>
        </div>
    </div>
  )
}

export default Card
