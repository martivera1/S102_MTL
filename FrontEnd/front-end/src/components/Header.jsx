import React from 'react'
import HeaderLogo from '../static/images/gran.png'

const Header = () => {
  return (
    <div className='flex w-full bg-white py-3 shadow-md' >
      <div className='flex-initial'>
        <img src={HeaderLogo} alt='imageNotFound' className='ml-4 w-32 h-auto'/>
      </div>
      <div className='flex flex-grow justify-end pr-8'>
        <div className='text-blue-600 font-roboto font-semibold mr-10 cursor-pointer text-lg'>Regster</div>
        <div className='text-blue-600 font-roboto font-semibold mr-10 cursor-pointer text-lg'>Login</div>
      </div>  
    </div>
  )
}

export default Header