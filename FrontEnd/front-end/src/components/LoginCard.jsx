import React from 'react';
import GoogleLogo from '../static/images/google_icon.png';

const LoginCard = () => {
  const handleLogin = () => {
    window.location.href = 'http://localhost:5000/login'; // Point directly to the backend
  };

  return (
    <div className='flex bg-white rounded-3xl md:w-[500px] sm:w-[400px] mx-auto my-[8vh] flex-col font-roboto shadow-2xl p-8'>
      <h1 className='text-center font-bold text-2xl mb-4'>Login / Sign Up</h1>
      <p className='text-center text-gray-600 mb-8'>Access your account using Google</p>
      <div className='flex justify-center items-center mb-6'>
        <button
          className='bg-blue-600 rounded-lg px-8 py-2 text-white hover:bg-blue-700 text-md flex items-center'
          onClick={handleLogin}
        >
          <img src={GoogleLogo} alt='Google Icon' className='w-6 h-6 mr-2' />
          Login with Google
        </button>
      </div>
    </div>
  );
};

export default LoginCard;
