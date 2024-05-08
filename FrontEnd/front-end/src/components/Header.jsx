import React from 'react'

const Header = () => {
  return (
    <div className='flex w-full bg-white py-3 shadow-md' >
      <div className='flex-initial'>
        <div className='pl-8 font-bold'>Logo?</div>
      </div>
      <div className='flex flex-grow justify-end pr-8'>
        <div className='text-blue-600 font-roboto font-semibold mr-10 cursor-pointer text-lg'>Regster</div>
        <div className='text-blue-600 font-roboto font-semibold mr-10 cursor-pointer text-lg'>Login</div>
      </div>  
    </div>
  )
}

export default Header