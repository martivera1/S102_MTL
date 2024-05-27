import React from 'react';
import { useLocation, Link } from 'react-router-dom';
import HeaderLogo from '../static/images/gran.png';

const Header = () => {
  const location = useLocation();
  
  const isHome = location.pathname === '/home';
  const headerTitle = isHome ? 'PRE-COMPUTED RANKINGS' : 'BUILD YOUR RANK';
  const buttonText = isHome ? 'Build Ranking' : 'Home';
  const buttonLink = isHome ? '/upload' : '/home';

  return (
    <div className='flex w-full bg-white py-3 shadow-md items-center'>
      <div className='flex-initial'>
        <img src={HeaderLogo} alt='imageNotFound' className='ml-4 w-32 h-auto'/>
      </div>
      <div className='flex-1'>
        <Link to={buttonLink}>
          <button className='text-blue-600 font-roboto font-semibold ml-14 cursor-pointer text-lg'>
            {buttonText}
          </button>
        </Link>
      </div>
      <div className='flex-1 text-center'>
        <h1 className='font-semibold text-xl ml-16'>{headerTitle}</h1>
      </div>
      <div className='flex flex-grow justify-end pr-8'>
        <div className='text-blue-600 font-roboto font-semibold mr-10 cursor-pointer text-lg'>Register</div>
        <div className='text-blue-600 font-roboto font-semibold mr-10 cursor-pointer text-lg'>Login</div>
      </div>  
    </div>
  );
};

export default Header;
