import React from 'react';
import { useLocation, Link, useNavigate } from 'react-router-dom';
import HeaderLogo from '../static/images/gran.png';
import { useAuth } from '../useAuth';
import { BACKEND_URL } from '../constants';

const Header = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const user = useAuth();

  if (user) {
    console.log("email from header: " + user);
  }

  const isHome = location.pathname === '/home';
  const headerTitle = isHome ? 'PRE-COMPUTED RANKINGS' : 'BUILD YOUR RANK';
  const buttonText = isHome ? 'Build Ranking' : 'Home';
  const buttonLink = isHome ? '/upload' : '/home';

  return (
    <div className='sticky top-0 z-50'> 
      <div className='flex w-full bg-white py-3 shadow-md items-center justify-between'>
        <Link to={'/home'}>
          <div className='flex-initial ml-4'>
            <img src={HeaderLogo} alt='imageNotFound' className='w-36 h-auto'/>
          </div>
        </Link>
        <div className='flex-1 text-center'>
          <h1 className='font-semibold text-xl'>{headerTitle}</h1>
        </div>
        <div className='flex flex-initial items-center'>
          {user ? (
            <>
              <div className='flex items-center flex-col mr-4'>
                <div className='font-roboto font-medium text-md'>
                  Logged in as:
                </div>
                <div className='text-gray-800 text-md'>
                  {user}
                </div>
              </div>
              {isHome && (
                <Link to={buttonLink}>
                  <button className='text-blue-600 font-roboto font-semibold mr-8 cursor-pointer text-lg'>
                    {buttonText}
                  </button>
                </Link>
              )}
            </>
          ) : (
            <Link to={"/login"}>
              <div className='text-blue-600 font-roboto font-semibold cursor-pointer text-lg mr-4'>Login</div>
            </Link>
          )}
        </div>
      </div>
      <div className='h-[3px] bg-blue-600 w-full top-14'></div>
    </div>
  );
};

export default Header;
