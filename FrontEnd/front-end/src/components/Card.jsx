import React from 'react'
import ListedPiece from './ListedPiece'

const Card = () => {
  return (
    <div className='flex bg-white rounded-3xl mx-32 my-20 flex-col font-roboto shadow-2xl'>
        <input type="text" placeholder='Paste Link...' className='bg-grey mt-12 bg-slate-100 px-3 py-5 rounded-md mx-12 mb-8 h-8 outline-none'/>
        <div className='flex align-middle justify-center items-center flex-col'>
            <p className='mb-3'>Select the type of Link you want to load:</p>
            <div className='flex'>
                <button className='bg-blue-600 rounded-lg px-12 py-1.5 text-white mr-4 mb-6 hover:bg-blue-700 text-lg'>PDF File</button>
                <button className='bg-blue-600 rounded-lg px-12 py-1.5 text-white ml-4 mb-6 hover:bg-blue-700 text-lg'>Video File</button>
            </div>
        </div>
        <div className='align-middle justify-center bg-slate-100 overflow-y-auto max-h-96 mb-8 mx-12 rounded-lg'>
            <ListedPiece title={"Song.pdf"} size={"1.2 KB"} type={"pdf"}/>
            <ListedPiece title={"Song.pdf"} size={"1.2 KB"} type={"pdf"}/>
            <ListedPiece title={"https://www.youtube.com/"} size={"watch?v=dQw4w9WgXcQ&ab_channel=RickAstley"} type={"url"}/>
            <ListedPiece title={"Song.pdf"} size={"1.2 KB"} type={"pdf"}/>
            <ListedPiece title={"Song.pdf"} size={"1.2 KB"} type={"pdf"}/>
            <ListedPiece title={"https://www.youtube.com/"} size={"watch?v=dQw4w9WgXcQ&ab_channel=RickAstley"} type={"url"}/>
            <ListedPiece title={"https://www.youtube.com/"} size={"watch?v=dQw4w9WgXcQ&ab_channel=RickAstley"} type={"url"}/>
        </div>
        <div className='flex justify-center'>
          <button className='bg-white rounded-lg px-12 py-1.5 text-blue-600 font-semibold ml-4 mb-6 hover:bg-slate-100 shadow-md text-lg'>Generate Personal Rank</button>
        </div>
    </div>
  )
}

export default Card
