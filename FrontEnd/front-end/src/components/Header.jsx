import React from 'react';
import { useLocation, Link, useNavigate } from 'react-router-dom';
import HeaderLogo from '../static/images/gran.png';
import { useAuth } from '../useAuth';
import { BACKEND_URL } from '../constants';

const Header = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const user = useAuth();

  // Log user email if available
  if (user) {
    console.log("email from header: " + user);
  }

  const isHome = location.pathname === '/home';
  const headerTitle = isHome ? 'PRE-COMPUTED RANKINGS' : 'BUILD YOUR RANK';
  const buttonText = isHome ? 'Build Ranking' : 'Home';
  const buttonLink = isHome ? '/upload' : '/home';

  const handleLogout = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/logout`, {
        method: 'GET',
        credentials: 'include',  // Include cookies for authentication
        headers: {
          'Content-Type': 'application/json'
          // Add any other headers if needed
        }
      });
      if (response.ok) {
        console.log('Logout successful');
        navigate('/');
      } else {
        console.error('Logout failed');
        // Handle failed logout scenario
      }
    } catch (error) {
      console.error('Error during logout:', error);
      // Handle error scenario
    }
  };

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
        <div className='flex flex-initial'>
          {user ? (
            <div className='flex items-center'>
              <span className='text-blue-600 font-roboto font-semibold cursor-pointer text-lg mr-4'>
                Logged in as {user}
              </span>
              <button
                className='text-blue-600 font-roboto font-semibold mr-8 cursor-pointer text-lg'
                onClick={handleLogout}
              >
                Logout
              </button>
            </div>
          ) : (
            <Link to={"/login"}>
              <div className='text-blue-600 font-roboto font-semibold cursor-pointer text-lg mr-4'>Login</div>
            </Link>
          )}
          <Link to={buttonLink}>
            <button className='text-blue-600 font-roboto font-semibold mr-8 cursor-pointer text-lg'>
              {buttonText}
            </button>
          </Link>
        </div>
      </div>
      <div className='h-[3px] bg-blue-600 w-full top-14'></div>
    </div>
  );
};

export default Header;
